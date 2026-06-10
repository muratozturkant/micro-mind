class MicroTaskChainBuilder:
    def build(self, task: str, facts: dict) -> dict:
        micro_tasks = []

        for index, dependency in enumerate(facts.get("dependencies", []), start=1):
            micro_tasks.append(self._task(
                task_id=f"task_0.{index}",
                task_type="install_package",
                target=dependency,
            ))

        tree_targets = facts.get("directories", []) + facts.get("files", [])
        for index, target in enumerate(tree_targets, start=1):
            task_type = (
                "create_directory"
                if target in facts.get("directories", [])
                else "create_file"
            )
            micro_tasks.append(self._task(
                task_id=f"task_1.{index}",
                task_type=task_type,
                target=target,
            ))

        for index, target in enumerate(facts.get("files", []), start=1):
            micro_tasks.append(self._task(
                task_id=f"task_2.{index}",
                task_type="verify_file",
                target=target,
            ))

        for index, target in enumerate(
            facts.get("task_specific_files", []),
            start=1,
        ):
            micro_tasks.append(self._task(
                task_id=f"task_3.{index}",
                task_type="create_file",
                target=target,
            ))

        for index, target in enumerate(
            facts.get("task_specific_files", []),
            start=1,
        ):
            micro_tasks.append(self._task(
                task_id=f"task_4.{index}",
                task_type="verify_file",
                target=target,
            ))

        return {
            "status": "simulated",
            "task": task,
            "facts": facts,
            "micro_tasks": micro_tasks,
        }

    def _task(self, task_id, task_type, target):
        return {
            "id": task_id,
            "type": task_type,
            "target": target,
            "status": "planned",
        }
