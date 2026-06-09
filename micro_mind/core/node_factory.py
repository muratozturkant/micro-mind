class NodeFactory:
    def create(self, workflow_step: str) -> dict:
        node_map = {
            "analyze_task": {
                "node_type": "planner",
                "node_name": "TaskPlannerNode",
                "status": "available",
            },
            "create_project_structure": {
                "node_type": "execution",
                "node_name": "ProjectStructureNode",
                "status": "planned_not_implemented",
            },
            "install_dependencies": {
                "node_type": "execution",
                "node_name": "DependencyInstallNode",
                "status": "planned_not_implemented",
            },
            "create_mongo_connection": {
                "node_type": "execution",
                "node_name": "MongoConnectionNode",
                "status": "planned_not_implemented",
            },
            "create_user_model": {
                "node_type": "execution",
                "node_name": "UserModelNode",
                "status": "planned_not_implemented",
            },
            "create_jwt_service": {
                "node_type": "execution",
                "node_name": "JWTServiceNode",
                "status": "planned_not_implemented",
            },
            "create_auth_middleware": {
                "node_type": "execution",
                "node_name": "AuthMiddlewareNode",
                "status": "planned_not_implemented",
            },
            "create_register_route": {
                "node_type": "execution",
                "node_name": "RegisterRouteNode",
                "status": "planned_not_implemented",
            },
            "create_login_route": {
                "node_type": "execution",
                "node_name": "LoginRouteNode",
                "status": "planned_not_implemented",
            },
            "create_protected_route": {
                "node_type": "execution",
                "node_name": "ProtectedRouteNode",
                "status": "planned_not_implemented",
            },
            "verify_api": {
                "node_type": "verification",
                "node_name": "APIVerifyNode",
                "status": "planned_not_implemented",
            },
            "save_memory": {
                "node_type": "memory",
                "node_name": "MemoryNode",
                "status": "available",
            },
            "ask_human_for_solution_direction": {
                "node_type": "human_guidance",
                "node_name": "HumanGuidanceNode",
                "status": "waiting_for_human_guidance",
            },
        }

        return node_map.get(
            workflow_step,
            {
                "node_type": "unknown",
                "node_name": "UnknownNode",
                "status": "waiting_for_human_guidance",
            },
        )

    def create_many(self, workflow: list[str]) -> list[dict]:
        return [self.create(step) for step in workflow]
