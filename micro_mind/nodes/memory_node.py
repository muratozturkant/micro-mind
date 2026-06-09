import json
from datetime import UTC, datetime
from pathlib import Path

from micro_mind.core.execution_context import ExecutionContext
from micro_mind.nodes.base_node import BaseNode


class MemoryNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="MemoryNode")

    def execute(
        self,
        task: str | None = None,
        project_name: str | None = None,
        project_type: str | None = None,
        target_directory=None,
        result: str | None = None,
        nodes_used: list[str] | None = None,
        duration_seconds: float | None = None,
        created_directories: list[Path] | None = None,
        created_files: list[Path] | None = None,
        verification_result: dict | None = None,
        project_root=None,
        nodes: list[BaseNode] | None = None,
        context: ExecutionContext | None = None,
    ) -> dict:
        if context:
            task = context.task_type
            project_name = context.project_name
            project_type = context.project_type
            target_directory = context.target_directory
            project_root = context.project_root
            created_directories = context.created_directories
            created_files = context.created_files
            verification_result = context.verification_result
            nodes_used = context.metadata["nodes_used"]
            duration_seconds = context.metadata["duration_seconds"]
            result = context.metadata["result"]

        root = Path(project_root)
        executions_directory = root / ".micro_mind" / "executions"
        nodes_directory = root / ".micro_mind" / "nodes"
        executions_directory.mkdir(parents=True, exist_ok=True)
        nodes_directory.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(UTC).isoformat()
        memory = {
            "task_id": context.task_id if context else None,
            "task": task,
            "project_name": project_name,
            "project_type": project_type,
            "target_directory": str(Path(target_directory)),
            "result": result,
            "nodes_used": nodes_used,
            "duration_seconds": round(duration_seconds, 6),
            "created_directories": [str(path) for path in created_directories],
            "created_files": [str(path) for path in created_files],
            "verification_result": verification_result,
            "timestamp": timestamp,
        }

        safe_timestamp = timestamp.replace(":", "-").replace("+", "Z")
        memory_file = executions_directory / f"{safe_timestamp}.json"
        memory_file.write_text(json.dumps(memory, indent=2), encoding="utf-8")

        for node in nodes or []:
            node_file = nodes_directory / f"{node.node_name}.json"
            stats = self._merge_stats(node_file, self._stats_for_storage(node))
            node_file.write_text(json.dumps(stats, indent=2), encoding="utf-8")

        if context:
            context.execution_memory = memory
            context.metadata["memory_file"] = memory_file
        return {"memory_file": memory_file}

    def _stats_for_storage(self, node: BaseNode) -> dict:
        stats = node.to_dict()
        if node is self and self.state == "ACTIVE":
            stats["success_count"] += 1
            total = stats["success_count"] + stats["failure_count"]
            stats["fitness_score"] = stats["success_count"] / total if total else 0.0
            stats["sleep_score"] = 1.0
            stats["state"] = "SLEEPING"
        return stats

    def _merge_stats(self, node_file: Path, current_stats: dict) -> dict:
        if not node_file.exists():
            return current_stats

        previous_stats = json.loads(node_file.read_text(encoding="utf-8"))
        current_stats["activation_count"] += previous_stats.get("activation_count", 0)
        current_stats["success_count"] += previous_stats.get("success_count", 0)
        current_stats["failure_count"] += previous_stats.get("failure_count", 0)

        total = current_stats["success_count"] + current_stats["failure_count"]
        current_stats["fitness_score"] = (
            current_stats["success_count"] / total if total else 0.0
        )
        return current_stats
