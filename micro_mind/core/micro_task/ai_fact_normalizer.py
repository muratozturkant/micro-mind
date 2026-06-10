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

    def normalize(
        self,
        packages=None,
        structure=None,
        responsibilities=None,
        task_specific_files=None,
    ) -> dict:
        packages = self.parse_json(packages or [])
        structure = self.parse_json(structure or [])
        responsibilities = self.parse_json(responsibilities or {})
        task_specific_files = self.parse_json(task_specific_files or [])

        package_values = self._extract_package_values(packages)
        structure_values = self._extract_structure_values(structure)
        responsibility_values = self._extract_responsibility_values(responsibilities)
        task_specific_file_values = self._extract_structure_values(task_specific_files)

        return {
            "dependencies": self._normalize_list(package_values),
            "directories": self._normalize_structure(structure_values, want="directory"),
            "files": self._normalize_structure(structure_values, want="file"),
            "task_specific_files": self._normalize_structure(
                task_specific_file_values,
                want="file",
            ),
            "responsibilities": self._normalize_responsibilities(responsibility_values),
        }

    def _extract_package_values(self, value):
        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            for key in ("packages", "dependencies", "required_packages", "npm_packages"):
                items = value.get(key)
                if isinstance(items, list):
                    return items

        return []

    def _extract_structure_values(self, value):
        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            for key in (
                "structure",
                "project_structure",
                "files_and_directories",
                "paths",
                "items",
            ):
                items = value.get(key)
                if isinstance(items, list):
                    return items

            directories = value.get("directories")
            files = value.get("files")
            combined = []

            if isinstance(directories, list):
                combined.extend(directories)

            if isinstance(files, list):
                combined.extend(files)

            if combined:
                return combined

        return []

    def _extract_responsibility_values(self, value):
        if not isinstance(value, dict):
            return {}

        content = value.get("content")
        if isinstance(content, dict):
            return content

        responsibilities = value.get("responsibilities")
        if isinstance(responsibilities, dict):
            return responsibilities

        return value

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
