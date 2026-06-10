

from micro_mind.nodes.project_structure_node import ProjectStructureNode


class BaseExecutableNode:
    name = "BaseExecutableNode"

    def execute(self, context: dict | None = None) -> dict:
        return {
            "status": "executed",
            "node_name": self.name,
            "context": context or {},
        }


class TaskPlannerExecutableNode(BaseExecutableNode):
    name = "TaskPlannerNode"


class MemoryExecutableNode(BaseExecutableNode):
    name = "MemoryNode"


class HumanGuidanceExecutableNode(BaseExecutableNode):
    name = "HumanGuidanceNode"

    def execute(self, context: dict | None = None) -> dict:
        return {
            "status": "waiting_for_human_guidance",
            "node_name": self.name,
            "context": context or {},
        }


class NodeRegistry:
    def __init__(self):
        self._nodes = {
            "TaskPlannerNode": TaskPlannerExecutableNode,
            "MemoryNode": MemoryExecutableNode,
            "ProjectStructureNode": ProjectStructureNode,
            "HumanGuidanceNode": HumanGuidanceExecutableNode,
        }

    def get(self, node_name: str):
        node_class = self._nodes.get(node_name)

        if node_class is None:
            return None

        return node_class()

    def has(self, node_name: str) -> bool:
        return node_name in self._nodes