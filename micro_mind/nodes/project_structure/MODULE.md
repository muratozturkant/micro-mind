# Project Structure Node Module

## Purpose

This module owns project skeleton creation.

It is the first real executable node species in Micro Mind. It creates directories and initial project files on disk, then records those actions through the work tree logger.

---

## Files

### project_structure_node.py

Creates the initial project structure.

Current responsibilities:

- Receives `project_name`
- Receives `base_path`
- Slugifies the project name
- Creates the project root directory
- Creates standard child directories
- Creates initial project state files
- Optionally writes planned and executed actions to the work tree log

Current generated structure:

```text
<base_path>/<project_slug>/
├── frontend/
├── backend/
├── database/
├── docs/
├── PROJECT_STATE.md
├── DEVELOPMENT_RULES.md
└── .micro_mind/
    └── work_tree.jsonl
```

---

## Inputs

Expected context:

```python
{
    "project_name": "Node Auth API",
    "base_path": "/Volumes/HDD/MM_projects",
    "work_tree_log_path": "/Volumes/HDD/MM_projects/node_auth_api/.micro_mind/work_tree.jsonl",
}
```

Required fields:

- `project_name`
- `base_path`

Optional fields:

- `work_tree_log_path`

---

## Outputs

Example result:

```python
{
    "status": "executed",
    "node_name": "ProjectStructureNode",
    "project_name": "Node Auth API",
    "project_slug": "node_auth_api",
    "project_path": "/Volumes/HDD/MM_projects/node_auth_api",
    "created_directories": [],
    "created_files": [],
    "work_tree_log_path": "/Volumes/HDD/MM_projects/node_auth_api/.micro_mind/work_tree.jsonl",
}
```

Failure examples:

```python
{
    "status": "failed",
    "node_name": "ProjectStructureNode",
    "reason": "missing_project_name",
}
```

```python
{
    "status": "failed",
    "node_name": "ProjectStructureNode",
    "reason": "missing_base_path",
}
```

---

## Rules

- This module may create directories.
- This module may write only initial project structure files.
- This module may write `.micro_mind/work_tree.jsonl` through the logging module.
- This module must not install packages.
- This module must not generate application source code.
- This module must not run shell commands.
- This module must not deploy projects.
- This module must receive an explicit `base_path` from the caller.
- Project creation should normally happen under `/Volumes/HDD/MM_projects`.

---

## Related Modules

### core/logging

Provides `WorkTreeLogger` for planned and executed file tree actions.

### core/execution

Runs this node through `ExecutionRunner`.

### core/registry

Registers `ProjectStructureNode` as an executable node.

### core/planning

Produces the `create_project_structure` workflow step.
