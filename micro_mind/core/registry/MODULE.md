# Core Registry Module

## Purpose

This module owns the mapping layer between workflow definitions and executable node implementations.

The registry layer is responsible for answering two questions:

1. Which node should handle a workflow step?
2. Which executable class should be instantiated for a node name?

This module acts as the connection point between planning and execution.

---

## Files

### node_factory.py

Converts workflow steps into node definitions.

Example:

```text
create_project_structure
↓
ProjectStructureNode
```

Returns metadata such as:

- node name
- node type
- execution status

---

### node_registry.py

Maps node names to executable node classes.

Example:

```text
ProjectStructureNode
↓
ProjectStructureNode class
↓
instance
↓
execute(context)
```

Responsible for returning executable node instances.

---

## Inputs

The module receives:

- workflow step names
- node names
- execution requests from ExecutionRunner

Examples:

```python
node_factory.create("create_project_structure")
```

```python
node_registry.get("ProjectStructureNode")
```

---

## Outputs

### Node Definitions

Example:

```python
{
    "node_name": "ProjectStructureNode",
    "node_type": "execution",
    "status": "available",
}
```

### Executable Instances

Example:

```python
ProjectStructureNode()
```

---

## Rules

- Registry modules must not perform project work.
- Registry modules must not create files.
- Registry modules must not install dependencies.
- Registry modules must not execute shell commands.
- Registry modules only map names and relationships.
- Business logic belongs inside nodes.

---

## Related Modules

### core/execution

Uses this module to obtain executable nodes.

### core/planning

Produces workflow steps consumed by this module.

### nodes/\*

Registry maps workflow steps and node names to these implementations.

---

## Future Responsibilities

Later versions may support:

- dynamic species registration
- plugin nodes
- external node packages
- versioned node registries
- capability discovery

The registry should remain lightweight and focused on node lookup and mapping.
