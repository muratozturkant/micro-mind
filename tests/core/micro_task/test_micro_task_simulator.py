from micro_mind.core.micro_task.micro_task_simulator import MicroTaskSimulator


class FakeLocalLlamaSpecies:
    def __init__(self):
        self.questions = []

    def classify_task(self, task):
        self.questions.append(task)
        if "required npm packages" in task:
            return {
                "status": "completed",
                "parsed_response": ["express", "dotenv", "cors"],
                "raw_response": {"source": "fake"},
                "error": None,
            }
        if "recommended project structure" in task:
            return {
                "status": "completed",
                "parsed_response": [
                    "src",
                    "src/app.js",
                    "src/routes",
                    "src/controllers",
                    "src/middleware",
                    "src/config",
                    "src/models",
                    "package.json",
                    "README.md",
                    ".gitignore",
                ],
                "raw_response": {"source": "fake"},
                "error": None,
            }
        return {
            "status": "completed",
            "parsed_response": {
                "src": "Application source code directory",
                "src/app.js": "Main application entry point",
                "src/routes": "API endpoint definitions",
                "src/controllers": "Request handling logic",
                "src/middleware": "Request processing utilities",
                "src/config": "Environment and app settings",
                "src/models": "Database schema definitions",
                "package.json": "Project dependencies and scripts",
                "README.md": "Project documentation and setup",
                ".gitignore": "Files excluded from version control",
            },
            "raw_response": {"source": "fake"},
            "error": None,
        }


def test_micro_task_simulator_returns_sleeping_state_for_no_work(tmp_path):
    result = MicroTaskSimulator(
        local_species=FakeLocalLlamaSpecies(),
        queue_dir=tmp_path,
    ).simulate({})

    assert result == {
        "status": "sleeping",
        "reason": "no_work",
    }


def test_micro_task_simulator_asks_local_ai_and_returns_simulation(tmp_path):
    local_species = FakeLocalLlamaSpecies()
    simulator = MicroTaskSimulator(
        local_species=local_species,
        queue_dir=tmp_path,
    )

    result = simulator.simulate({"task": "Create a basic Node.js backend API"})

    assert len(local_species.questions) == 3
    assert result["status"] == "simulated"
    assert result["facts"]["dependencies"] == ["express", "dotenv", "cors"]
    assert "src/routes" in result["facts"]["directories"]
    assert "src/app.js" in result["facts"]["files"]
    assert result["facts"]["responsibilities"]["src/app.js"] == "Main application entry point"
    assert {"id": "task_0.1", "type": "install_package", "target": "express", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.1", "type": "create_directory", "target": "src", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.7", "type": "create_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_2.1", "type": "verify_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
