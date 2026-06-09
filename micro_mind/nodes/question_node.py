import re
from pathlib import Path

from micro_mind.nodes.base_node import BaseNode


class QuestionNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="QuestionNode")

    def execute(self, project_name, project_type: str, target_directory) -> dict:
        normalized_name = normalize_project_name(project_name)
        normalized_type = str(project_type).strip().lower()
        target_path = Path(target_directory)

        if not normalized_name:
            raise ValueError("project_name is required")
        if not normalized_type:
            raise ValueError("project_type is required")
        if not str(target_path).strip():
            raise ValueError("target_directory is required")

        return {
            "project_name": normalized_name,
            "project_type": normalized_type,
            "target_directory": target_path,
        }


def normalize_project_name(project_name) -> str:
    raw_name = str(project_name).strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", raw_name)
    return normalized.strip("_")
