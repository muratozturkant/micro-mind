from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4


@dataclass
class ExecutionContext:
    task_type: str
    task_id: str = field(default_factory=lambda: str(uuid4()))
    project_name: str | None = None
    project_type: str | None = None
    target_directory: Path | None = None
    project_root: Path | None = None
    created_directories: list[Path] = field(default_factory=list)
    created_files: list[Path] = field(default_factory=list)
    verification_result: dict = field(default_factory=dict)
    execution_memory: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
