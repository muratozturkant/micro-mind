

from micro_mind.core.registry.node_registry import NodeRegistry


def test_node_registry_returns_executable_node_instance():
    registry = NodeRegistry()

    node = registry.get("TaskPlannerNode")
    result = node.execute({"task": "Create Node.js Express MongoDB JWT Auth API"})

    assert result == {
        "status": "executed",
        "node_name": "TaskPlannerNode",
        "context": {
            "task": "Create Node.js Express MongoDB JWT Auth API",
        },
    }


def test_node_registry_knows_registered_nodes():
    registry = NodeRegistry()

    assert registry.has("TaskPlannerNode") is True
    assert registry.has("MemoryNode") is True
    assert registry.has("HumanGuidanceNode") is True
    assert registry.has("UnknownNode") is False


def test_node_registry_returns_none_for_unknown_node():
    registry = NodeRegistry()

    node = registry.get("UnknownNode")

    assert node is None


def test_human_guidance_node_returns_waiting_status():
    registry = NodeRegistry()

    node = registry.get("HumanGuidanceNode")
    result = node.execute({"reason": "missing_strategy"})

    assert result == {
        "status": "waiting_for_human_guidance",
        "node_name": "HumanGuidanceNode",
        "context": {
            "reason": "missing_strategy",
        },
    }
