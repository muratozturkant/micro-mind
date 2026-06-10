from micro_mind.core.recipes.recipe_matcher import RecipeMatcher


class TestRecipeMatcher:
    def test_returns_no_match_when_no_recipes_exist(self):
        matcher = RecipeMatcher()

        result = matcher.match(
            task="Create Node.js backend API",
            recipes=[],
        )

        assert result["status"] == "no_match"
        assert result["reason"] == "no_recipes"

    def test_matches_nodejs_backend_recipe(self):
        matcher = RecipeMatcher()

        recipes = [
            {
                "recipe_id": "nodejs_backend_basic_v1",
                "approved": True,
                "task_family": "nodejs_backend_api",
                "title": "Basic Node.js Backend API",
                "tags": ["nodejs", "express", "backend_api"],
            }
        ]

        result = matcher.match(
            task="Create Node.js backend API",
            recipes=recipes,
        )

        assert result["status"] == "matched"
        assert result["best_match"]["recipe_id"] == "nodejs_backend_basic_v1"

    def test_prefers_approved_recipe(self):
        matcher = RecipeMatcher()

        recipes = [
            {
                "recipe_id": "candidate_recipe",
                "approved": False,
                "task_family": "nodejs_backend_api",
                "title": "Node Backend",
                "tags": ["nodejs"],
            },
            {
                "recipe_id": "approved_recipe",
                "approved": True,
                "task_family": "nodejs_backend_api",
                "title": "Node Backend",
                "tags": ["nodejs"],
            },
        ]

        result = matcher.match(
            task="Node.js backend API",
            recipes=recipes,
        )

        assert result["status"] == "matched"
        assert result["best_match"]["recipe_id"] == "approved_recipe"

    def test_matches_using_facts(self):
        matcher = RecipeMatcher()

        recipes = [
            {
                "recipe_id": "nodejs_backend_basic_v1",
                "approved": True,
                "facts": {
                    "dependencies": [
                        "express",
                        "dotenv",
                        "cors",
                    ]
                },
            }
        ]

        result = matcher.match(
            facts={
                "dependencies": [
                    "express",
                    "dotenv",
                    "cors",
                ]
            },
            recipes=recipes,
        )

        assert result["status"] == "matched"
        assert result["best_match"]["recipe_id"] == "nodejs_backend_basic_v1"

    def test_returns_no_match_when_score_is_too_low(self):
        matcher = RecipeMatcher()

        recipes = [
            {
                "recipe_id": "flutter_recipe",
                "approved": True,
                "tags": ["flutter"],
            }
        ]

        result = matcher.match(
            task="Node.js backend API",
            recipes=recipes,
            min_score=0.5,
        )

        assert result["status"] == "no_match"
        assert result["reason"] == "score_below_threshold"