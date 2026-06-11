from micro_mind.core.micro_task.ai_fact_normalizer import AIFactNormalizer
from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder
from micro_mind.core.micro_task.micro_task_chain_builder import MicroTaskChainBuilder
from micro_mind.core.micro_task.micro_task_simulator import MicroTaskSimulator


class MicroTaskSimulationRunner:
    PURPOSES = {
        "base_packages": "collect_base_packages",
        "project_structure": "collect_project_structure",
        "file_responsibilities": "collect_file_responsibilities",
        "task_specific_files": "collect_task_specific_files",
    }

    QUESTION_IDS = {
        "base_packages": "question_0.1",
        "project_structure": "question_1.1",
        "file_responsibilities": "question_2.1",
        "task_specific_files": "question_3.1",
    }

    def __init__(
        self,
        local_ai,
        question_builder=None,
        fact_normalizer=None,
        chain_builder=None,
        simulator=None,
        question_plan_runtime=None,
    ):
        self.local_ai = local_ai
        self.question_builder = question_builder or MicroQuestionBuilder()
        self.fact_normalizer = fact_normalizer or AIFactNormalizer()
        self.chain_builder = chain_builder or MicroTaskChainBuilder()
        self.simulator = simulator or MicroTaskSimulator
        self.question_plan_runtime = question_plan_runtime

    def run(self, task: str) -> dict:
        if not isinstance(task, str) or not task.strip():
            return {
                "status": "sleeping",
                "reason": "no_work",
            }

        task = task.strip()
        questions_report = []
        answers = {}
        questions = self._build_questions(task)

        for index, question in enumerate(questions):
            report_question = self._report_question(question, index)
            response = self._ask(question["prompt"])

            if response.get("status") != "completed":
                failed_question = {
                    **report_question,
                    "raw_response": response.get("raw_response"),
                    "error": response.get("error"),
                }
                partial_report = self._partial_report(task, questions_report)
                return {
                    "status": "waiting_for_human_guidance",
                    "reason": "local_ai_question_failed",
                    "failed_question": failed_question,
                    "partial_report": partial_report,
                }

            try:
                normalized_fact = self._normalize_question_fact(
                    question["fact_key"],
                    response.get("parsed_response"),
                )
            except Exception as error:
                failed_question = {
                    **report_question,
                    "raw_response": response.get("raw_response"),
                    "error": str(error),
                }
                partial_report = self._partial_report(task, questions_report)
                return {
                    "status": "waiting_for_human_guidance",
                    "reason": "local_ai_question_failed",
                    "failed_question": failed_question,
                    "partial_report": partial_report,
                }

            questions_report.append({
                **report_question,
                "raw_response": response.get("raw_response"),
                "normalized_fact": normalized_fact,
            })
            answers[question["fact_key"]] = response.get("parsed_response")

        facts = self.fact_normalizer.normalize(
            packages=answers.get("packages"),
            structure=answers.get("structure"),
            responsibilities=answers.get("responsibilities"),
            task_specific_files=answers.get("task_specific_files"),
        )
        chain = self.chain_builder.build(task, facts)
        simulation = self.simulator.simulate_chain(
            task=task,
            facts=facts,
            micro_tasks=chain["micro_tasks"],
        )

        return {
            "status": "simulated",
            "task": task,
            "questions": questions_report,
            "facts": facts,
            "micro_tasks": chain["micro_tasks"],
            "simulation": simulation,
        }

    def _ask(self, question):
        try:
            if hasattr(self.local_ai, "ask"):
                raw_answer = self.local_ai.ask(question)
                return {
                    "status": "completed",
                    "parsed_response": self.fact_normalizer.parse_json(raw_answer),
                    "raw_response": raw_answer,
                    "error": None,
                }

            return self.local_ai.classify_task(question)
        except Exception as error:
            return {
                "status": "failed",
                "parsed_response": None,
                "raw_response": None,
                "error": str(error),
            }

    def _normalize_question_fact(self, fact_key, answer):
        if fact_key == "packages":
            return {
                "dependencies": self.fact_normalizer.normalize(
                    packages=answer,
                )["dependencies"],
            }

        if fact_key == "structure":
            normalized = self.fact_normalizer.normalize(
                structure=answer,
            )
            return {
                "directories": normalized["directories"],
                "files": normalized["files"],
            }

        if fact_key == "responsibilities":
            return {
                "responsibilities": self.fact_normalizer.normalize(
                    responsibilities=answer,
                )["responsibilities"],
            }

        if fact_key == "task_specific_files":
            return {
                "task_specific_files": self.fact_normalizer.normalize(
                    task_specific_files=answer,
                )["task_specific_files"],
            }

        return {}

    def _build_questions(self, task):
        if self.question_plan_runtime is None:
            return self.question_builder.build(task)

        result = self.question_plan_runtime.build_questions(task)
        if result.get("status") in {
            "question_plan_created",
            "fallback_questions_used",
        }:
            return result.get("questions", [])

        return self.question_builder.build(task)

    def _report_question(self, question, index):
        question_id = question["question_id"]
        return {
            "id": self.QUESTION_IDS.get(question_id, f"question_{index}.1"),
            "purpose": self.PURPOSES.get(
                question_id,
                f"collect_{question['fact_key']}",
            ),
            "question": question["prompt"],
        }

    def _partial_report(self, task, questions):
        return {
            "status": "partial",
            "task": task,
            "questions": questions,
            "facts": {},
            "micro_tasks": [],
            "simulation": {},
        }
