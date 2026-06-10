import json

from micro_mind.core.model_queue.file_model_queue import FileModelQueue


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_file_model_queue_enqueues_and_lists_pending_jsonl(tmp_path):
    queue = FileModelQueue(tmp_path)

    result = queue.enqueue({"task": "Create API"})

    assert result["status"] == "queued"
    assert result["request"]["task"] == "Create API"
    assert result["request"]["request_id"]
    assert queue.list_pending() == [result["request"]]
    assert read_jsonl(tmp_path / "pending.jsonl") == [result["request"]]


def test_file_model_queue_marks_completed_and_failed_jsonl(tmp_path):
    queue = FileModelQueue(tmp_path)
    completed = queue.enqueue({"task": "Create API"})["request"]
    failed = queue.enqueue({"task": "Create app"})["request"]

    completed_result = queue.mark_completed(
        completed["request_id"],
        {"task_type": "backend_api"},
    )
    failed_result = queue.mark_failed(failed["request_id"], "invalid_json")

    assert completed_result["status"] == "completed"
    assert failed_result["status"] == "failed"
    assert queue.list_pending() == []
    assert read_jsonl(tmp_path / "completed.jsonl") == [
        {
            "request": completed,
            "response": {"task_type": "backend_api"},
        },
    ]
    assert read_jsonl(tmp_path / "failed.jsonl") == [
        {
            "request": failed,
            "error": "invalid_json",
        },
    ]
