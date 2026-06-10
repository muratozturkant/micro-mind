from micro_mind.core.micro_task.micro_task_simulation_runner import (
    MicroTaskSimulationRunner,
)


class FakeLocalAI:
    def __init__(self):
        self.asked_questions = []

    def classify_task(self, question):
        self.asked_questions.append(question)
        if "required npm packages" in question:
            return {
                "status": "completed",
                "parsed_response": ["express", "dotenv", "cors"],
                "raw_response": {"answer": "packages"},
                "error": None,
            }
        if "7 essential project paths" in question:
            return {
                "status": "completed",
                "parsed_response": [
                    "src",
                    "src/app.js",
                    "src/routes",
                    "package.json",
                ],
                "raw_response": {"answer": "structure"},
                "error": None,
            }
        return {
            "status": "completed",
            "parsed_response": {
                "src": "Application source code directory",
                "src/app.js": "Main application entry point",
                "src/routes": "API endpoint definitions",
                "package.json": "Project dependencies and scripts",
            },
            "raw_response": {"answer": "responsibilities"},
            "error": None,
        }


class FailingLocalAI:
    def __init__(self):
        self.asked_questions = []

    def classify_task(self, question):
        self.asked_questions.append(question)
        if len(self.asked_questions) == 2:
            return {
                "status": "failed",
                "parsed_response": None,
                "raw_response": {"answer": "bad"},
                "error": "invalid_json",
            }
        return {
            "status": "completed",
            "parsed_response": ["express"],
            "raw_response": {"answer": "packages"},
            "error": None,
        }


def test_micro_task_simulation_runner_returns_sleeping_state_for_no_work():
    result = MicroTaskSimulationRunner(FakeLocalAI()).run("")

    assert result == {
        "status": "sleeping",
        "reason": "no_work",
    }


def test_micro_task_simulation_runner_asks_questions_and_returns_full_report():
    local_ai = FakeLocalAI()

    result = MicroTaskSimulationRunner(local_ai).run(
        "Create a basic Node.js backend API"
    )

    assert len(local_ai.asked_questions) == 3
    assert result["status"] == "simulated"
    assert result["task"] == "Create a basic Node.js backend API"
    assert [question["id"] for question in result["questions"]] == [
        "question_0.1",
        "question_1.1",
        "question_2.1",
    ]
    assert result["questions"][0]["purpose"] == "collect_base_packages"
    assert result["questions"][0]["raw_response"] == {"answer": "packages"}
    assert result["questions"][0]["normalized_fact"] == {
        "dependencies": ["express", "dotenv", "cors"],
    }
    assert result["facts"]["dependencies"] == ["express", "dotenv", "cors"]
    assert result["facts"]["directories"] == ["src", "src/routes"]
    assert result["facts"]["files"] == ["src/app.js", "package.json"]
    assert result["facts"]["responsibilities"]["src/app.js"] == (
        "Main application entry point"
    )
    assert {"id": "task_0.1", "type": "install_package", "target": "express", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.1", "type": "create_directory", "target": "src", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.3", "type": "create_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_2.1", "type": "verify_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
    assert result["simulation"]["status"] == "simulated"
    assert result["simulation"]["will_write_real_files"] is False
    assert result["simulation"]["will_run_commands"] is False


def test_micro_task_simulation_runner_returns_human_guidance_on_failed_ai_answer():
    result = MicroTaskSimulationRunner(FailingLocalAI()).run(
        "Create a basic Node.js backend API"
    )

    assert result["status"] == "waiting_for_human_guidance"
    assert result["reason"] == "local_ai_question_failed"
    assert result["failed_question"]["id"] == "question_1.1"
    assert result["failed_question"]["error"] == "invalid_json"
    assert result["partial_report"]["status"] == "partial"
    assert result["partial_report"]["questions"][0]["normalized_fact"] == {
        "dependencies": ["express"],
    }
