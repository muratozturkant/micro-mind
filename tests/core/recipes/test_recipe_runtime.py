from micro_mind.core.recipes.recipe_runtime import RecipeRuntime


class TestRecipeRuntime:
    def test_simulate_from_approved_recipe(self):
        runtime = RecipeRuntime()

        recipe = {
            "recipe_id": "nodejs_backend_basic_v1",
            "approved": True,
            "facts": {
                "dependencies": [
                    "express",
                    "dotenv",
                ]
            },
            "questions": [
                {
                    "question_id": "packages",
                }
            ],
            "micro_tasks": [
                {
                    "id": "task_1.1",
                    "type": "create_directory",
                    "target": "src/routes",
                }
            ],
        }

        result = runtime.simulate_from_recipe(
            recipe,
            task="Create a basic Node.js backend API",
        )

        assert result["status"] == "simulated"
        assert result["source"] == "recipe"
        assert result["recipe_id"] == "nodejs_backend_basic_v1"
        assert result["ai_used"] is False
        assert len(result["micro_tasks"]) == 1

    def test_missing_recipe(self):
        runtime = RecipeRuntime()

        result = runtime.simulate_from_recipe(None)

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "missing_recipe"

    def test_unapproved_recipe(self):
        runtime = RecipeRuntime()

        result = runtime.simulate_from_recipe(
            {
                "recipe_id": "candidate_recipe",
                "approved": False,
                "micro_tasks": [],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "recipe_not_approved"

    def test_recipe_without_micro_tasks(self):
        runtime = RecipeRuntime()

        result = runtime.simulate_from_recipe(
            {
                "recipe_id": "approved_recipe",
                "approved": True,
                "micro_tasks": [],
            }
        )

        assert result["status"] == "waiting_for_human_guidance"
        assert result["reason"] == "recipe_missing_micro_tasks"