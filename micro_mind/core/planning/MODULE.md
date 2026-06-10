# Core Planning Module

## Purpose

This module owns high-level planning networks.

Planning modules turn user intent into structured task plans and workflow steps. They decide what should happen, but they should not directly perform project work.

---

## Files

### task_planner_network.py

Coordinates the task planning chain.

Current responsibilities:

- Receives a user task
- Calls planner nodes
- Produces a structured task plan
- Produces dependency decisions
- Produces workflow steps
- Produces execution node definitions and execution preview

---

### project_creation_execution_network.py

Runs the first end-to-end project creation workflow.

Current responsibilities:

- Receives task, project name and base path
- Applies the default Micro Mind project workspace rule
- Rejects forbidden base paths
- Calls task planning
- Calls project structure execution
- Returns project path and work tree log path

Important path rule:

```text
Allowed default base path:
/Volumes/HDD/MM_projects

Forbidden base path:
/Volumes/HDD/projects
```

---

## Inputs

Planning modules receive high-level user intent.

Examples:

```text
Create Node.js Express MongoDB JWT Auth API
```

```python
network.run(
    task="Create Node.js Express MongoDB JWT Auth API",
    project_name="Block Heaven",
    base_path="/Volumes/HDD/MM_projects",
)
```

---

## Outputs

Planning modules produce structured outputs.

Example task plan:

```python
{
    "project_type": "nodejs_api",
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt",
}
```

Example workflow:

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

## Rules

- Planning modules must decide what should happen.
- Planning modules must not directly write arbitrary project code.
- Planning modules must not install dependencies directly.
- Planning modules must not run shell commands directly.
- If the local planning system cannot create a reliable plan, it must return `waiting_for_human_guidance`.
- Planning must not automatically fall back to GPT, Claude or Gemini.
- Local LLM attempts may be added later, but unresolved planning must wait for human guidance.

---

## Related Modules

### core/execution

Consumes workflow steps and runs executable nodes.

### core/registry

Maps workflow steps to node definitions and executable node instances.

### nodes/planning

Contains planner node implementations used by this module.

### nodes/dependency

Provides dependency decisions.

### nodes/project_structure

Executes the project skeleton creation step when planning produces `create_project_structure`.
