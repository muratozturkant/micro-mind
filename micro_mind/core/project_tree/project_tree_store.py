import json
from pathlib import Path


class ProjectTreeStore:
    def __init__(self, store_path: str | Path):
        self.store_path = Path(store_path)

    def append(self, record: dict) -> dict:
        self.store_path.parent.mkdir(parents=True, exist_ok=True)

        with self.store_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")

        return {
            "status": "stored",
            "artifact_id": record.get("artifact_id"),
        }

    def list(self) -> list[dict]:
        if not self.store_path.exists():
            return []

        records = []

        with self.store_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()

                if not line:
                    continue

                records.append(json.loads(line))

        return records

    def find_by_path(self, path: str) -> dict | None:
        for record in self.list():
            if record.get("path") == path:
                return record

        return None

    def find_by_artifact_id(self, artifact_id: str) -> dict | None:
        for record in self.list():
            if record.get("artifact_id") == artifact_id:
                return record

        return None