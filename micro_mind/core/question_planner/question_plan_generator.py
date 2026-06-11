class QuestionPlanGenerator:
    def build_prompt(self, task: str) -> str:
        if not isinstance(task, str) or not task.strip():
            return ""

        return (
            "Create a micro question plan for this software task. "
            "Return compact JSON only as a JSON array of objects. "
            "Each object must include question_id, fact_key, prompt. "
            "Each generated prompt must ask for one small fact only. "
            "do not ask for code generation. "
            "do not ask broad architecture questions. "
            "Prefer package list, project paths, file responsibilities, "
            "task-specific files, imports, wiring, verification. "
            f"Task: {task.strip()}"
        )
