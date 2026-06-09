class WorkflowBuilderNode:
    name = "WorkflowBuilderNode"

    def execute(self, task_plan: dict) -> list[str]:
        if task_plan.get("project_type") == "nodejs_api":
            return [
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
            ]

        return [
            "ask_human_for_solution_direction",
        ]
