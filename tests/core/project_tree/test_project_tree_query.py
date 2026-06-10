

from micro_mind.core.project_tree.project_tree_query import ProjectTreeQuery


class TestProjectTreeQuery:
    def test_find_by_recipe_id(self):
        records = [
            {
                "artifact_id": "artifact_001",
                "path": "src/app.js",
                "recipe_id": "nodejs_backend_basic_v1",
            },
            {
                "artifact_id": "artifact_002",
                "path": "src/routes/health.route.js",
                "recipe_id": "health_route_v1",
            },
        ]

        result = ProjectTreeQuery(records).find_by_recipe_id("nodejs_backend_basic_v1")

        assert result == [records[0]]

    def test_find_by_task_id(self):
        records = [
            {
                "artifact_id": "artifact_001",
                "path": "src/app.js",
                "created_by_task": "task_1.1",
            },
            {
                "artifact_id": "artifact_002",
                "path": "src/routes/health.route.js",
                "created_by_task": "task_2.1",
            },
        ]

        result = ProjectTreeQuery(records).find_by_task_id("task_2.1")

        assert result == [records[1]]

    def test_find_by_responsibility(self):
        records = [
            {
                "artifact_id": "artifact_001",
                "path": "src/controllers/health/getHealth.controller.js",
                "responsibility": "get_health_controller",
            },
            {
                "artifact_id": "artifact_002",
                "path": "src/app.js",
                "responsibility": "app_entry",
            },
        ]

        result = ProjectTreeQuery(records).find_by_responsibility(
            "get_health_controller"
        )

        assert result == [records[0]]

    def test_find_dependents(self):
        records = [
            {
                "artifact_id": "artifact_001",
                "path": "src/controllers/health/getHealth.controller.js",
            },
            {
                "artifact_id": "artifact_002",
                "path": "src/routes/health.route.js",
                "depends_on": ["artifact_001"],
            },
        ]

        result = ProjectTreeQuery(records).find_dependents("artifact_001")

        assert result == [records[1]]

    def test_find_import_targets(self):
        records = [
            {
                "artifact_id": "artifact_001",
                "path": "src/routes/health.route.js",
                "imports": ["src/controllers/health/getHealth.controller.js"],
            },
            {
                "artifact_id": "artifact_002",
                "path": "src/app.js",
                "imports": ["src/routes/health.route.js"],
            },
        ]

        result = ProjectTreeQuery(records).find_import_targets(
            "src/routes/health.route.js"
        )

        assert result == [records[1]]