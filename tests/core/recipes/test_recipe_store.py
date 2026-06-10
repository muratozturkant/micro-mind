

import json

from micro_mind.core.recipes.recipe_store import RecipeStore


class TestRecipeStore:
    def test_save_and_load_recipe(self, tmp_path):
        store = RecipeStore(tmp_path / "recipes")
        recipe = {
            "recipe_id": "nodejs_backend_basic_v1",
            "status": "candidate",
            "approved": False,
            "task_family": "nodejs_backend_api",
            "title": "Basic Node.js Backend API",
            "tags": ["nodejs", "express", "backend_api"],
        }

        save_result = store.save(recipe)
        load_result = store.load("nodejs_backend_basic_v1")

        assert save_result["status"] == "saved"
        assert save_result["recipe_id"] == "nodejs_backend_basic_v1"
        assert load_result["status"] == "loaded"
        assert load_result["recipe"] == recipe

    def test_save_fails_without_recipe_id(self, tmp_path):
        store = RecipeStore(tmp_path / "recipes")

        result = store.save({"title": "Missing ID"})

        assert result == {
            "status": "failed",
            "reason": "missing_recipe_id",
        }

    def test_load_returns_not_found(self, tmp_path):
        store = RecipeStore(tmp_path / "recipes")

        result = store.load("missing_recipe")

        assert result["status"] == "not_found"
        assert result["recipe_id"] == "missing_recipe"

    def test_list_recipes(self, tmp_path):
        store = RecipeStore(tmp_path / "recipes")
        store.save(
            {
                "recipe_id": "nodejs_backend_basic_v1",
                "status": "candidate",
                "approved": False,
                "task_family": "nodejs_backend_api",
                "title": "Basic Node.js Backend API",
                "tags": ["nodejs", "express"],
            }
        )
        store.save(
            {
                "recipe_id": "flutter_app_basic_v1",
                "status": "approved",
                "approved": True,
                "task_family": "flutter_app",
                "title": "Basic Flutter App",
                "tags": ["flutter", "mobile_app"],
            }
        )

        result = store.list()

        assert result["status"] == "listed"
        assert len(result["recipes"]) == 2
        assert result["recipes"][0]["recipe_id"] == "flutter_app_basic_v1"
        assert result["recipes"][1]["recipe_id"] == "nodejs_backend_basic_v1"

    def test_list_marks_invalid_json(self, tmp_path):
        recipes_dir = tmp_path / "recipes"
        recipes_dir.mkdir()
        (recipes_dir / "broken.json").write_text("{bad json", encoding="utf-8")

        store = RecipeStore(recipes_dir)
        result = store.list()

        assert result["status"] == "listed"
        assert result["recipes"] == [
            {
                "recipe_id": "broken",
                "recipe_path": str(recipes_dir / "broken.json"),
                "status": "invalid_json",
            }
        ]

    def test_load_invalid_json_fails(self, tmp_path):
        recipes_dir = tmp_path / "recipes"
        recipes_dir.mkdir()
        (recipes_dir / "broken.json").write_text("{bad json", encoding="utf-8")

        store = RecipeStore(recipes_dir)
        result = store.load("broken")

        assert result["status"] == "failed"
        assert result["reason"] == "invalid_recipe_json"
        assert result["recipe_id"] == "broken"