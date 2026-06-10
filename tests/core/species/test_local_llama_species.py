import json

from micro_mind.core.species.local_llama_species import LocalLlamaSpecies


class FakeHTTPResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_local_llama_species_sends_enable_thinking_false_and_parses_json():
    captured = {}

    def fake_http_client(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["headers"] = dict(request.header_items())
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return FakeHTTPResponse({
            "choices": [
                {
                    "message": {
                        "content": json.dumps({
                            "task_type": "backend_api",
                            "confidence": 0.91,
                        }),
                    },
                },
            ],
        })

    species = LocalLlamaSpecies(
        endpoint="http://localhost:8080",
        model_name="local-model",
        timeout=7,
        http_client=fake_http_client,
    )

    result = species.classify_task("Create a Node.js API")

    assert captured["url"] == "http://localhost:8080/v1/chat/completions"
    assert captured["timeout"] == 7
    assert captured["body"]["model"] == "local-model"
    assert captured["body"]["temperature"] == 0
    assert captured["body"]["max_tokens"] == 128
    assert captured["body"]["chat_template_kwargs"] == {"enable_thinking": False}
    assert "JSON" in captured["body"]["messages"][0]["content"]
    assert result["status"] == "completed"
    assert result["parsed_response"] == {
        "task_type": "backend_api",
        "confidence": 0.91,
    }
    assert result["raw_response"]["choices"][0]["message"]["content"]
    assert result["error"] is None


def test_local_llama_species_returns_failed_for_invalid_json_content():
    def fake_http_client(request, timeout):
        return FakeHTTPResponse({
            "choices": [
                {
                    "message": {
                        "content": "not json",
                    },
                },
            ],
        })

    species = LocalLlamaSpecies(
        endpoint="http://localhost:8080",
        model_name="local-model",
        http_client=fake_http_client,
    )

    result = species.classify_task("Create a project")

    assert result["status"] == "failed"
    assert result["parsed_response"] is None
    assert result["raw_response"]["choices"][0]["message"]["content"] == "not json"
    assert "JSON" in result["error"]
