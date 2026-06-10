# Dependency Node Module

## Purpose

This module owns dependency-related decisions and dependency installation preparation.

It decides which external packages a task needs and will later prepare or execute safe dependency installation steps.

This module exists so dependency logic does not get mixed into planning, execution or project structure creation.

---

## Files

### dependency_node.py

Decides package dependencies from a structured task plan.

Current example:

```python
{
    "project_type": "nodejs_api",
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt",
}
```

Produces:

```python
[
    "express",
    "cors",
    "mongoose",
    "jsonwebtoken",
    "bcryptjs",
    "dotenv",
]
```

---

### dependency_install_node.py

Planned node.

Future responsibility:

- Receive dependency list
- Build package manager plan
- Write package plan files
- Later: safely execute package manager commands when allowed

The first version should not run shell commands automatically.

---

## Inputs

This module receives task plan data.

Example:

```python
task_plan = {
    "project_type": "nodejs_api",
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt",
}
```

Future install node context may include:

```python
{
    "project_path": "/Volumes/HDD/MM_projects/node_auth_api",
    "dependencies": ["express", "mongoose"],
    "package_manager": "npm",
}
```

---

## Outputs

### DependencyNode output

```python
[
    "express",
    "cors",
    "mongoose",
    "jsonwebtoken",
    "bcryptjs",
    "dotenv",
]
```

### Future DependencyInstallNode output

```python
{
    "status": "executed",
    "node_name": "DependencyInstallNode",
    "package_manager": "npm",
    "dependencies": [],
    "plan_file": "package_plan.json",
}
```

---

## Rules

- Dependency decision logic belongs here.
- Dependency installation planning belongs here.
- This module must not create project skeleton directories.
- This module must not generate application source code.
- This module must not deploy projects.
- This module must not automatically run package manager commands until command execution safety exists.
- If dependencies cannot be decided reliably, the system should wait for human guidance instead of guessing.

---

## Related Modules

### core/planning

Uses dependency decisions while building task plan results.

### core/execution

Will execute `DependencyInstallNode` when it becomes available.

### core/registry

Maps `install_dependencies` to `DependencyInstallNode`.

### core/logging

May log package plan file creation and future package manager actions.
