

class ApplyPlanBuilder:
    FORBIDDEN_BASE_PATHS = [
        "/Volumes/HDD/projects",
    ]

    def build(self, simulation_report: dict | None) -> dict:
        if not simulation_report:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_simulation_report",
            }

        if simulation_report.get("status") != "simulated":
            return {
                "status": "waiting_for_human_guidance",
                "reason": "simulation_not_ready",
                "source_status": simulation_report.get("status"),
            }

        micro_tasks = simulation_report.get("micro_tasks") or []

        if not micro_tasks:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_micro_tasks",
            }

        apply_tasks = []

        for index, micro_task in enumerate(micro_tasks, start=1):
            target = micro_task.get("target")

            if self._is_forbidden_target(target):
                return {
                    "status": "waiting_for_human_guidance",
                    "reason": "forbidden_apply_target",
                    "target": target,
                }

            apply_tasks.append(
                {
                    "id": f"apply_{index}",
                    "from_micro_task": micro_task.get("id"),
                    "action": micro_task.get("type"),
                    "target": target,
                    "status": "planned",
                    "requires_approval": True,
                    "will_write_real_files": self._would_write_real_files(
                        micro_task.get("type")
                    ),
                    "will_run_commands": self._would_run_commands(micro_task.get("type")),
                }
            )

        return {
            "status": "apply_plan_created",
            "source_status": simulation_report.get("status"),
            "requires_human_approval": True,
            "will_write_real_files": any(
                task["will_write_real_files"] for task in apply_tasks
            ),
            "will_run_commands": any(task["will_run_commands"] for task in apply_tasks),
            "apply_task_count": len(apply_tasks),
            "apply_tasks": apply_tasks,
        }

    def _is_forbidden_target(self, target: str | None) -> bool:
        if not target:
            return False

        return any(target.startswith(path) for path in self.FORBIDDEN_BASE_PATHS)

    def _would_write_real_files(self, action: str | None) -> bool:
        return action in {
            "create_directory",
            "create_file",
            "write_file",
            "update_file",
            "delete_file",
        }

    def _would_run_commands(self, action: str | None) -> bool:
        return action in {
            "install_package",
            "run_command",
        }