


from pathlib import Path
from micro_mind.core.work_tree_logger import WorkTreeLogger


class ProjectStructureNode:
    name = "ProjectStructureNode"

    def execute(self, context: dict | None = None) -> dict:
        context = context or {}
        project_name = context.get("project_name")
        base_path = context.get("base_path")
        work_tree_log_path = context.get("work_tree_log_path")
        logger = WorkTreeLogger(work_tree_log_path) if work_tree_log_path else None

        if not project_name:
            return {
                "status": "failed",
                "node_name": self.name,
                "reason": "missing_project_name",
            }

        if not base_path:
            return {
                "status": "failed",
                "node_name": self.name,
                "reason": "missing_base_path",
            }

        project_slug = self._slugify(project_name)
        project_path = Path(base_path) / project_slug

        directories = [
            project_path / "frontend",
            project_path / "backend",
            project_path / "database",
            project_path / "docs",
        ]

        if logger:
            for directory in directories:
                logger.log(
                    node_name=self.name,
                    action="create_directory",
                    target_path=str(directory),
                    status="planned",
                    metadata={
                        "project_name": project_name,
                        "project_slug": project_slug,
                    },
                )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            if logger:
                logger.log(
                    node_name=self.name,
                    action="create_directory",
                    target_path=str(directory),
                    status="executed",
                    metadata={
                        "project_name": project_name,
                        "project_slug": project_slug,
                    },
                )

        state_file = project_path / "PROJECT_STATE.md"
        rules_file = project_path / "DEVELOPMENT_RULES.md"

        files = [state_file, rules_file]

        if logger:
            for file_path in files:
                logger.log(
                    node_name=self.name,
                    action="write_file",
                    target_path=str(file_path),
                    status="planned",
                    metadata={
                        "project_name": project_name,
                        "project_slug": project_slug,
                    },
                )

        state_file.write_text(
            f"# {project_name} Project State\n\nStatus: initialized\n",
            encoding="utf-8",
        )
        rules_file.write_text(
            "# Development Rules\n\n- Work incrementally.\n- Verify changes after each step.\n",
            encoding="utf-8",
        )

        if logger:
            for file_path in files:
                logger.log(
                    node_name=self.name,
                    action="write_file",
                    target_path=str(file_path),
                    status="executed",
                    metadata={
                        "project_name": project_name,
                        "project_slug": project_slug,
                    },
                )

        return {
            "status": "executed",
            "node_name": self.name,
            "project_name": project_name,
            "project_slug": project_slug,
            "project_path": str(project_path),
            "created_directories": [str(directory) for directory in directories],
            "created_files": [
                str(state_file),
                str(rules_file),
            ],
            "work_tree_log_path": str(work_tree_log_path) if work_tree_log_path else None,
        }

    def _slugify(self, value: str) -> str:
        return value.strip().lower().replace(" ", "_")