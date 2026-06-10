

class ApplySimulator:
    FORBIDDEN_BASE_PATHS = [
        "/Volumes/HDD/projects",
    ]

    def simulate(self, apply_plan: dict | None) -> dict:
        if not apply_plan:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_apply_plan",
            }

        if apply_plan.get("status") != "apply_plan_created":
            return {
                "status": "waiting_for_human_guidance",
                "reason": "apply_plan_not_ready",
                "source_status": apply_plan.get("status"),
            }

        apply_tasks = apply_plan.get("apply_tasks") or []

        if not apply_tasks:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_apply_tasks",
            }

        forbidden_targets = [
            task.get("target")
            for task in apply_tasks
            if self._is_forbidden_target(task.get("target"))
        ]

        if forbidden_targets:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "forbidden_apply_target",
                "forbidden_targets": forbidden_targets,
                "will_write_real_files": False,
                "will_run_commands": False,
            }

        missing_links = [
            task.get("id")
            for task in apply_tasks
            if not task.get("from_micro_task")
        ]

        if missing_links:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_micro_task_link",
                "apply_task_ids": missing_links,
                "will_write_real_files": False,
                "will_run_commands": False,
            }

        return {
            "status": "apply_simulated",
            "apply_task_count": len(apply_tasks),
            "requires_human_approval": apply_plan.get("requires_human_approval", True),
            "safe_to_request_human_approval": True,
            "will_write_real_files": False,
            "will_run_commands": False,
            "would_write_real_files_after_approval": apply_plan.get(
                "will_write_real_files", False
            ),
            "would_run_commands_after_approval": apply_plan.get(
                "will_run_commands", False
            ),
            "apply_tasks": apply_tasks,
        }

    def _is_forbidden_target(self, target: str | None) -> bool:
        if not target:
            return False

        return any(target.startswith(path) for path in self.FORBIDDEN_BASE_PATHS)