from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder


def test_micro_question_builder_returns_specific_micro_questions():
    questions = MicroQuestionBuilder().build("Create a basic Node.js backend API")

    assert [question["question_id"] for question in questions] == [
        "base_packages",
        "project_structure",
        "file_responsibilities",
    ]
    assert "required npm packages" in questions[0]["prompt"]
    assert "7 essential project paths" in questions[1]["prompt"]
    assert "max 3-word purposes" in questions[2]["prompt"]
    assert all("compact JSON only" in question["prompt"] for question in questions)
    assert all("Create a basic Node.js backend API" not in question["prompt"] for question in questions)
