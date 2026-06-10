

from micro_mind.core.logging.work_tree_logger import WorkTreeLogger


def test_work_tree_logger_writes_and_reads_entries(tmp_path):
    log_path = tmp_path / "work_tree.jsonl"
    logger = WorkTreeLogger(log_path)

    entry = logger.log(
        node_name="ProjectStructureNode",
        action="create_directory",
        target_path=str(tmp_path / "node_auth_api" / "backend"),
        status="planned",
        metadata={
            "project_name": "Node Auth API",
        },
    )

    entries = logger.read_entries()

    assert len(entries) == 1
    assert entries[0] == entry
    assert entries[0]["node_name"] == "ProjectStructureNode"
    assert entries[0]["action"] == "create_directory"
    assert entries[0]["status"] == "planned"
    assert entries[0]["metadata"] == {
        "project_name": "Node Auth API",
    }
    assert "timestamp" in entries[0]


def test_work_tree_logger_returns_empty_list_when_log_file_does_not_exist(tmp_path):
    logger = WorkTreeLogger(tmp_path / "missing" / "work_tree.jsonl")

    assert logger.read_entries() == []


def test_work_tree_logger_appends_multiple_entries(tmp_path):
    log_path = tmp_path / "work_tree.jsonl"
    logger = WorkTreeLogger(log_path)

    logger.log(
        node_name="ProjectStructureNode",
        action="create_directory",
        target_path=str(tmp_path / "node_auth_api" / "backend"),
        status="planned",
    )
    logger.log(
        node_name="ProjectStructureNode",
        action="create_directory",
        target_path=str(tmp_path / "node_auth_api" / "backend"),
        status="executed",
    )

    entries = logger.read_entries()

    assert len(entries) == 2
    assert entries[0]["status"] == "planned"
    assert entries[1]["status"] == "executed"