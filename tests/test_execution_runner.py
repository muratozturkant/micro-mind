from micro_mind.core.execution_runner import ExecutionRunner


def test_execution_runner_executes_available_nodes_and_skips_unimplemented_nodes():
    runner = ExecutionRunner()

    result = runner.run([
        "analyze_task",
        "create_project_structure",
        "install_dependencies",
        "save_memory",
    ])

    assert result["status"] == "completed_with_skipped_nodes"
    assert result["executed_nodes"] == [
        "TaskPlannerNode",
        "MemoryNode",
    ]
    assert result["skipped_nodes"] == [
        {
            "node_name": "ProjectStructureNode",
            "reason": "node_not_implemented_yet",
        },
        {
            "node_name": "DependencyInstallNode",
            "reason": "node_not_implemented_yet",
        },
    ]
    assert result["waiting_nodes"] == []


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
