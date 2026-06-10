from pathlib import Path

from micro_mind.core.planning.project_creation_execution_network import (
    ProjectCreationExecutionNetwork,
)


def test_project_creation_execution_network_runs_end_to_end(tmp_path):
    network = ProjectCreationExecutionNetwork()

    result = network.run(
        task="Create Node.js Express MongoDB JWT Auth API",
        project_name="Block Heaven",
        base_path=str(tmp_path),
    )

    project_path = tmp_path / "block_heaven"
    work_tree_log_path = project_path / ".micro_mind" / "work_tree.jsonl"

    assert result["status"] == "executed"
    assert result["project_name"] == "Block Heaven"
    assert result["project_path"] == str(project_path)
    assert result["work_tree_log_path"] == str(work_tree_log_path)

    assert project_path.exists()
    assert (project_path / "frontend").is_dir()
    assert (project_path / "backend").is_dir()
    assert (project_path / "database").is_dir()
    assert (project_path / "docs").is_dir()

    assert work_tree_log_path.exists()

    log_lines = work_tree_log_path.read_text(encoding="utf-8").splitlines()
    assert len(log_lines) >= 12

    assert result["task_plan_result"]["status"] == "planned"
    assert result["project_structure_result"]["status"] == "executed"


def test_project_creation_execution_network_waits_for_human_guidance(tmp_path):
    network = ProjectCreationExecutionNetwork()

    result = network.run(
        task="Create something unknown and unclear",
        project_name="Mystery Project",
        base_path=str(tmp_path),
    )

    assert result["status"] == "waiting_for_human_guidance"
    assert result["reason"] == "local_llm_could_not_create_reliable_plan"


def test_project_creation_execution_network_rejects_forbidden_base_path():
    network = ProjectCreationExecutionNetwork()

    result = network.run(
        task="Create Node.js Express MongoDB JWT Auth API",
        project_name="Block Heaven",
        base_path="/Volumes/HDD/projects",
    )

    assert result == {
        "status": "failed",
        "reason": "forbidden_base_path",
        "base_path": "/Volumes/HDD/projects",
        "allowed_base_path": "/Volumes/HDD/MM_projects",
    }
