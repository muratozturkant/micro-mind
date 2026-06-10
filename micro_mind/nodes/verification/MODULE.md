# Verification Node Module

## Purpose

This module owns verification node behavior.

Verification nodes check whether previous workflow steps produced the expected result. They should observe and validate work, not perform the work themselves.

This module exists so validation logic does not get mixed into planning, filesystem, project structure or memory nodes.

---

## Files

### structure_verify_node.py

Verifies project structure output in the original Phase 1 project creation flow.

Current responsibilities:

- Check that required directories exist
- Check that required files exist
- Return verification status
- Report missing files or directories
- Support the early `ProjectCreateNetwork` flow

---

## Inputs

Verification nodes may receive:

- project path
- expected directories
- expected files
- execution context
- previous node results

Example:

```python
{
    "project_path": "/Volumes/HDD/MM_projects/block_heaven",
    "expected_directories": ["frontend", "backend", "database", "docs"],
    "expected_files": ["PROJECT_STATE.md", "DEVELOPMENT_RULES.md"],
}
```

---

## Outputs

Verification nodes may return:

- success/failure status
- missing directories
- missing files
- verification metadata

Example:

```python
{
    "status": "success",
    "missing_directories": [],
    "missing_files": [],
}
```

Failure example:

```python
{
    "status": "failed",
    "missing_directories": ["backend"],
    "missing_files": ["PROJECT_STATE.md"],
}
```

---

## Rules

- Verification nodes must only verify results.
- Verification nodes must not create missing files automatically.
- Verification nodes must not create missing directories automatically.
- Verification nodes must not install dependencies.
- Verification nodes must not generate source code.
- Verification nodes must not deploy projects.
- If verification fails, report the reason clearly.
- Repair behavior should belong to a separate repair node later.

---

## Related Modules

### core/project_creation

Uses `StructureVerifyNode` in the original Phase 1 project creation flow.

### nodes/filesystem

Filesystem nodes create structures that verification nodes check.

### nodes/project_structure

Newer project structure nodes may later use verification nodes after execution.

### nodes/memory

Memory nodes may record verification results.
