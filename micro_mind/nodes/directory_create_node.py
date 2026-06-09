from pathlib import Path

from micro_mind.nodes.base_node import BaseNode


REQUIRED_DIRECTORIES = [
    "frontend",
    "backend",
    "database",
    "docs",
    ".micro_mind",
    ".micro_mind/executions",
    ".micro_mind/nodes",
]

REQUIRED_FILES = ["PROJECT_STATE.md", "DEVELOPMENT_RULES.md"]


class DirectoryCreateNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="DirectoryCreateNode")

    def execute(self, project_data: dict) -> dict:
        target_directory = Path(project_data["target_directory"])
        project_root = target_directory / project_data["project_name"]
        created_directories: list[Path] = []
        created_files: list[Path] = []

        for relative_path in REQUIRED_DIRECTORIES:
            directory = project_root / relative_path
            if not directory.exists():
                created_directories.append(directory)
            directory.mkdir(parents=True, exist_ok=True)

        for relative_path in REQUIRED_FILES:
            file_path = project_root / relative_path
            if not file_path.exists():
                file_path.write_text("", encoding="utf-8")
                created_files.append(file_path)

        return {
            "project_root": project_root,
            "required_directories": REQUIRED_DIRECTORIES,
            "required_files": REQUIRED_FILES,
            "created_directories": created_directories,
            "created_files": created_files,
        }
