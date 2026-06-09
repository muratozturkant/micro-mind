from time import perf_counter

from micro_mind.core.execution_context import ExecutionContext
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
        context = ExecutionContext(
            task_type=task,
            project_name=project_name,
            project_type=project_type,
            target_directory=target_directory,
        )
        context.metadata["nodes_used"] = []

        self.question_node.run(context=context)
        context.metadata["nodes_used"].append(self.question_node.node_name)

        self.directory_create_node.run(context)
        context.metadata["nodes_used"].append(self.directory_create_node.node_name)

        self.structure_verify_node.run(context=context)
        context.metadata["nodes_used"].append(self.structure_verify_node.node_name)

        result = "success" if context.verification_result["success"] else "failure"
        duration_seconds = perf_counter() - started_at
        context.metadata["result"] = result
        context.metadata["duration_seconds"] = duration_seconds
        context.metadata["nodes_used"].append(self.memory_node.node_name)

        memory_result = self.memory_node.run(
            context=context,
            nodes=self.nodes,
        )

        return {
            "task": task,
            "project_name": context.project_name,
            "project_type": context.project_type,
            "target_directory": str(context.target_directory),
            "project_root": str(context.project_root),
            "result": result,
            "nodes_used": context.metadata["nodes_used"],
            "duration_seconds": duration_seconds,
            "created_directories": [
                str(path) for path in context.created_directories
            ],
            "created_files": [str(path) for path in context.created_files],
            "verification_result": context.verification_result,
            "memory_file": str(memory_result["memory_file"]),
        }
