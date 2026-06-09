class TaskPlannerNode:
    name = "TaskPlannerNode"

    def execute(self, task: str) -> dict:
        normalized_task = task.lower()

        if (
            "node" in normalized_task
            and "express" in normalized_task
            and "mongo" in normalized_task
            and "jwt" in normalized_task
        ):
            return {
                "project_type": "nodejs_api",
                "runtime": "nodejs",
                "framework": "express",
                "database": "mongodb",
                "auth": "jwt",
            }

        return {
            "status": "waiting_for_human_guidance",
            "reason": "local_llm_could_not_create_reliable_plan",
        }
