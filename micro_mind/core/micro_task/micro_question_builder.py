class MicroQuestionBuilder:
    DEFAULT_QUESTIONS = [
        {
            "question_id": "base_packages",
            "fact_key": "packages",
            "prompt": (
                "For a basic Node.js backend API setup, list the required "
                "npm packages as compact JSON only. No descriptions. No Redis. "
                "No database-specific packages unless essential."
            ),
        },
        {
            "question_id": "project_structure",
            "fact_key": "structure",
            "prompt": (
                "For a basic Node.js backend API setup, list only 7 essential "
                "project paths as compact JSON only. Include src/app.js, "
                "routes, controllers, config, package.json. No descriptions."
            ),
        },
        {
            "question_id": "file_responsibilities",
            "fact_key": "responsibilities",
            "prompt": (
                "Map these Node.js API paths to max 3-word purposes as compact "
                "JSON only: src, src/app.js, src/routes, src/controllers, "
                "src/config, package.json. No extra keys."
            ),
        },
        {
            "question_id": "task_specific_files",
            "fact_key": "task_specific_files",
            "prompt": (
                "For this software task, list only task-specific files or paths "
                "that are not part of a generic Node.js backend template. "
                "Return compact JSON only as an array. No descriptions. "
                "Examples: health.route.js, auth.route.js, auth.middleware.js."
            ),
        },
    ]

    def build(self, task: str, question_plan: list[dict] | None = None) -> list[dict]:
        if not task or not task.strip():
            return []

        if question_plan:
            normalized_questions = self.normalize_question_plan(question_plan)
            if normalized_questions:
                return normalized_questions

        return [question.copy() for question in self.DEFAULT_QUESTIONS]

    def build_question_generation_prompt(self, task: str) -> str:
        return (
            "Create micro questions for this software task. "
            "Return compact JSON array only. "
            "Each item must include question_id, fact_key, prompt. "
            "Each prompt must ask for one small fact only. "
            "Do not ask for code generation. "
            "Do not ask broad architecture questions. "
            "Prefer package list, project paths, file purpose, imports, wiring, verification. "
            f"Task: {task}"
        )

    def normalize_question_plan(self, question_plan: list[dict]) -> list[dict]:
        questions = []

        for index, item in enumerate(question_plan, start=1):
            if not isinstance(item, dict):
                continue

            prompt = item.get("prompt") or item.get("question")
            fact_key = item.get("fact_key") or item.get("key") or item.get("purpose")
            question_id = item.get("question_id") or item.get("id") or f"generated_{index}"

            if not prompt or not fact_key:
                continue

            questions.append(
                {
                    "question_id": self._slug(question_id),
                    "fact_key": self._slug(fact_key),
                    "prompt": str(prompt).strip(),
                }
            )

        return questions

    def _slug(self, value: str) -> str:
        return str(value).strip().lower().replace(" ", "_").replace("-", "_")
