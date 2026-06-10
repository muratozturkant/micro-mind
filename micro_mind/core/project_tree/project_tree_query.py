class ProjectTreeQuery:
    def __init__(self, records: list[dict] | None = None):
        self.records = records or []

    def find_by_recipe_id(self, recipe_id: str) -> list[dict]:
        return [
            record
            for record in self.records
            if record.get("recipe_id") == recipe_id
        ]

    def find_by_task_id(self, task_id: str) -> list[dict]:
        return [
            record
            for record in self.records
            if record.get("created_by_task") == task_id
        ]

    def find_by_responsibility(self, responsibility: str) -> list[dict]:
        return [
            record
            for record in self.records
            if record.get("responsibility") == responsibility
        ]

    def find_dependents(self, artifact_id: str) -> list[dict]:
        return [
            record
            for record in self.records
            if artifact_id in record.get("depends_on", [])
        ]

    def find_import_targets(self, path: str) -> list[dict]:
        return [
            record
            for record in self.records
            if path in record.get("imports", [])
        ]