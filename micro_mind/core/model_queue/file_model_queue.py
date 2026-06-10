import json
from pathlib import Path
from uuid import uuid4


class FileModelQueue:
    def __init__(self, queue_dir):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self.pending_path = self.queue_dir / "pending.jsonl"
        self.completed_path = self.queue_dir / "completed.jsonl"
        self.failed_path = self.queue_dir / "failed.jsonl"

    def enqueue(self, request: dict) -> dict:
        queued_request = dict(request)
        queued_request.setdefault("request_id", str(uuid4()))
        self._append_jsonl(self.pending_path, queued_request)

        return {
            "status": "queued",
            "request": queued_request,
        }

    def list_pending(self) -> list[dict]:
        return self._read_jsonl(self.pending_path)

    def mark_completed(self, request_id: str, response: dict) -> dict:
        request = self._remove_pending(request_id)
        if request is None:
            return {
                "status": "failed",
                "reason": "request_not_found",
            }

        record = {
            "request": request,
            "response": response,
        }
        self._append_jsonl(self.completed_path, record)

        return {
            "status": "completed",
            "request": request,
            "response": response,
        }

    def mark_failed(self, request_id: str, error: str) -> dict:
        request = self._remove_pending(request_id)
        if request is None:
            return {
                "status": "failed",
                "reason": "request_not_found",
            }

        record = {
            "request": request,
            "error": error,
        }
        self._append_jsonl(self.failed_path, record)

        return {
            "status": "failed",
            "request": request,
            "error": error,
        }

    def _remove_pending(self, request_id):
        pending = self.list_pending()
        matching_request = None
        remaining = []

        for request in pending:
            if request.get("request_id") == request_id and matching_request is None:
                matching_request = request
            else:
                remaining.append(request)

        self._write_jsonl(self.pending_path, remaining)
        return matching_request

    def _read_jsonl(self, path):
        if not path.exists():
            return []

        return [
            json.loads(line)
            for line in path.read_text().splitlines()
            if line.strip()
        ]

    def _append_jsonl(self, path, record):
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, sort_keys=True))
            file.write("\n")

    def _write_jsonl(self, path, records):
        with path.open("w", encoding="utf-8") as file:
            for record in records:
                file.write(json.dumps(record, sort_keys=True))
                file.write("\n")
