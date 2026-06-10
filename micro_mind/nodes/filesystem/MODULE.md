# Filesystem Node Module

## Purpose

This module owns low-level filesystem node behavior.

Filesystem nodes perform direct file and directory operations used by early project creation workflows. They should remain focused on filesystem changes only.

This module exists so directory and file operations do not get mixed into planning, dependency, memory or verification nodes.

---

## Files

### directory_create_node.py

Creates directories and initial files for the original Phase 1 project creation flow.

Current responsibilities:

- Create requested project directories
- Create basic project files
- Return created path information
- Support the early `ProjectCreateNetwork` flow

This node belongs to the original MVO flow and may later be replaced or wrapped by newer execution-based nodes.

---

## Inputs

Filesystem nodes may receive:

- target directory
- project name
- folder list
- file list
- execution context

Example:

```python
{
    "project_name": "Block Heaven",
    "target_directory": "/Volumes/HDD/MM_projects",
    "folders": ["frontend", "backend", "database", "docs"],
}
```

---

## Outputs

Filesystem nodes may return:

- created directory paths
- created file paths
- success/failure status
- error reason if a filesystem operation fails

Example:

```python
{
    "status": "success",
    "created_directories": [],
    "created_files": [],
}
```

---

## Rules

- Filesystem nodes may create directories.
- Filesystem nodes may create basic files when explicitly required.
- Filesystem nodes must not decide project strategy.
- Filesystem nodes must not install dependencies.
- Filesystem nodes must not generate application logic.
- Filesystem nodes must not deploy projects.
- Filesystem nodes should only operate inside approved project workspaces.
- New project structure behavior should prefer `nodes/project_structure` unless this module is intentionally being used for legacy Phase 1 flow.

---

## Related Modules

### core/project_creation

Uses filesystem nodes in the original Phase 1 project creation flow.

### nodes/questioning

Runs before filesystem operations when required information is missing.

### nodes/verification

Verifies filesystem output after creation.

### nodes/project_structure

Owns the newer project skeleton node used by execution-based workflows.

### core/logging

May later receive filesystem operation logs.
