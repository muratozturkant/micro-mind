import argparse
import json
from pathlib import Path

from micro_mind.cli.memory_summary import (
    add_memory_summary_parser,
    run_memory_summary,
)
from micro_mind.core.root_planner import RootPlanner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Micro Mind project creation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_project = subparsers.add_parser(
        "create-project",
        help="Create and verify a Micro Mind project directory structure.",
    )
    create_project.add_argument("--name", required=True, help="Project name.")
    create_project.add_argument("--type", required=True, help="Project type.")
    create_project.add_argument(
        "--target",
        required=True,
        type=Path,
        help="Directory that will contain the normalized project folder.",
    )

    add_memory_summary_parser(subparsers)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "create-project":
        planner = RootPlanner()
        result = planner.execute(
            task="create_project_structure",
            project_name=args.name,
            project_type=args.type,
            target_directory=args.target,
        )
        print(json.dumps(result, indent=2))
        return 0 if result["verification_result"]["success"] else 1

    if args.command == "memory-summary":
        return run_memory_summary(args.project)

    parser.error(f"Unsupported command: {args.command}")
    return 1
