from pathlib import Path

from micro_mind.core.planning.task_planner_network import TaskPlannerNetwork
from micro_mind.nodes.project_structure.project_structure_node import ProjectStructureNode


class ProjectCreationExecutionNetwork:
    DEFAULT_BASE_PATH = "/Volumes/HDD/MM_projects"
    FORBIDDEN_BASE_PATHS = {
        "/Volumes/HDD/projects",
    }

    def __init__(self):
        self.task_planner_network = TaskPlannerNetwork()
        self.project_structure_node = ProjectStructureNode()

    def run(self, *, task: str, project_name: str, base_path: str | None = None) -> dict:
        base_path = base_path or self.DEFAULT_BASE_PATH

        if base_path in self.FORBIDDEN_BASE_PATHS:
            return {
                "status": "failed",
                "reason": "forbidden_base_path",
                "base_path": base_path,
                "allowed_base_path": self.DEFAULT_BASE_PATH,
            }

        task_plan_result = self.task_planner_network.run(task)

        if task_plan_result.get("status") != "planned":
            return {
                "status": "waiting_for_human_guidance",
                "reason": task_plan_result.get("reason"),
                "task_plan_result": task_plan_result,
            }

        project_slug = self.project_structure_node._slugify(project_name)
        project_path = Path(base_path) / project_slug
        work_tree_log_path = project_path / ".micro_mind" / "work_tree.jsonl"

        project_structure_result = self.project_structure_node.execute({
            "project_name": project_name,
            "base_path": base_path,
            "work_tree_log_path": str(work_tree_log_path),
        })

        return {
            "status": "executed",
            "task": task,
            "project_name": project_name,
            "project_path": project_structure_result.get("project_path"),
            "task_plan_result": task_plan_result,
            "project_structure_result": project_structure_result,
            "work_tree_log_path": str(work_tree_log_path),
        }
