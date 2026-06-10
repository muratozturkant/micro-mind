from micro_mind.core.registry.node_factory import NodeFactory
from micro_mind.core.registry.node_registry import NodeRegistry


class ExecutionRunner:
    def __init__(self):
        self.node_factory = NodeFactory()
        self.node_registry = NodeRegistry()

    def run(self, workflow: list[str], context: dict | None = None) -> dict:
        context = context or {}

        execution_nodes = self.node_factory.create_many(workflow)
        executed_nodes = []
        skipped_nodes = []
        waiting_nodes = []
        node_results = []

        for node_definition in execution_nodes:
            node_status = node_definition.get("status")
            node_name = node_definition.get("node_name")

            if node_status == "available":
                executable_node = self.node_registry.get(node_name)

                if executable_node is None:
                    skipped_nodes.append(
                        {
                            "node_name": node_name,
                            "reason": "node_not_registered",
                        }
                    )
                    continue

                result = executable_node.execute(context)
                node_results.append(result)

                if result.get("status") == "waiting_for_human_guidance":
                    waiting_nodes.append(node_name)
                    continue

                if result.get("status") == "failed":
                    return {
                        "status": "failed",
                        "failed_node": node_name,
                        "failure": result,
                        "executed_nodes": executed_nodes,
                        "skipped_nodes": skipped_nodes,
                        "waiting_nodes": waiting_nodes,
                        "node_results": node_results,
                    }

                executed_nodes.append(node_name)
                continue

            if node_status == "planned_not_implemented":
                skipped_nodes.append(
                    {
                        "node_name": node_name,
                        "reason": "node_not_implemented_yet",
                    }
                )
                continue

            if node_status == "waiting_for_human_guidance":
                waiting_nodes.append(node_name)

        if waiting_nodes:
            return {
                "status": "waiting_for_human_guidance",
                "executed_nodes": executed_nodes,
                "skipped_nodes": skipped_nodes,
                "waiting_nodes": waiting_nodes,
                "node_results": node_results,
            }

        if skipped_nodes:
            return {
                "status": "completed_with_skipped_nodes",
                "executed_nodes": executed_nodes,
                "skipped_nodes": skipped_nodes,
                "waiting_nodes": waiting_nodes,
                "node_results": node_results,
            }

        return {
            "status": "completed",
            "executed_nodes": executed_nodes,
            "skipped_nodes": skipped_nodes,
            "waiting_nodes": waiting_nodes,
            "node_results": node_results,
        }
