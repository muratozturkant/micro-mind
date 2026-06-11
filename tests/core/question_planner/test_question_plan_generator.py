from micro_mind.core.question_planner.question_plan_generator import (
    QuestionPlanGenerator,
)


def test_question_plan_generator_returns_empty_prompt_for_no_work():
    assert QuestionPlanGenerator().build_prompt("") == ""


def test_question_plan_generator_prompt_contains_required_instructions():
    prompt = QuestionPlanGenerator().build_prompt("Create auth API")

    assert "compact JSON only" in prompt
    assert "JSON array of objects" in prompt
    assert "question_id" in prompt
    assert "fact_key" in prompt
    assert "prompt" in prompt
    assert "one small fact only" in prompt
    assert "do not ask for code generation" in prompt
    assert "do not ask broad architecture questions" in prompt
    assert "package list" in prompt
    assert "project paths" in prompt
    assert "file responsibilities" in prompt
    assert "imports" in prompt
    assert "wiring" in prompt
    assert "verification" in prompt
    assert "Create auth API" in prompt
