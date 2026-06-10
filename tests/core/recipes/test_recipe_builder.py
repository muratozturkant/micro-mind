from micro_mind.core.recipes.recipe_builder import RecipeBuilder


class TestRecipeBuilder:
    def test_build_recipe_candidate(self):
        builder = RecipeBuilder()

        simulation_report = {
            "status": "simulated",
            "facts": {
                "dependencies": [
                    "express",
                    "dotenv",
                    "cors",
                ]
            },
            "micro_tasks": [
                {
                    "id": "task_1.1",
                    "type": "create_directory",
                    "target": "src/routes",
                }
            ],
            "questions": [
                {
                    "question_id": "packages",
                }
            ],
            "simulation": {
                "status": "simulated",
            },
        }

        apply_simulation_report = {
            "status": "apply_simulated",
        }

        result = builder.build_candidate(
            task="Create a basic Node.js backend API",
            simulation_report=simulation_report,
            apply_simulation_report=apply_simulation_report,
        )

        assert result["status"] == "recipe_candidate_created"

        recipe = result["recipe"]

        assert recipe["approved"] is False
        assert recipe["status"] == "candidate"
        assert recipe["task_family"] == "nodejs_backend_api"
        assert recipe["facts"]["dependencies"] == [
            "express",
            "dotenv",
            "cors",
        ]
        assert len(recipe["micro_tasks"]) == 1

    def test_missing_task_fails(self):
        builder = RecipeBuilder()

        result = builder.build_candidate(
            task="",
            simulation_report={"status": "simulated"},
        )

        assert result["status"] == "failed"
        assert result["reason"] == "missing_task"

    def test_missing_simulation_report_fails(self):
        builder = RecipeBuilder()

        result = builder.build_candidate(
            task="Create API",
            simulation_report=None,
        )

        assert result["status"] == "failed"
        assert result["reason"] == "missing_simulation_report"

    def test_invalid_simulation_status_fails(self):
        builder = RecipeBuilder()

        result = builder.build_candidate(
            task="Create API",
            simulation_report={
                "status": "waiting_for_human_guidance",
            },
        )

        assert result["status"] == "failed"
        assert result["reason"] == "simulation_not_successful"

    def test_generates_recipe_id(self):
        builder = RecipeBuilder()

        result = builder.build_candidate(
            task="Create a basic Node.js backend API",
            simulation_report={
                "status": "simulated",
            },
        )

        assert result["status"] == "recipe_candidate_created"
        assert result["recipe_id"].endswith("_v1")