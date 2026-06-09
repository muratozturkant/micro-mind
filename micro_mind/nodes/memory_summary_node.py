from pathlib import Path

from micro_mind.nodes.base_node import BaseNode


class MemorySummaryNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="MemorySummaryNode")

    def execute(self, memory: dict) -> dict:
        project_root = Path(memory["project_root"])
        executions = memory["executions"]
        node_stats = memory["node_stats"]
        durations = [
            execution.get("duration_seconds", 0)
            for execution in executions
            if isinstance(execution.get("duration_seconds", 0), (int, float))
        ]

        return {
            "project_root": str(project_root),
            "total_executions": len(executions),
            "successful_executions": self._count_results(executions, "success"),
            "failed_executions": self._count_results(executions, "failure"),
            "last_execution": self._last_execution_timestamp(executions),
            "tasks_seen": sorted(
                {
                    execution["task"]
                    for execution in executions
                    if execution.get("task")
                }
            ),
            "node_stats": node_stats,
            "most_used_nodes": self._most_used_nodes(node_stats),
            "average_duration_seconds": (
                round(sum(durations) / len(durations), 6) if durations else 0.0
            ),
        }

    def _count_results(self, executions: list[dict], result: str) -> int:
        return sum(1 for execution in executions if execution.get("result") == result)

    def _last_execution_timestamp(self, executions: list[dict]) -> str | None:
        timestamps = [
            execution["timestamp"]
            for execution in executions
            if execution.get("timestamp")
        ]
        return max(timestamps) if timestamps else None

    def _most_used_nodes(self, node_stats: dict) -> list[dict]:
        nodes = [
            {
                "node_name": stats.get("node_name", node_name),
                "activation_count": stats.get("activation_count", 0),
            }
            for node_name, stats in node_stats.items()
        ]
        return sorted(
            nodes,
            key=lambda stats: (-stats["activation_count"], stats["node_name"]),
        )
