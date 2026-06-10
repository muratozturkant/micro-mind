from micro_mind.core.apply.apply_simulator import ApplySimulator


class TestApplySimulator:
    def test_simulate_valid_apply_plan(self):
        simulator = ApplySimulator()

        apply_plan = {
            "status": "apply_plan_created",
            "requires_human_approval": True,
            "will_write_real_files": True,
            "will_run_commands": True,
            "apply_tasks": [
                {
                    "id": "apply_1",
                    "from_micro_task": "task_1.1",
                    "action": "create_directory",
                    "target": "src/routes",
                },
                {
                    "id": "apply_2",
                    "from_micro_task": "task_1.2",
                    "action": "create_file",
                    "target": "src/app.js",
                },
            ],
        }

        result = simulator.simulate(apply_plan)

        assert result["status"] == "apply_simulated"
        assert result["apply_task_count"] == 2
        assert result["safe_to_request_human_approval"] is True
        assert result["will_write_real_files"] is False
        assert result["will_run_commands"] is False
        assert result["would_write_real_files_after_approval"] is True
        assert result["would_run_commands_after_approval"] is True

    def test_missing_apply_plan(self):
        simulator = ApplySimulator()

        result = simulator.simulate(None)

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_apply_plan"

    def test_missing_apply_tasks(self):
        simulator = ApplySimulator()

        result = simulator.simulate(
            {
                "status": "apply_plan_created",
                "apply_tasks": [],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_apply_tasks"

    def test_forbidden_target_is_rejected(self):
        simulator = ApplySimulator()

        result = simulator.simulate(
            {
                "status": "apply_plan_created",
                "apply_tasks": [
                    {
                        "id": "apply_1",
                        "from_micro_task": "task_1.1",
                        "target": "/Volumes/HDD/projects/test.js",
                    }
                ],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "forbidden_apply_target"

    def test_missing_micro_task_link(self):
        simulator = ApplySimulator()

        result = simulator.simulate(
            {
                "status": "apply_plan_created",
                "apply_tasks": [
                    {
                        "id": "apply_1",
                        "target": "src/app.js",
                    }
                ],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_micro_task_link"