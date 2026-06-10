from datetime import datetime, UTC


class ProjectTreeRecord:
    def create(
        self,
        *,
        artifact_id: str,
        path: str,
        artifact_type: str,
        responsibility: str,
        created_by_task: str,
        recipe_id: str | None = None,
        node_id: str | None = None,
        imports: list[str] | None = None,
        depends_on: list[str] | None = None,
        verified_by: list[str] | None = None,
        status: str = "planned",
    ) -> dict:
        return {
            "artifact_id": artifact_id,
            "path": path,
            "artifact_type": artifact_type,
            "responsibility": responsibility,
            "created_by_task": created_by_task,
            "recipe_id": recipe_id,
            "node_id": node_id,
            "imports": imports or [],
            "depends_on": depends_on or [],
            "verified_by": verified_by or [],
            "status": status,
            "created_at": datetime.now(UTC).isoformat(),
        }