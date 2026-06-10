# Micro Mind Module Layout

This document defines how Micro Mind source files should be organized as the system grows.

The goal is to prevent `core/` and `nodes/` from becoming large, unclear folders.
Every responsibility area must live inside a clear module directory, and every module directory must explain itself.

---

## Core Rule

Every responsibility area must have:

1. A dedicated directory
2. A `MODULE.md` file inside that directory
3. Files with one clear responsibility
4. Tests that mirror the module structure where practical

A new file should not be added directly into a crowded generic folder unless it is temporary and marked for migration.

---

## Current Problem

Current files are growing under broad folders:

```text
micro_mind/core/
micro_mind/nodes/
tests/
```

This is acceptable for the early prototype, but it will become hard to maintain when Micro Mind gains more node species, runners, planners, loggers and verifiers.

---

## Target Source Layout

```text
micro_mind/
├── core/
│   ├── execution/
│   │   ├── execution_runner.py
│   │   └── MODULE.md
│   │
│   ├── planning/
│   │   ├── task_planner_network.py
│   │   ├── project_creation_execution_network.py
│   │   └── MODULE.md
│   │
│   ├── registry/
│   │   ├── node_factory.py
│   │   ├── node_registry.py
│   │   └── MODULE.md
│   │
│   ├── logging/
│   │   ├── work_tree_logger.py
│   │   └── MODULE.md
│   │
│   ├── context/
│   │   ├── execution_context.py
│   │   └── MODULE.md
│   │
│   └── project_creation/
│       ├── project_create_network.py
│       └── MODULE.md
│
├── nodes/
│   ├── planning/
│   │   ├── task_planner_node.py
│   │   ├── workflow_builder_node.py
│   │   └── MODULE.md
│   │
│   ├── dependency/
│   │   ├── dependency_node.py
│   │   ├── dependency_install_node.py
│   │   └── MODULE.md
│   │
│   ├── project_structure/
│   │   ├── project_structure_node.py
│   │   └── MODULE.md
│   │
│   ├── questioning/
│   │   ├── question_node.py
│   │   └── MODULE.md
│   │
│   ├── verification/
│   │   ├── structure_verify_node.py
│   │   └── MODULE.md
│   │
│   ├── memory/
│   │   ├── memory_node.py
│   │   ├── memory_read_node.py
│   │   ├── memory_summary_node.py
│   │   └── MODULE.md
│   │
│   └── filesystem/
│       ├── directory_create_node.py
│       └── MODULE.md
```

---

## Target Test Layout

Tests should gradually mirror the source layout:

```text
tests/
├── core/
│   ├── execution/
│   │   └── test_execution_runner.py
│   ├── planning/
│   │   ├── test_task_planner_network.py
│   │   └── test_project_creation_execution_network.py
│   ├── registry/
│   │   └── test_node_registry.py
│   ├── logging/
│   │   └── test_work_tree_logger.py
│   └── context/
│       └── test_execution_context.py
│
└── nodes/
    └── project_structure/
        └── test_project_structure_node.py
```

For now, existing flat tests may remain until migration is done safely.

---

## Required `MODULE.md` Format

Every module directory must include a `MODULE.md` file with this structure:

```markdown
# Module Name

## Purpose

Short explanation of what this module owns.

## Files

### file_name.py

What this file does.

## Inputs

What this module receives.

## Outputs

What this module produces.

## Rules

- Important boundaries
- What this module must not do
- Safety constraints

## Related Modules

- Other modules this module depends on
```

---

## Initial Module Responsibilities

### `core/execution`

Owns the execution loop.

Responsible for:

- Taking workflow steps
- Asking `NodeFactory` for node definitions
- Asking `NodeRegistry` for executable node instances
- Running `node.execute(context)`
- Returning executed, skipped, waiting and failed node results

Must not:

- Decide task strategy
- Write project files directly
- Install dependencies directly

---

### `core/planning`

Owns high-level planning networks.

Responsible for:

- Turning user tasks into structured plans
- Building workflows
- Orchestrating project creation flows

Must not:

- Directly write files when an execution node should do it
- Hide execution behavior inside planning code

---

### `core/registry`

Owns mapping between workflow names and executable node classes.

Responsible for:

- `NodeFactory`: workflow step -> node definition
- `NodeRegistry`: node name -> executable node instance

Must not:

- Execute node behavior directly
- Contain business logic for project creation

---

### `core/logging`

Owns persistent execution logs.

Responsible for:

- Writing work tree actions
- Reading work tree actions
- Supporting future timeline and project graph views

Must not:

- Decide whether a node should run
- Modify files outside log files

---

### `nodes/project_structure`

Owns project skeleton creation.

Responsible for:

- Creating project directories
- Creating initial project files
- Logging planned and executed file tree actions

Must not:

- Install packages
- Generate app code
- Deploy projects

---

### `nodes/dependency`

Owns dependency decisions and dependency installation behavior.

Responsible for:

- Deciding package lists
- Preparing install plans
- Later: running package manager commands safely

Must not:

- Decide project architecture alone
- Write unrelated source code

---

### `nodes/planning`

Owns planner-specific node logic.

Responsible for:

- Analyzing tasks
- Producing task plans
- Producing workflow steps

Must not:

- Execute file operations directly

---

## Migration Plan

### Step 1 — Document Current Layout

Create this file and freeze the modular direction.

### Step 2 — Add Module Directories

Create directories and `MODULE.md` files without moving Python files yet.

### Step 3 — Move One Module at a Time

Move files in small commits.

Suggested order:

1. `core/logging`
2. `core/registry`
3. `core/execution`
4. `nodes/project_structure`
5. `core/planning`
6. `nodes/planning`
7. `nodes/dependency`
8. Remaining legacy project creation nodes

### Step 4 — Update Imports

After each move, update imports and run tests.

### Step 5 — Preserve Green Tests

After every module migration:

```bash
python -m pytest
```

must pass.

---

## New File Rule

Before adding any new Python file, decide:

1. Which module owns this file?
2. Does that module directory exist?
3. Does that module have a `MODULE.md`?
4. Is the file responsibility described in that `MODULE.md`?

If the answer is no, create or update the module documentation first.

---

## Current Decision

From this point forward, Micro Mind development should be module-first.

No new large behavior should be added directly into broad folders without a module boundary.
