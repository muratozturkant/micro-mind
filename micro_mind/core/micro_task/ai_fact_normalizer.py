import json
from pathlib import PurePosixPath


class AIFactNormalizer:
    def parse_json(self, value):
        if not isinstance(value, str):
            return value

        content = value.strip()
        if content.startswith("```"):
            lines = content.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        return json.loads(content)

    def normalize(self, packages=None, structure=None, responsibilities=None) -> dict:
        packages = self.parse_json(packages or [])
        structure = self.parse_json(structure or [])
        responsibilities = self.parse_json(responsibilities or {})

        return {
            "dependencies": self._normalize_list(packages),
            "directories": self._normalize_structure(structure, want="directory"),
            "files": self._normalize_structure(structure, want="file"),
            "responsibilities": self._normalize_responsibilities(responsibilities),
        }

    def _normalize_list(self, values):
        normalized = []
        for value in values:
            if not isinstance(value, str):
                continue
            cleaned = value.strip()
            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)
        return normalized

    def _normalize_structure(self, values, want):
        normalized = []
        for value in values:
            if not isinstance(value, str):
                continue
            cleaned = value.strip().strip("/")
            if not cleaned:
                continue

            path = PurePosixPath(cleaned)
            kind = (
                "file"
                if path.suffix or path.name.startswith(".")
                else "directory"
            )
            if kind == want and cleaned not in normalized:
                normalized.append(cleaned)
        return normalized

    def _normalize_responsibilities(self, values):
        if not isinstance(values, dict):
            return {}

        return {
            str(path): str(purpose)
            for path, purpose in values.items()
            if str(path).strip() and str(purpose).strip()
        }
