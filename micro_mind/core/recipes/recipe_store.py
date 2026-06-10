

import json
from pathlib import Path


class RecipeStore:
    def __init__(self, recipes_dir: str | Path):
        self.recipes_dir = Path(recipes_dir)

    def save(self, recipe: dict) -> dict:
        if not recipe:
            return {
                "status": "failed",
                "reason": "missing_recipe",
            }

        recipe_id = recipe.get("recipe_id")

        if not recipe_id:
            return {
                "status": "failed",
                "reason": "missing_recipe_id",
            }

        self.recipes_dir.mkdir(parents=True, exist_ok=True)

        recipe_path = self.recipes_dir / f"{recipe_id}.json"
        recipe_path.write_text(
            json.dumps(recipe, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return {
            "status": "saved",
            "recipe_id": recipe_id,
            "recipe_path": str(recipe_path),
        }

    def load(self, recipe_id: str) -> dict:
        if not recipe_id:
            return {
                "status": "failed",
                "reason": "missing_recipe_id",
            }

        recipe_path = self.recipes_dir / f"{recipe_id}.json"

        if not recipe_path.exists():
            return {
                "status": "not_found",
                "recipe_id": recipe_id,
                "recipe_path": str(recipe_path),
            }

        try:
            recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            return {
                "status": "failed",
                "reason": "invalid_recipe_json",
                "recipe_id": recipe_id,
                "error": str(error),
            }

        return {
            "status": "loaded",
            "recipe_id": recipe_id,
            "recipe_path": str(recipe_path),
            "recipe": recipe,
        }

    def list(self) -> dict:
        if not self.recipes_dir.exists():
            return {
                "status": "listed",
                "recipes": [],
            }

        recipes = []

        for recipe_path in sorted(self.recipes_dir.glob("*.json")):
            try:
                recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                recipes.append(
                    {
                        "recipe_id": recipe_path.stem,
                        "recipe_path": str(recipe_path),
                        "status": "invalid_json",
                    }
                )
                continue

            recipes.append(
                {
                    "recipe_id": recipe.get("recipe_id", recipe_path.stem),
                    "recipe_path": str(recipe_path),
                    "status": recipe.get("status"),
                    "approved": recipe.get("approved", False),
                    "task_family": recipe.get("task_family"),
                    "title": recipe.get("title"),
                    "tags": recipe.get("tags", []),
                }
            )

        return {
            "status": "listed",
            "recipes": recipes,
        }