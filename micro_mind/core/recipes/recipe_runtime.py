class RecipeRuntime:
    def simulate_from_recipe(self, recipe: dict | None, task: str = "") -> dict:
        if not recipe:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "missing_recipe",
            }

        if recipe.get("approved") is not True:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "recipe_not_approved",
                "recipe_id": recipe.get("recipe_id"),
            }

        facts = recipe.get("facts") or {}
        micro_tasks = recipe.get("micro_tasks") or []

        if not micro_tasks:
            return {
                "status": "waiting_for_human_guidance",
                "reason": "recipe_missing_micro_tasks",
                "recipe_id": recipe.get("recipe_id"),
            }

        return {
            "status": "simulated",
            "source": "recipe",
            "recipe_id": recipe.get("recipe_id"),
            "task": task or recipe.get("description") or recipe.get("title") or "",
            "facts": facts,
            "questions": recipe.get("questions", []),
            "micro_tasks": micro_tasks,
            "simulation": {
                "status": "simulated",
                "source": "recipe",
                "will_write_real_files": False,
                "will_run_commands": False,
                "will_apply_to_real_workspace": False,
                "micro_task_count": len(micro_tasks),
            },
            "ai_used": False,
        }
