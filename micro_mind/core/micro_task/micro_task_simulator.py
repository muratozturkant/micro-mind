from micro_mind.core.micro_task.ai_fact_normalizer import AIFactNormalizer
from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder
from micro_mind.core.micro_task.micro_task_chain_builder import MicroTaskChainBuilder
from micro_mind.core.model_queue.file_model_queue import FileModelQueue


class MicroTaskSimulator:
    def __init__(
        self,
        local_species,
        queue_dir,
        question_builder=None,
        fact_normalizer=None,
        chain_builder=None,
    ):
        self.local_species = local_species
        self.queue = FileModelQueue(queue_dir)
        self.question_builder = question_builder or MicroQuestionBuilder()
        self.fact_normalizer = fact_normalizer or AIFactNormalizer()
        self.chain_builder = chain_builder or MicroTaskChainBuilder()

    def simulate(self, request: dict) -> dict:
        task = (request or {}).get("task")
        if not isinstance(task, str) or not task.strip():
            return {
                "status": "sleeping",
                "reason": "no_work",
            }

        task = task.strip()
        advisor_answers = {}

        for question in self.question_builder.build(task):
            queued = self.queue.enqueue({
                "task": task,
                "question_id": question["question_id"],
                "question": question["prompt"],
            })
            response = self.local_species.classify_task(question["prompt"])
            request_id = queued["request"]["request_id"]

            if response.get("status") != "completed":
                self.queue.mark_failed(request_id, response.get("error") or "advisor_failed")
                return {
                    "status": "failed",
                    "reason": "advisor_failed",
                    "question_id": question["question_id"],
                    "error": response.get("error"),
                }

            self.queue.mark_completed(request_id, response)
            advisor_answers[question["fact_key"]] = response.get("parsed_response")

        facts = self.fact_normalizer.normalize(
            packages=advisor_answers.get("packages"),
            structure=advisor_answers.get("structure"),
            responsibilities=advisor_answers.get("responsibilities"),
        )

        return self.chain_builder.build(task, facts)

    @staticmethod
    def simulate_chain(task, facts, micro_tasks):
        return {
            "status": "simulated",
            "task": task,
            "facts": facts,
            "micro_tasks": micro_tasks,
            "planned_task_count": len(micro_tasks),
            "will_write_real_files": False,
            "will_run_commands": False,
            "will_apply_to_real_workspace": False,
        }
