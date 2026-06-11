from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder
from micro_mind.core.question_planner.question_plan_runtime import (
    QuestionPlanRuntime,
)


class AskLocalAI:
    def __init__(self, answer):
        self.prompts = []
        self.answer = answer

    def ask(self, prompt):
        self.prompts.append(prompt)
        return self.answer


class FailingLocalAI:
    def classify_task(self, prompt):
        return {
            "status": "failed",
            "parsed_response": None,
            "raw_response": {},
            "error": "local model failed",
        }


def test_question_plan_runtime_returns_sleeping_state_for_no_work():
    result = QuestionPlanRuntime(AskLocalAI("[]")).build_questions("")

    assert result == {
        "status": "sleeping",
        "reason": "no_work",
        "questions": [],
    }


def test_question_plan_runtime_uses_valid_local_ai_question_plan():
    local_ai = AskLocalAI(
        """[
          {
            "question_id": "Auth Packages",
            "fact_key": "Packages",
            "prompt": "List auth npm packages as compact JSON only."
          }
        ]"""
    )

    result = QuestionPlanRuntime(local_ai).build_questions("Create auth API")

    assert len(local_ai.prompts) == 1
    assert result["status"] == "question_plan_created"
    assert result["source"] == "local_ai"
    assert "planner_prompt" in result
    assert result["raw_response"] == local_ai.answer
    assert result["questions"] == [
        {
            "question_id": "auth_packages",
            "fact_key": "packages",
            "prompt": "List auth npm packages as compact JSON only.",
        }
    ]


def test_question_plan_runtime_falls_back_when_local_ai_fails():
    result = QuestionPlanRuntime(
        FailingLocalAI(),
        fallback_builder=MicroQuestionBuilder(),
    ).build_questions("Create API")

    assert result["status"] == "fallback_questions_used"
    assert result["source"] == "default_questions"
    assert result["reason"] == "local_ai_failed"
    assert result["questions"] == MicroQuestionBuilder().build("Create API")


def test_question_plan_runtime_falls_back_when_validator_rejects():
    local_ai = AskLocalAI(
        """[
          {
            "question_id": "bad",
            "fact_key": "bad",
            "prompt": "Write the full code as compact JSON only."
          }
        ]"""
    )

    result = QuestionPlanRuntime(
        local_ai,
        fallback_builder=MicroQuestionBuilder(),
    ).build_questions("Create API")

    assert result["status"] == "fallback_questions_used"
    assert result["source"] == "default_questions"
    assert result["reason"] == "prompt_requests_full_code_generation"
    assert result["parsed_response"] == [
        {
            "question_id": "bad",
            "fact_key": "bad",
            "prompt": "Write the full code as compact JSON only.",
        }
    ]
    assert result["questions"] == MicroQuestionBuilder().build("Create API")
