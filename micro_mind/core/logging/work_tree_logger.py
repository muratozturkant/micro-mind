import json
from datetime import datetime, timezone
from pathlib import Path


class WorkTreeLogger:
    def __init__(self, log_path: str | Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        *,
        node_name: str,
        action: str,
        target_path: str,
        status: str,
        metadata: dict | None = None,
    ) -> dict:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "node_name": node_name,
            "action": action,
            "target_path": target_path,
            "status": status,
            "metadata": metadata or {},
        }

        with self.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")

        return entry

    def read_entries(self) -> list[dict]:
        if not self.log_path.exists():
            return []

        entries = []
        with self.log_path.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                clean_line = line.strip()
                if clean_line:
                    entries.append(json.loads(clean_line))

        return entries
