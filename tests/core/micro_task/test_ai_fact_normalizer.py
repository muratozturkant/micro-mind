from micro_mind.core.micro_task.ai_fact_normalizer import AIFactNormalizer


def test_ai_fact_normalizer_parses_code_fenced_json():
    content = """```json
["express", "dotenv", "cors"]
```"""

    result = AIFactNormalizer().parse_json(content)

    assert result == ["express", "dotenv", "cors"]


def test_ai_fact_normalizer_normalizes_packages_structure_and_responsibilities():
    normalizer = AIFactNormalizer()

    facts = normalizer.normalize(
        packages=["express", "dotenv", "cors"],
        structure=[
            "src",
            "src/app.js",
            "src/routes",
            "src/controllers",
            "src/middleware",
            "src/config",
            "src/models",
            "package.json",
            "README.md",
            ".gitignore",
        ],
        responsibilities={
            "src": "Application source code directory",
            "src/app.js": "Main application entry point",
            "src/routes": "API endpoint definitions",
            "src/controllers": "Request handling logic",
            "src/middleware": "Request processing utilities",
            "src/config": "Environment and app settings",
            "src/models": "Database schema definitions",
            "package.json": "Project dependencies and scripts",
            "README.md": "Project documentation and setup",
            ".gitignore": "Files excluded from version control",
        },
    )

    assert facts == {
        "dependencies": ["express", "dotenv", "cors"],
        "directories": [
            "src",
            "src/routes",
            "src/controllers",
            "src/middleware",
            "src/config",
            "src/models",
        ],
        "files": ["src/app.js", "package.json", "README.md", ".gitignore"],
        "responsibilities": {
            "src": "Application source code directory",
            "src/app.js": "Main application entry point",
            "src/routes": "API endpoint definitions",
            "src/controllers": "Request handling logic",
            "src/middleware": "Request processing utilities",
            "src/config": "Environment and app settings",
            "src/models": "Database schema definitions",
            "package.json": "Project dependencies and scripts",
            "README.md": "Project documentation and setup",
            ".gitignore": "Files excluded from version control",
        },
    }
