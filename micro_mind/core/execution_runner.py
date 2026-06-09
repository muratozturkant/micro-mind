from micro_mind.core.node_factory import NodeFactory


class ExecutionRunner:
    def __init__(self):
        self.node_factory = NodeFactory()

    def run(self, workflow: list[str]) -> dict:
        execution_nodes = self.node_factory.create_many(workflow)
        executed_nodes = []
        skipped_nodes = []
        waiting_nodes = []

        for node in execution_nodes:
            node_status = node.get("status")
            node_name = node.get("node_name")

            if node_status == "available":
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
            }

        return {
            "status": "completed_with_skipped_nodes",
            "executed_nodes": executed_nodes,
            "skipped_nodes": skipped_nodes,
            "waiting_nodes": waiting_nodes,
        }
