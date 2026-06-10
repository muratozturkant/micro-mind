

from micro_mind.core.planning.task_planner_network import TaskPlannerNetwork
from micro_mind.core.registry.node_factory import NodeFactory


def test_task_planner_network_creates_nodejs_express_mongodb_jwt_plan():
    network = TaskPlannerNetwork()

    result = network.run("Create Node.js Express MongoDB JWT Auth API")

    assert result["status"] == "planned"
    assert result["task_plan"]["project_type"] == "nodejs_api"
    assert result["task_plan"]["runtime"] == "nodejs"
    assert result["task_plan"]["framework"] == "express"
    assert result["task_plan"]["database"] == "mongodb"
    assert result["task_plan"]["auth"] == "jwt"

    assert result["dependencies"] == [
        "express",
        "mongoose",
        "jsonwebtoken",
        "bcryptjs",
        "dotenv",
        "cors",
    ]

    assert result["workflow"] == [
        "analyze_task",
        "create_project_structure",
        "install_dependencies",
        "create_mongo_connection",
        "create_user_model",
        "create_jwt_service",
        "create_auth_middleware",
        "create_register_route",
        "create_login_route",
        "create_protected_route",
        "verify_api",
        "save_memory",
    ]


def test_task_planner_network_waits_for_human_when_local_llm_cannot_plan():
    network = TaskPlannerNetwork()

    result = network.run("Create something unknown and unclear")

    assert result["status"] == "waiting_for_human_guidance"
    assert result["reason"] == "local_llm_could_not_create_reliable_plan"
    assert result["next_action"] == "ask_human_for_solution_direction"


def test_node_factory_creates_node_definitions_from_workflow_steps():
    factory = NodeFactory()

    nodes = factory.create_many([
        "analyze_task",
        "create_user_model",
        "create_jwt_service",
        "verify_api",
        "save_memory",
    ])

    assert nodes == [
        {
            "node_type": "planner",
            "node_name": "TaskPlannerNode",
            "status": "available",
        },
        {
            "node_type": "execution",
            "node_name": "UserModelNode",
            "status": "planned_not_implemented",
        },
        {
            "node_type": "execution",
            "node_name": "JWTServiceNode",
            "status": "planned_not_implemented",
        },
        {
            "node_type": "verification",
            "node_name": "APIVerifyNode",
            "status": "planned_not_implemented",
        },
        {
            "node_type": "memory",
            "node_name": "MemoryNode",
            "status": "available",
        },
    ]


def test_node_factory_waits_for_human_guidance_for_unknown_steps():
    factory = NodeFactory()

    node = factory.create("unknown_future_step")

    assert node == {
        "node_type": "unknown",
        "node_name": "UnknownNode",
        "status": "waiting_for_human_guidance",
    }
