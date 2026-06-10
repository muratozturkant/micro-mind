from micro_mind.core.micro_task.micro_question_builder import MicroQuestionBuilder


def test_micro_question_builder_returns_specific_micro_questions():
    questions = MicroQuestionBuilder().build("Create a basic Node.js backend API")

    assert [question["question_id"] for question in questions] == [
        "base_packages",
        "project_structure",
        "file_responsibilities",
    ]
    assert "required npm packages" in questions[0]["prompt"]
    assert "recommended project structure" in questions[1]["prompt"]
    assert "purpose of each file or directory" in questions[2]["prompt"]
    assert all("compact JSON only" in question["prompt"] for question in questions)
    assert all("Create a basic Node.js backend API" not in question["prompt"] for question in questions)
