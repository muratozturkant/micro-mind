from pathlib import Path

from micro_mind.core.execution_context import ExecutionContext
from micro_mind.nodes.base_node import BaseNode


class StructureVerifyNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="StructureVerifyNode")

    def execute(
        self,
        project_root=None,
        required_directories: list[str] | None = None,
        required_files: list[str] | None = None,
        context: ExecutionContext | None = None,
    ) -> dict:
        if context:
            root = Path(context.project_root)
            required_directories = context.metadata["required_directories"]
            required_files = context.metadata["required_files"]
        else:
            root = Path(project_root)
            required_directories = required_directories or []
            required_files = required_files or []

        missing_directories = [
            relative_path
            for relative_path in required_directories
            if not (root / relative_path).is_dir()
        ]
        missing_files = [
            relative_path
            for relative_path in required_files
            if not (root / relative_path).is_file()
        ]

        result = {
            "success": not missing_directories and not missing_files,
            "missing_directories": missing_directories,
            "missing_files": missing_files,
            "directories": {
                relative_path: (root / relative_path).is_dir()
                for relative_path in required_directories
            },
            "files": {
                relative_path: (root / relative_path).is_file()
                for relative_path in required_files
            },
        }
        if context:
            context.verification_result = result
        return result
