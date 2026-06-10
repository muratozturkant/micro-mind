

import argparse
import json

from micro_mind.core.micro_task.micro_task_simulation_runner import (
    MicroTaskSimulationRunner,
)
from micro_mind.core.species.local_llama_species import LocalLlamaSpecies


DEFAULT_ENDPOINT = "http://192.168.1.197:18080"
DEFAULT_MODEL = "local-qwen"


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
        help="OpenAI-compatible local llama.cpp chat completions endpoint.",
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
    return parser


def main() -> None:
    args = build_parser().parse_args()

    local_ai = LocalLlamaSpecies(
        endpoint=args.endpoint,
        model_name=args.model,
        timeout=args.timeout,
    )
    runner = MicroTaskSimulationRunner(local_ai=local_ai)

    result = runner.run(args.task)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()