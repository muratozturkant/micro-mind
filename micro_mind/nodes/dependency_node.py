class DependencyNode:
    name = "DependencyNode"

    def execute(self, task_plan: dict) -> list[str]:
        if task_plan.get("project_type") == "nodejs_api":
            dependencies = []

            if task_plan.get("framework") == "express":
                dependencies.append("express")
                dependencies.append("cors")

            if task_plan.get("database") == "mongodb":
                dependencies.append("mongoose")

            if task_plan.get("auth") == "jwt":
                dependencies.append("jsonwebtoken")
                dependencies.append("bcryptjs")

            dependencies.append("dotenv")

            return dependencies

        return []
