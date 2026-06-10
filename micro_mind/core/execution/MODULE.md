# Core Execution Module

## Purpose

This module owns the execution loop of Micro Mind.

It is responsible for taking workflow steps, resolving them into executable nodes and running those nodes with a shared execution context.

This module is the first version of Micro Mind's nervous system.

---

## Files

### execution_runner.py

Runs workflow steps.

Current responsibilities:

- Receives a workflow list
- Uses `NodeFactory` to convert workflow steps into node definitions
- Uses `NodeRegistry` to resolve executable node instances
- Calls `node.execute(context)`
- Tracks executed nodes
- Tracks skipped nodes
- Tracks nodes waiting for human guidance
- Stops safely when a node fails

Example flow:

```text
workflow step
↓
NodeFactory
↓
node definition
↓
NodeRegistry
↓
executable node
↓
execute(context)
```

---

## Inputs

The module receives:

- `workflow`: ordered list of workflow step names
- `context`: shared execution data passed into executable nodes

Example:

```python
runner.run(
    [
        "analyze_task",
        "create_project_structure",
        "install_dependencies",
        "save_memory",
    ],
    context={
        "project_name": "Node Auth API",
        "base_path": "/Volumes/HDD/MM_projects",
        "work_tree_log_path": "/Volumes/HDD/MM_projects/node_auth_api/.micro_mind/work_tree.jsonl",
    },
)
```

---

## Outputs

The execution runner returns a structured execution result.

Example:

```python
{
    "status": "completed_with_skipped_nodes",
    "executed_nodes": [
        "TaskPlannerNode",
        "ProjectStructureNode",
        "MemoryNode",
    ],
    "skipped_nodes": [
        {
            "node_name": "DependencyInstallNode",
            "reason": "node_not_implemented_yet",
        },
    ],
    "waiting_nodes": [],
    "node_results": [],
}
```

Possible statuses:

- `completed`
- `completed_with_skipped_nodes`
- `waiting_for_human_guidance`
- `failed`

---

## Rules

- This module must execute nodes through `NodeRegistry`.
- This module must not directly instantiate business nodes except through registry.
- This module must not decide task strategy.
- This module must not create files directly.
- This module must not install dependencies directly.
- This module must stop safely when an executable node returns `failed`.
- If a node cannot be resolved or is not implemented, it must be skipped or moved to human guidance instead of guessing.

---

## Related Modules

### core/registry

Provides `NodeFactory` and `NodeRegistry`.

### core/planning

Produces workflows consumed by this module.

### nodes/\*

Executable node implementations live under node modules.

### core/logging

Execution lifecycle logging may later be added through the logging module.
