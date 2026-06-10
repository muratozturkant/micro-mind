

from micro_mind.core.project_tree.project_tree_store import ProjectTreeStore


class TestProjectTreeStore:
    def test_append_and_list_records(self, tmp_path):
        store = ProjectTreeStore(tmp_path / ".micro_mind" / "project_tree.jsonl")

        first_record = {
            "artifact_id": "artifact_001",
            "path": "src/app.js",
            "artifact_type": "file",
            "responsibility": "app_entry",
        }
        second_record = {
            "artifact_id": "artifact_002",
            "path": "src/routes/health.route.js",
            "artifact_type": "file",
            "responsibility": "health_route",
        }

        first_result = store.append(first_record)
        second_result = store.append(second_record)
        records = store.list()

        assert first_result == {
            "status": "stored",
            "artifact_id": "artifact_001",
        }
        assert second_result == {
            "status": "stored",
            "artifact_id": "artifact_002",
        }
        assert records == [first_record, second_record]

    def test_list_returns_empty_when_store_does_not_exist(self, tmp_path):
        store = ProjectTreeStore(tmp_path / ".micro_mind" / "project_tree.jsonl")

        assert store.list() == []

    def test_find_by_path(self, tmp_path):
        store = ProjectTreeStore(tmp_path / ".micro_mind" / "project_tree.jsonl")
        record = {
            "artifact_id": "artifact_001",
            "path": "src/controllers/health/getHealth.controller.js",
            "artifact_type": "file",
            "responsibility": "get_health_controller",
        }

        store.append(record)

        assert store.find_by_path("src/controllers/health/getHealth.controller.js") == record
        assert store.find_by_path("src/missing.js") is None

    def test_find_by_artifact_id(self, tmp_path):
        store = ProjectTreeStore(tmp_path / ".micro_mind" / "project_tree.jsonl")
        record = {
            "artifact_id": "artifact_001",
            "path": "src/app.js",
            "artifact_type": "file",
            "responsibility": "app_entry",
        }

        store.append(record)

        assert store.find_by_artifact_id("artifact_001") == record
        assert store.find_by_artifact_id("missing") is None