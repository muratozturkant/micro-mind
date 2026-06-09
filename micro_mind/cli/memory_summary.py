import json
from pathlib import Path

from micro_mind.core.root_planner import RootPlanner


def add_memory_summary_parser(subparsers) -> None:
    memory_summary = subparsers.add_parser(
        "memory-summary",
        help="Read and summarize Micro Mind memory for a project.",
    )
    memory_summary.add_argument(
        "--project",
        required=True,
        type=Path,
        help="Project root that contains .micro_mind memory.",
    )


def run_memory_summary(project: Path) -> int:
    planner = RootPlanner()
    result = planner.execute(
        task="memory_summary",
        project_root=project,
    )
    print(json.dumps(result, indent=2))
    return 0
