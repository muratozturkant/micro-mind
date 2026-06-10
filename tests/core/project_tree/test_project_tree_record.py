from micro_mind.core.project_tree.project_tree_record import ProjectTreeRecord


class TestProjectTreeRecord:
    def test_create_project_tree_record(self):
        record = ProjectTreeRecord().create(
            artifact_id="artifact_001",
            path="src/routes/user/get_user.js",
            artifact_type="file",
            responsibility="get_user_route",
            created_by_task="task_18.2",
            recipe_id="nodejs_backend_basic_v1",
            node_id="route_creation_node",
            imports=["src/routes/index.js"],
            depends_on=["artifact_000"],
            verified_by=["task_18.4"],
            status="verified",
        )

        assert record["artifact_id"] == "artifact_001"
        assert record["path"] == "src/routes/user/get_user.js"
        assert record["artifact_type"] == "file"
        assert record["responsibility"] == "get_user_route"
        assert record["created_by_task"] == "task_18.2"
        assert record["recipe_id"] == "nodejs_backend_basic_v1"
        assert record["node_id"] == "route_creation_node"
        assert record["imports"] == ["src/routes/index.js"]
        assert record["depends_on"] == ["artifact_000"]
        assert record["verified_by"] == ["task_18.4"]
        assert record["status"] == "verified"
        assert "created_at" in record

    def test_create_record_with_defaults(self):
        record = ProjectTreeRecord().create(
            artifact_id="artifact_001",
            path="src/app.js",
            artifact_type="file",
            responsibility="app_entry",
            created_by_task="task_1.1",
        )

        assert record["imports"] == []
        assert record["depends_on"] == []
        assert record["verified_by"] == []
        assert record["status"] == "planned"