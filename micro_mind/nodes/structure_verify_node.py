from pathlib import Path

from micro_mind.nodes.base_node import BaseNode


class StructureVerifyNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="StructureVerifyNode")

    def execute(
        self,
        project_root,
        required_directories: list[str],
        required_files: list[str],
    ) -> dict:
        root = Path(project_root)
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

        return {
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
