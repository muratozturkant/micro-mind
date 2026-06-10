from pathlib import Path

from micro_mind.core.execution_runner import ExecutionRunner


def test_execution_runner_executes_available_nodes_and_skips_unimplemented_nodes(tmp_path):
    runner = ExecutionRunner()
    work_tree_log_path = tmp_path / "node_auth_api" / ".micro_mind" / "work_tree.jsonl"

    result = runner.run(
        [
            "analyze_task",
            "create_project_structure",
            "install_dependencies",
            "save_memory",
        ],
        context={
            "project_name": "Node Auth API",
            "base_path": str(tmp_path),
            "work_tree_log_path": str(work_tree_log_path),
        },
    )

    project_path = tmp_path / "node_auth_api"

    assert result["status"] == "completed_with_skipped_nodes"
    assert result["executed_nodes"] == [
        "TaskPlannerNode",
        "ProjectStructureNode",
        "MemoryNode",
    ]
    assert result["skipped_nodes"] == [
        {
            "node_name": "DependencyInstallNode",
            "reason": "node_not_implemented_yet",
        },
    ]
    assert result["waiting_nodes"] == []
    assert (project_path / "frontend").is_dir()
    assert (project_path / "backend").is_dir()
    assert work_tree_log_path.exists()
    assert Path(result["node_results"][1]["project_path"]) == project_path


def test_execution_runner_waits_for_human_guidance_for_unknown_nodes():
    runner = ExecutionRunner()

    result = runner.run([
        "analyze_task",
        "unknown_future_step",
        "save_memory",
    ])

    assert result["status"] == "waiting_for_human_guidance"
    assert result["executed_nodes"] == [
        "TaskPlannerNode",
        "MemoryNode",
    ]
    assert result["waiting_nodes"] == [
        "UnknownNode",
    ]


def test_execution_runner_fails_when_available_node_context_is_missing():
    runner = ExecutionRunner()

    result = runner.run([
        "create_project_structure",
    ])

    assert result["status"] == "failed"
    assert result["failed_node"] == "ProjectStructureNode"
    assert result["failure"] == {
        "status": "failed",
        "node_name": "ProjectStructureNode",
        "reason": "missing_project_name",
    }
