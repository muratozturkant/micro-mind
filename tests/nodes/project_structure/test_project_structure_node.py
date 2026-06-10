

from pathlib import Path

from micro_mind.nodes.project_structure.project_structure_node import ProjectStructureNode


def test_project_structure_node_creates_project_directories_and_files(tmp_path):
    node = ProjectStructureNode()

    result = node.execute({
        "project_name": "Node Auth API",
        "base_path": str(tmp_path),
    })

    project_path = tmp_path / "node_auth_api"

    assert result["status"] == "executed"
    assert result["node_name"] == "ProjectStructureNode"
    assert result["project_name"] == "Node Auth API"
    assert result["project_slug"] == "node_auth_api"
    assert Path(result["project_path"]) == project_path
    assert result["work_tree_log_path"] is None

    assert (project_path / "frontend").is_dir()
    assert (project_path / "backend").is_dir()
    assert (project_path / "database").is_dir()
    assert (project_path / "docs").is_dir()
    assert (project_path / "PROJECT_STATE.md").is_file()
    assert (project_path / "DEVELOPMENT_RULES.md").is_file()

    assert (project_path / "PROJECT_STATE.md").read_text(encoding="utf-8") == (
        "# Node Auth API Project State\n\nStatus: initialized\n"
    )
    assert "Work incrementally" in (project_path / "DEVELOPMENT_RULES.md").read_text(
        encoding="utf-8"
    )


def test_project_structure_node_fails_without_project_name(tmp_path):
    node = ProjectStructureNode()

    result = node.execute({
        "base_path": str(tmp_path),
    })

    assert result == {
        "status": "failed",
        "node_name": "ProjectStructureNode",
        "reason": "missing_project_name",
    }


def test_project_structure_node_fails_without_base_path():
    node = ProjectStructureNode()

    result = node.execute({
        "project_name": "Node Auth API",
    })

    assert result == {
        "status": "failed",
        "node_name": "ProjectStructureNode",
        "reason": "missing_base_path",
    }


def test_project_structure_node_logs_work_tree_entries(tmp_path):
    node = ProjectStructureNode()
    log_path = tmp_path / "logs" / "work_tree.jsonl"

    result = node.execute({
        "project_name": "Node Auth API",
        "base_path": str(tmp_path),
        "work_tree_log_path": str(log_path),
    })

    assert result["status"] == "executed"
    assert result["work_tree_log_path"] == str(log_path)

    log_lines = log_path.read_text(encoding="utf-8").strip().splitlines()

    assert len(log_lines) == 12
    assert any('"action": "create_directory"' in line for line in log_lines)
    assert any('"action": "write_file"' in line for line in log_lines)
    assert any('"status": "planned"' in line for line in log_lines)
    assert any('"status": "executed"' in line for line in log_lines)
    assert any('"target_path":' in line and "frontend" in line for line in log_lines)
    assert any('"target_path":' in line and "PROJECT_STATE.md" in line for line in log_lines)
