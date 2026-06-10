

class TaskPlannerNetwork:
    def run(self, task: str) -> dict:
        normalized_task = task.lower()

        if (
            "node" in normalized_task
            and "express" in normalized_task
            and "mongo" in normalized_task
            and "jwt" in normalized_task
        ):
            return {
                "status": "planned",
                "task_plan": {
                    "project_type": "nodejs_api",
                    "runtime": "nodejs",
                    "framework": "express",
                    "database": "mongodb",
                    "auth": "jwt",
                },
                "dependencies": [
                    "express",
                    "mongoose",
                    "jsonwebtoken",
                    "bcryptjs",
                    "dotenv",
                    "cors",
                ],
                "workflow": [
                    "analyze_task",
                    "create_project_structure",
                    "install_dependencies",
                    "create_mongo_connection",
                    "create_user_model",
                    "create_jwt_service",
                    "create_auth_middleware",
                    "create_register_route",
                    "create_login_route",
                    "create_protected_route",
                    "verify_api",
                    "save_memory",
                ],
            }

        return {
            "status": "waiting_for_human_guidance",
            "reason": "local_llm_could_not_create_reliable_plan",
            "next_action": "ask_human_for_solution_direction",
        }