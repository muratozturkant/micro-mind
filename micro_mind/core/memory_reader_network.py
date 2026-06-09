from micro_mind.nodes.memory_read_node import MemoryReadNode
from micro_mind.nodes.memory_summary_node import MemorySummaryNode


class MemoryReaderNetwork:
    def __init__(self) -> None:
        self.memory_read_node = MemoryReadNode()
        self.memory_summary_node = MemorySummaryNode()

    def execute(self, project_root) -> dict:
        memory = self.memory_read_node.run(project_root=project_root)
        return self.memory_summary_node.run(memory)
