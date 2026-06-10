import json
from pathlib import Path

from micro_mind.nodes.base_node import BaseNode


class MemoryReadNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="MemoryReadNode")

    def execute(self, project_root) -> dict:
        root = Path(project_root)
        micro_mind_root = root / ".micro_mind"
        executions_directory = micro_mind_root / "executions"
        nodes_directory = micro_mind_root / "nodes"

        return {
            "project_root": root,
            "executions": self._read_json_files(executions_directory),
            "node_stats": self._read_named_json_files(nodes_directory),
        }

    def _read_json_files(self, directory: Path) -> list[dict]:
        if not directory.is_dir():
            return []

        return [
            json.loads(file_path.read_text(encoding="utf-8"))
            for file_path in sorted(directory.glob("*.json"))
            if file_path.is_file()
        ]

    def _read_named_json_files(self, directory: Path) -> dict:
        if not directory.is_dir():
            return {}

        return {
            file_path.stem: json.loads(file_path.read_text(encoding="utf-8"))
            for file_path in sorted(directory.glob("*.json"))
            if file_path.is_file()
        }
