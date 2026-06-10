

from micro_mind.core.apply.apply_plan_builder import ApplyPlanBuilder


class TestApplyPlanBuilder:
    def test_build_apply_plan_from_simulation_report(self):
        builder = ApplyPlanBuilder()

        simulation_report = {
            "status": "simulated",
            "micro_tasks": [
                {
                    "id": "task_1.1",
                    "type": "create_directory",
                    "target": "src/routes",
                    "status": "planned",
                },
                {
                    "id": "task_1.2",
                    "type": "create_file",
                    "target": "src/app.js",
                    "status": "planned",
                },
            ],
        }

        result = builder.build(simulation_report)

        assert result["status"] == "apply_plan_created"
        assert result["apply_task_count"] == 2
        assert result["requires_human_approval"] is True

        first_task = result["apply_tasks"][0]

        assert first_task["from_micro_task"] == "task_1.1"
        assert first_task["action"] == "create_directory"
        assert first_task["target"] == "src/routes"

    def test_missing_simulation_report(self):
        builder = ApplyPlanBuilder()

        result = builder.build(None)

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_simulation_report"

    def test_missing_micro_tasks(self):
        builder = ApplyPlanBuilder()

        result = builder.build(
            {
                "status": "simulated",
                "micro_tasks": [],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_micro_tasks"

    def test_forbidden_target_is_rejected(self):
        builder = ApplyPlanBuilder()

        result = builder.build(
            {
                "status": "simulated",
                "micro_tasks": [
                    {
                        "id": "task_1.1",
                        "type": "create_file",
                        "target": "/Volumes/HDD/projects/test.js",
                    }
                ],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "forbidden_apply_target"