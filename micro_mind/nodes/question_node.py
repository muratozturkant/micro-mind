import re
from pathlib import Path

from micro_mind.core.execution_context import ExecutionContext
from micro_mind.nodes.base_node import BaseNode


class QuestionNode(BaseNode):
    def __init__(self) -> None:
        super().__init__(node_name="QuestionNode")

    def execute(
        self,
        project_name=None,
        project_type: str | None = None,
        target_directory=None,
        context: ExecutionContext | None = None,
    ) -> dict:
        source_name = context.project_name if context else project_name
        source_type = context.project_type if context else project_type
        source_target = context.target_directory if context else target_directory

        normalized_name = normalize_project_name(source_name)
        normalized_type = str(source_type).strip().lower()
        target_path = Path(source_target)

        if not normalized_name:
            raise ValueError("project_name is required")
        if not normalized_type:
            raise ValueError("project_type is required")
        if not str(target_path).strip():
            raise ValueError("target_directory is required")

        result = {
            "project_name": normalized_name,
            "project_type": normalized_type,
            "target_directory": target_path,
        }
        if context:
            context.project_name = normalized_name
            context.project_type = normalized_type
            context.target_directory = target_path
        return result


def normalize_project_name(project_name) -> str:
    raw_name = str(project_name).strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", raw_name)
    return normalized.strip("_")
