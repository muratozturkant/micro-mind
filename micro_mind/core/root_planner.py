from micro_mind.core.memory_reader_network import MemoryReaderNetwork
from micro_mind.core.project_creation.project_create_network import ProjectCreateNetwork


class RootPlanner:
    def execute(
        self,
        task: str,
        project_name=None,
        project_type: str | None = None,
        target_directory=None,
        project_root=None,
    ) -> dict:
        if task == "memory_summary":
            network = MemoryReaderNetwork()
            return network.execute(project_root=project_root)

        if task != "create_project_structure":
            raise ValueError(f"Unsupported task: {task}")

        network = ProjectCreateNetwork()
        return network.execute(
            task=task,
            project_name=project_name,
            project_type=project_type,
            target_directory=target_directory,
        )
