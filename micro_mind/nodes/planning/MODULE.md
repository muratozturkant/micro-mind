# Planning Node Module

## Purpose

This module owns planner-specific node behavior.

Planning nodes analyze a task and produce structured planning outputs. They are smaller node-level units used by higher-level planning networks.

This module should stay focused on understanding intent and building workflow steps. It must not directly execute file operations.

---

## Files

### task_planner_node.py

Analyzes a user task and returns a structured task plan.

Current example input:

```text
Create Node.js Express MongoDB JWT Auth API
```

Current example output:

```python
{
    "project_type": "nodejs_api",
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt",
}
```

If the task cannot be planned reliably, it returns a waiting state for human guidance.

---

### workflow_builder_node.py

Builds workflow step lists from a structured task plan.

Current example output:

```python
[
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
```

---

## Inputs

Planning nodes receive:

- raw user task text
- structured task plan dictionaries

Examples:

```python
TaskPlannerNode().execute("Create Node.js Express MongoDB JWT Auth API")
```

```python
WorkflowBuilderNode().execute({
    "project_type": "nodejs_api",
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt",
})
```

---

## Outputs

This module outputs:

- structured task plans
- workflow step lists
- human guidance waiting states when planning is uncertain

---

## Rules

- Planning nodes must not create files.
- Planning nodes must not create directories.
- Planning nodes must not install packages.
- Planning nodes must not run shell commands.
- Planning nodes must not automatically use cloud LLM fallback.
- If local planning cannot solve the task, return `waiting_for_human_guidance`.
- Workflow steps should be stable strings that `NodeFactory` can map.

---

## Related Modules

### core/planning

Uses these planning nodes to build high-level task results.

### core/registry

Maps workflow step strings produced here into node definitions.

### core/execution

Consumes workflow steps after planning is complete.

### nodes/dependency

Provides dependency decisions used during planning.
