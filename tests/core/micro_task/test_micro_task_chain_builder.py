from micro_mind.core.micro_task.micro_task_chain_builder import MicroTaskChainBuilder


def test_micro_task_chain_builder_generates_simulated_micro_tasks():
    facts = {
        "dependencies": ["express", "dotenv", "cors"],
        "directories": ["src", "src/routes"],
        "files": ["src/app.js", "package.json"],
        "responsibilities": {},
    }

    result = MicroTaskChainBuilder().build(
        "Create a basic Node.js backend API",
        facts,
    )

    assert result["status"] == "simulated"
    assert result["task"] == "Create a basic Node.js backend API"
    assert result["facts"] == facts
    assert {"id": "task_0.1", "type": "install_package", "target": "express", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.1", "type": "create_directory", "target": "src", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_1.3", "type": "create_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
    assert {"id": "task_2.1", "type": "verify_file", "target": "src/app.js", "status": "planned"} in result["micro_tasks"]
