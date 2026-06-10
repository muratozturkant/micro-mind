from datetime import datetime, UTC


class RecipeBuilder:
    def build_candidate(
        self,
        *,
        task: str,
        simulation_report: dict | None,
        apply_simulation_report: dict | None = None,
        recipe_id: str | None = None,
        title: str | None = None,
        task_family: str | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        if not task or not task.strip():
            return {
                "status": "failed",
                "reason": "missing_task",
            }

        if not simulation_report:
            return {
                "status": "failed",
                "reason": "missing_simulation_report",
            }

        if simulation_report.get("status") != "simulated":
            return {
                "status": "failed",
                "reason": "simulation_not_successful",
                "source_status": simulation_report.get("status"),
            }

        if apply_simulation_report and apply_simulation_report.get("status") not in {
            "apply_ready_for_human_approval",
            "apply_simulated",
        }:
            return {
                "status": "failed",
                "reason": "apply_simulation_not_successful",
                "source_status": apply_simulation_report.get("status"),
            }

        candidate_recipe_id = recipe_id or self._build_recipe_id(task)
        candidate_task_family = task_family or self._infer_task_family(simulation_report)
        candidate_tags = tags or self._build_tags(task, simulation_report)

        recipe = {
            "recipe_id": candidate_recipe_id,
            "status": "candidate",
            "approved": False,
            "task_family": candidate_task_family,
            "title": title or self._title_from_task(task),
            "description": task.strip(),
            "tags": candidate_tags,
            "facts": simulation_report.get("facts", {}),
            "micro_tasks": simulation_report.get("micro_tasks", []),
            "questions": simulation_report.get("questions", []),
            "simulation": {
                "status": simulation_report.get("status"),
                "summary": simulation_report.get("simulation", {}),
            },
            "apply_simulation": apply_simulation_report or {},
            "verification": {
                "status": "pending",
            },
            "source": {
                "created_from": "simulation_report",
                "created_at": datetime.now(UTC).isoformat(),
                "requires_human_approval": True,
            },
        }

        return {
            "status": "recipe_candidate_created",
            "recipe_id": candidate_recipe_id,
            "recipe": recipe,
        }

    def _build_recipe_id(self, task: str) -> str:
        slug = task.strip().lower()

        for char in [".", ",", ":", ";", "'", '"', "(", ")", "[", "]", "/", "\\"]:
            slug = slug.replace(char, " ")

        slug = "_".join(part for part in slug.split() if part)

        return f"{slug}_v1"

    def _title_from_task(self, task: str) -> str:
        return task.strip()[:120]

    def _infer_task_family(self, simulation_report: dict) -> str:
        facts = simulation_report.get("facts", {})
        dependencies = set(facts.get("dependencies", []))

        if "express" in dependencies:
            return "nodejs_backend_api"

        return "unknown"

    def _build_tags(self, task: str, simulation_report: dict) -> list[str]:
        tags = set()
        facts = simulation_report.get("facts", {})

        for dependency in facts.get("dependencies", []):
            tags.add(str(dependency).lower())

        task_text = task.lower()

        if "node" in task_text or "nodejs" in task_text or "node.js" in task_text:
            tags.add("nodejs")

        if "backend" in task_text:
            tags.add("backend_api")

        return sorted(tags)
