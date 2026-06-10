class MicroQuestionBuilder:
    def build(self, task: str) -> list[dict]:
        return [
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
                    "For a basic Node.js backend API setup, list the recommended "
                    "project structure as compact JSON only. Max 10 directories "
                    "or files. No descriptions."
                ),
            },
            {
                "question_id": "file_responsibilities",
                "fact_key": "responsibilities",
                "prompt": (
                    "For a basic Node.js backend API setup with Express, list the "
                    "purpose of each file or directory as compact JSON only. Use "
                    "this list: src, src/app.js, src/routes, src/controllers, "
                    "src/middleware, src/config, src/models, package.json, "
                    "README.md, .gitignore. No descriptions longer than 8 words."
                ),
            },
        ]
