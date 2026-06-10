

class RecipeMatcher:
    def match(
        self,
        *,
        task: str = "",
        facts: dict | None = None,
        recipes: list[dict] | None = None,
        min_score: float = 0.3,
    ) -> dict:
        recipes = recipes or []
        facts = facts or {}

        if not recipes:
            return {
                "status": "no_match",
                "reason": "no_recipes",
                "matches": [],
            }

        candidates = []

        for recipe in recipes:
            score = self._score_recipe(task=task, facts=facts, recipe=recipe)

            if score >= min_score:
                candidates.append(
                    {
                        "recipe_id": recipe.get("recipe_id"),
                        "score": round(score, 4),
                        "approved": recipe.get("approved", False),
                        "task_family": recipe.get("task_family"),
                        "title": recipe.get("title"),
                        "tags": recipe.get("tags", []),
                        "recipe": recipe,
                    }
                )

        candidates.sort(
            key=lambda candidate: (
                candidate["approved"],
                candidate["score"],
            ),
            reverse=True,
        )

        if not candidates:
            return {
                "status": "no_match",
                "reason": "score_below_threshold",
                "matches": [],
            }

        return {
            "status": "matched",
            "best_match": candidates[0],
            "matches": candidates,
        }

    def _score_recipe(self, *, task: str, facts: dict, recipe: dict) -> float:
        score = 0.0
        task_tokens = self._tokens(task)
        recipe_tokens = set()

        recipe_tokens.update(self._tokens(recipe.get("recipe_id", "")))
        recipe_tokens.update(self._tokens(recipe.get("task_family", "")))
        recipe_tokens.update(self._tokens(recipe.get("title", "")))
        recipe_tokens.update(self._tokens(recipe.get("description", "")))
        recipe_tokens.update(self._tokens(" ".join(recipe.get("tags", []))))

        if task_tokens and recipe_tokens:
            score += self._overlap_score(task_tokens, recipe_tokens) * 0.45

        fact_tokens = self._fact_tokens(facts)
        recipe_fact_tokens = self._fact_tokens(recipe.get("facts", {}))

        if fact_tokens and recipe_fact_tokens:
            score += self._overlap_score(fact_tokens, recipe_fact_tokens) * 0.45

        if recipe.get("approved") is True:
            score += 0.10

        return min(score, 1.0)

    def _fact_tokens(self, facts: dict) -> set[str]:
        tokens = set()

        for value in facts.values():
            if isinstance(value, str):
                tokens.update(self._tokens(value))
            elif isinstance(value, list):
                tokens.update(self._tokens(" ".join(str(item) for item in value)))
            elif isinstance(value, dict):
                tokens.update(self._fact_tokens(value))

        return tokens

    def _tokens(self, value: str) -> set[str]:
        normalized = str(value).lower()

        normalized = normalized.replace("node.js", "nodejs")

        for char in ["_", "-", "/", ".", ",", ":", "(", ")", "[", "]"]:
            normalized = normalized.replace(char, " ")

        tokens = {
            token.strip()
            for token in normalized.split()
            if token.strip() and len(token.strip()) > 1
        }

        if "nodejs" in tokens:
            tokens.add("node")

        if "backend" in tokens and "api" in tokens:
            tokens.add("backend_api")

        return tokens

    def _overlap_score(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0

        return len(left.intersection(right)) / len(left.union(right))