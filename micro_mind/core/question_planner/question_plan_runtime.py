from micro_mind.core.micro_task.ai_fact_normalizer import AIFactNormalizer
from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder
from micro_mind.core.question_planner.question_plan_generator import (
    QuestionPlanGenerator,
)
from micro_mind.core.question_planner.question_plan_validator import (
    QuestionPlanValidator,
)


class QuestionPlanRuntime:
    def __init__(
        self,
        local_ai,
        fallback_builder=None,
        generator=None,
        validator=None,
        fact_normalizer=None,
    ):
        self.local_ai = local_ai
        self.fallback_builder = fallback_builder or MicroQuestionBuilder()
        self.generator = generator or QuestionPlanGenerator()
        self.validator = validator or QuestionPlanValidator()
        self.fact_normalizer = fact_normalizer or AIFactNormalizer()

    def build_questions(self, task: str) -> dict:
        if not isinstance(task, str) or not task.strip():
            return {
                "status": "sleeping",
                "reason": "no_work",
                "questions": [],
            }

        task = task.strip()

        try:
            prompt = self.generator.build_prompt(task)
            ai_result = self._ask_local_ai(prompt)
        except Exception:
            return self._fallback(task, "local_ai_failed")

        if ai_result.get("status") != "completed":
            return self._fallback(task, "local_ai_failed")

        validation = self.validator.validate(ai_result.get("parsed_response"))
        if validation["status"] != "accepted":
            return self._fallback(task, validation["reason"])

        return {
            "status": "question_plan_created",
            "source": "local_ai",
            "questions": validation["questions"],
        }

    def _ask_local_ai(self, prompt):
        if hasattr(self.local_ai, "ask"):
            raw_response = self.local_ai.ask(prompt)
            return {
                "status": "completed",
                "parsed_response": self.fact_normalizer.parse_json(raw_response),
                "raw_response": raw_response,
                "error": None,
            }

        response = self.local_ai.classify_task(prompt)
        if response.get("status") != "completed":
            return response

        return {
            "status": "completed",
            "parsed_response": response.get("parsed_response"),
            "raw_response": response.get("raw_response"),
            "error": None,
        }

    def _fallback(self, task, reason):
        return {
            "status": "fallback_questions_used",
            "source": "default_questions",
            "reason": reason,
            "questions": self.fallback_builder.build(task),
        }
