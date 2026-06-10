# Core Context Module

## Purpose

This module owns shared execution context structures.

Execution context is the data package that travels through Micro Mind workflows. It allows planners, runners and nodes to share task information, project paths, metadata and execution state without passing many unrelated arguments manually.

---

## Files

### execution_context.py

Defines the execution context used by project creation workflows.

Current responsibilities:

- Store user task data
- Store project metadata
- Store target paths
- Store execution state
- Provide a structured object that nodes and networks can pass around

---

## Inputs

This module receives structured data from networks and CLI layers.

Example context data:

```python
{
    "task": "Create Node.js Express MongoDB JWT Auth API",
    "project_name": "Block Heaven",
    "base_path": "/Volumes/HDD/MM_projects",
    "work_tree_log_path": "/Volumes/HDD/MM_projects/block_heaven/.micro_mind/work_tree.jsonl",
}
```

---

## Outputs

This module provides shared context objects or dictionaries for:

- planning networks
- execution runner
- executable nodes
- memory systems
- logging systems

---

## Rules

- Context modules must not execute work directly.
- Context modules must not create files directly.
- Context modules must not install dependencies.
- Context modules must not decide task strategy.
- Context should remain explicit and readable.
- Context should be safe to serialize later for memory and timeline usage.

---

## Related Modules

### core/planning

Creates or enriches context before execution.

### core/execution

Passes context into executable nodes.

### core/logging

May receive log paths and metadata from context.

### nodes/\*

Nodes read context values during execution.
