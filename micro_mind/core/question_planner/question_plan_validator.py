import re


class QuestionPlanValidator:
    FORBIDDEN_PROMPT_PHRASES = (
        "write the full code",
        "generate the whole app",
        "create complete project",
    )

    def validate(self, question_plan) -> dict:
        if not isinstance(question_plan, list):
            return self._rejected("invalid_question_plan")

        if not question_plan:
            return self._rejected("empty_question_plan")

        questions = []
        for item in question_plan:
            if not isinstance(item, dict):
                return self._rejected("invalid_question")

            question_id = item.get("question_id") or item.get("id")
            fact_key = item.get("fact_key") or item.get("key") or item.get("purpose")
            prompt = item.get("prompt") or item.get("question")

            if not question_id or not fact_key or not prompt:
                return self._rejected("missing_required_fields")

            prompt = str(prompt).strip()
            lower_prompt = prompt.lower()

            if len(prompt) > 240:
                return self._rejected("prompt_too_long")

            if "json" not in lower_prompt:
                return self._rejected("prompt_must_request_json")

            if any(phrase in lower_prompt for phrase in self.FORBIDDEN_PROMPT_PHRASES):
                return self._rejected("prompt_requests_full_code_generation")

            questions.append({
                "question_id": self._slug(question_id),
                "fact_key": self._slug(fact_key),
                "prompt": prompt,
            })

        return {
            "status": "accepted",
            "questions": questions,
        }

    def _slug(self, value):
        slug = str(value).strip().lower()
        slug = re.sub(r"[\s-]+", "_", slug)
        slug = re.sub(r"[^a-z0-9_]", "", slug)
        slug = re.sub(r"_+", "_", slug)
        return slug.strip("_")

    def _rejected(self, reason):
        return {
            "status": "rejected",
            "reason": reason,
            "questions": [],
        }
