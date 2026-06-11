from micro_mind.core.question_planner.question_plan_validator import (
    QuestionPlanValidator,
)


def test_question_plan_validator_accepts_and_normalizes_valid_plan():
    result = QuestionPlanValidator().validate([
        {
            "id": "Base Packages",
            "purpose": "Package List",
            "question": "List npm packages as compact JSON only.",
        },
        {
            "question_id": "project-paths",
            "fact_key": "structure",
            "prompt": "List project paths as compact JSON only.",
        },
    ])

    assert result == {
        "status": "accepted",
        "questions": [
            {
                "question_id": "base_packages",
                "fact_key": "package_list",
                "prompt": "List npm packages as compact JSON only.",
            },
            {
                "question_id": "project_paths",
                "fact_key": "structure",
                "prompt": "List project paths as compact JSON only.",
            },
        ],
    }


def test_question_plan_validator_rejects_empty_plan():
    assert QuestionPlanValidator().validate([]) == {
        "status": "rejected",
        "reason": "empty_question_plan",
        "questions": [],
    }


def test_question_plan_validator_rejects_missing_fields():
    assert QuestionPlanValidator().validate([{"question_id": "packages"}]) == {
        "status": "rejected",
        "reason": "missing_required_fields",
        "questions": [],
    }


def test_question_plan_validator_appends_json_instruction_to_non_json_prompt():
    result = QuestionPlanValidator().validate([
        {
            "question_id": "packages",
            "fact_key": "packages",
            "prompt": "List npm packages.",
        }
    ])

    assert result == {
        "status": "accepted",
        "questions": [
            {
                "question_id": "packages",
                "fact_key": "packages",
                "prompt": "List npm packages. Return compact JSON only.",
            }
        ],
    }


def test_question_plan_validator_rejects_too_long_prompt():
    result = QuestionPlanValidator().validate([
        {
            "question_id": "packages",
            "fact_key": "packages",
            "prompt": f"{'x' * 241} JSON",
        }
    ])

    assert result == {
        "status": "rejected",
        "reason": "prompt_too_long",
        "questions": [],
    }


def test_question_plan_validator_rejects_full_code_prompt():
    result = QuestionPlanValidator().validate([
        {
            "question_id": "full_code",
            "fact_key": "code",
            "prompt": "Write the full code as JSON.",
        }
    ])

    assert result == {
        "status": "rejected",
        "reason": "prompt_requests_full_code_generation",
        "questions": [],
    }
