import argparse
import json
from pathlib import Path

from micro_mind.core.apply.apply_simulation_runner import ApplySimulationRunner
from micro_mind.core.micro_task.micro_task_simulation_runner import (
    MicroTaskSimulationRunner,
)
from micro_mind.core.project_tree.project_tree_record import ProjectTreeRecord
from micro_mind.core.project_tree.project_tree_store import ProjectTreeStore
from micro_mind.core.recipes.recipe_builder import RecipeBuilder
from micro_mind.core.recipes.recipe_matcher import RecipeMatcher
from micro_mind.core.recipes.recipe_runtime import RecipeRuntime
from micro_mind.core.recipes.recipe_store import RecipeStore
from micro_mind.core.species.local_llama_species import LocalLlamaSpecies


DEFAULT_ENDPOINT = "http://192.168.1.197:18080"
DEFAULT_MODEL = "local-qwen"
DEFAULT_RECIPES_DIR = ".micro_mind/recipes"
DEFAULT_PROJECT_TREE_PATH = ".micro_mind/project_tree.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a simulation-only Micro Mind micro task planning flow."
    )
    parser.add_argument(
        "task",
        nargs="?",
        default="",
        help="Task to simulate, for example: 'Create a basic Node.js backend API'.",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help="OpenAI-compatible local llama.cpp base endpoint.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Local model name sent to the chat completions endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--recipes-dir",
        default=DEFAULT_RECIPES_DIR,
        help="Directory where recipe candidate JSON files are stored.",
    )
    parser.add_argument(
        "--project-tree-path",
        default=DEFAULT_PROJECT_TREE_PATH,
        help="JSONL file where project tree records are stored.",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Print the full report without saving recipe or project tree metadata.",
    )
    return parser


def build_project_tree_records(
    *,
    simulation_report: dict,
    recipe_id: str | None,
) -> list[dict]:
    record_builder = ProjectTreeRecord()
    records = []

    artifact_counter = 1

    for micro_task in simulation_report.get("micro_tasks", []):
        action = micro_task.get("type")
        target = micro_task.get("target")

        if action not in {"create_directory", "create_file"}:
            continue

        artifact_type = "directory" if action == "create_directory" else "file"

        records.append(
            record_builder.create(
                artifact_id=f"artifact_{artifact_counter:04d}",
                path=target,
                artifact_type=artifact_type,
                responsibility=_responsibility_from_target(target),
                created_by_task=micro_task.get("id"),
                recipe_id=recipe_id,
                node_id="micro_task_simulation_runner",
                status="planned",
            )
        )
        artifact_counter += 1

    return records


def _responsibility_from_target(target: str | None) -> str:
    if not target:
        return "unknown"

    normalized = str(target).strip().replace("/", "_").replace(".", "_")
    return normalized.lower()


def load_recipes(recipes_dir: str | Path) -> list[dict]:
    store = RecipeStore(Path(recipes_dir))
    listed = store.list().get("recipes", [])
    recipes = []

    for item in listed:
        recipe_id = item.get("recipe_id")
        if not recipe_id:
            continue

        loaded = store.load(recipe_id)
        if loaded.get("status") == "loaded":
            recipes.append(loaded["recipe"])

    return recipes


def main() -> None:
    args = build_parser().parse_args()

    recipes = load_recipes(args.recipes_dir)
    recipe_match = RecipeMatcher().match(
        task=args.task,
        recipes=[recipe for recipe in recipes if recipe.get("approved") is True],
    )

    ai_used = True
    recipe_reuse_result = None

    if recipe_match.get("status") == "matched":
        recipe = recipe_match["best_match"]["recipe"]
        simulation_report = RecipeRuntime().simulate_from_recipe(
            recipe,
            task=args.task,
        )
        ai_used = False
        recipe_reuse_result = {
            "status": "recipe_reused",
            "recipe_id": recipe.get("recipe_id"),
            "score": recipe_match["best_match"].get("score"),
        }
    else:
        local_ai = LocalLlamaSpecies(
            endpoint=args.endpoint,
            model_name=args.model,
            timeout=args.timeout,
        )
        micro_task_runner = MicroTaskSimulationRunner(local_ai=local_ai)
        simulation_report = micro_task_runner.run(args.task)

    apply_report = None
    recipe_candidate = None
    recipe_save_result = None
    project_tree_records = []
    project_tree_store_results = []

    if simulation_report.get("status") == "simulated":
        apply_report = ApplySimulationRunner().run(simulation_report)

        if ai_used:
            recipe_candidate = RecipeBuilder().build_candidate(
                task=args.task,
                simulation_report=simulation_report,
                apply_simulation_report=apply_report,
            )
            recipe_id = recipe_candidate.get("recipe_id")
        else:
            recipe_id = simulation_report.get("recipe_id")

        project_tree_records = build_project_tree_records(
            simulation_report=simulation_report,
            recipe_id=recipe_id,
        )

        if not args.no_save and recipe_candidate and recipe_candidate.get("status") == "recipe_candidate_created":
            recipe_save_result = RecipeStore(Path(args.recipes_dir)).save(
                recipe_candidate["recipe"]
            )

            project_tree_store = ProjectTreeStore(Path(args.project_tree_path))
            project_tree_store_results = [
                project_tree_store.append(record) for record in project_tree_records
            ]

    result = {
        "status": "full_simulation_completed"
        if simulation_report.get("status") == "simulated"
        else simulation_report.get("status"),
        "task": args.task,
        "ai_used": ai_used,
        "recipe_match": recipe_match,
        "recipe_reuse_result": recipe_reuse_result,
        "simulation_report": simulation_report,
        "apply_report": apply_report,
        "recipe_candidate": recipe_candidate,
        "recipe_save_result": recipe_save_result,
        "project_tree_records": project_tree_records,
        "project_tree_store_results": project_tree_store_results,
        "saved": not args.no_save,
        "will_write_project_files": False,
        "will_run_commands": False,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()