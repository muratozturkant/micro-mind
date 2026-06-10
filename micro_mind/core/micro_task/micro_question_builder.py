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
        ]
