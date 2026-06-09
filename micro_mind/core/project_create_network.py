from time import perf_counter

from micro_mind.nodes.directory_create_node import DirectoryCreateNode
from micro_mind.nodes.memory_node import MemoryNode
from micro_mind.nodes.question_node import QuestionNode
from micro_mind.nodes.structure_verify_node import StructureVerifyNode


class ProjectCreateNetwork:
    def __init__(self) -> None:
        self.question_node = QuestionNode()
        self.directory_create_node = DirectoryCreateNode()
        self.structure_verify_node = StructureVerifyNode()
        self.memory_node = MemoryNode()
        self.nodes = [
            self.question_node,
            self.directory_create_node,
            self.structure_verify_node,
            self.memory_node,
        ]

    def execute(self, task: str, project_name, project_type: str, target_directory) -> dict:
        started_at = perf_counter()
        nodes_used: list[str] = []

        question_result = self.question_node.run(
            project_name=project_name,
            project_type=project_type,
            target_directory=target_directory,
        )
        nodes_used.append(self.question_node.node_name)

        directory_result = self.directory_create_node.run(question_result)
        nodes_used.append(self.directory_create_node.node_name)

        verification_result = self.structure_verify_node.run(
            project_root=directory_result["project_root"],
            required_directories=directory_result["required_directories"],
            required_files=directory_result["required_files"],
        )
        nodes_used.append(self.structure_verify_node.node_name)

        result = "success" if verification_result["success"] else "failure"
        duration_seconds = perf_counter() - started_at

        memory_result = self.memory_node.run(
            task=task,
            project_name=question_result["project_name"],
            project_type=question_result["project_type"],
            target_directory=question_result["target_directory"],
            result=result,
            nodes_used=[*nodes_used, self.memory_node.node_name],
            duration_seconds=duration_seconds,
            created_directories=directory_result["created_directories"],
            created_files=directory_result["created_files"],
            verification_result=verification_result,
            project_root=directory_result["project_root"],
            nodes=self.nodes,
        )
        nodes_used.append(self.memory_node.node_name)

        return {
            "task": task,
            "project_name": question_result["project_name"],
            "project_type": question_result["project_type"],
            "target_directory": str(question_result["target_directory"]),
            "project_root": str(directory_result["project_root"]),
            "result": result,
            "nodes_used": nodes_used,
            "duration_seconds": duration_seconds,
            "created_directories": [
                str(path) for path in directory_result["created_directories"]
            ],
            "created_files": [str(path) for path in directory_result["created_files"]],
            "verification_result": verification_result,
            "memory_file": str(memory_result["memory_file"]),
        }
