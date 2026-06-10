# Core Project Creation Module

## Purpose

This module owns the original Phase 1 project creation flow.

It represents the early Minimum Viable Organism flow where Micro Mind can ask questions, create folders, verify project structure and save memory.

This module is considered a legacy/early project creation flow while newer execution-based planning evolves under `core/planning` and `core/execution`.

---

## Files

### project_create_network.py

Coordinates the original project creation chain.

Current responsibility:

```text
RootPlanner
↓
ProjectCreateNetwork
↓
QuestionNode
↓
DirectoryCreateNode
↓
StructureVerifyNode
↓
MemoryNode
```

This flow is focused on basic project structure creation and verification.

---

## Inputs

Typical input:

```text
Create a project called Block Heaven
```

or structured project creation data from tests or CLI layers.

---

## Outputs

Expected output includes:

- project directory creation result
- structure verification result
- memory record result
- execution context updates

---

## Rules

- This module may coordinate basic project creation.
- This module should remain stable while newer planning/execution modules evolve.
- This module should not absorb new task-planning responsibilities.
- New workflow execution behavior should go through `core/planning` and `core/execution`.
- If this module is refactored, tests must remain green after each move.

---

## Related Modules

### core/context

Provides execution context data used by the project creation flow.

### nodes/questioning

Owns user question behavior.

### nodes/filesystem

Owns directory creation behavior.

### nodes/verification

Owns structure verification behavior.

### nodes/memory

Owns memory recording behavior.

### core/planning

Owns the newer task planning and project creation execution network.
