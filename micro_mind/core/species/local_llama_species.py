import json
from urllib import request as urllib_request


class LocalLlamaSpecies:
    def __init__(self, endpoint, model_name, timeout=30, http_client=None):
        self.endpoint = endpoint.rstrip("/")
        self.model_name = model_name
        self.timeout = timeout
        self.http_client = http_client or self._default_http_client

    @staticmethod
    def _extract_json_content(content: str) -> str:
        stripped_content = content.strip()

        if stripped_content.startswith("```"):
            lines = stripped_content.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            stripped_content = "\n".join(lines).strip()

        return stripped_content

    def classify_task(
        self,
        task: str,
        max_tokens: int = 256,
    ) -> dict:
        payload = {
            "model": self.model_name,
            "temperature": 0,
            "max_tokens": max_tokens,
            "chat_template_kwargs": {
                "enable_thinking": False,
            },
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a local advisor for Micro Mind. "
                        "Return JSON only. Do not execute workflows. "
                        "Do not apply changes."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Classify this task and return compact JSON only: "
                        f"{task}"
                    ),
                },
            ],
        }

        try:
            raw_response = self._post_chat_completions(payload)
            content = raw_response["choices"][0]["message"]["content"]
            json_content = self._extract_json_content(content)
            parsed_response = json.loads(json_content)
        except Exception as error:
            return {
                "status": "failed",
                "parsed_response": None,
                "raw_response": locals().get("raw_response"),
                "raw_content": locals().get("content"),
                "json_content": locals().get("json_content"),
                "error": f"JSON classification failed: {error}",
            }

        return {
            "status": "completed",
            "parsed_response": parsed_response,
            "raw_response": raw_response,
            "error": None,
        }

    def _post_chat_completions(self, payload):
        body = json.dumps(payload).encode("utf-8")
        request = urllib_request.Request(
            f"{self.endpoint}/v1/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with self.http_client(request, self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _default_http_client(request, timeout):
        return urllib_request.urlopen(request, timeout=timeout)
