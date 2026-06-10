class AISuggestionValidator:
    ALLOWED_TASK_TYPES = {
        "backend_api",
        "frontend_app",
        "mobile_app",
        "project_setup",
        "unknown",
    }

    def validate(self, parsed_response: dict) -> dict:
        if not isinstance(parsed_response, dict):
            return {
                "status": "rejected",
                "reason": "invalid_response",
            }

        confidence = parsed_response.get("confidence")
        if confidence is not None:
            if not isinstance(confidence, (int, float)):
                return {
                    "status": "rejected",
                    "reason": "invalid_confidence",
                }

            if confidence < 0.70:
                return {
                    "status": "requires_human_guidance",
                    "reason": "confidence_below_threshold",
                }

        task_type = parsed_response.get("task_type")
        if task_type is not None and task_type not in self.ALLOWED_TASK_TYPES:
            return {
                "status": "rejected",
                "reason": "unknown_task_type",
            }

        return {
            "status": "accepted",
            "reason": None,
        }
