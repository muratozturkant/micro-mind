# Core Project Tree Module

## Purpose

This module owns project structure knowledge.

A project tree record explains why a file, directory, import, route, controller, service, test or configuration exists.

The project tree is not the filesystem.

The filesystem stores files.

The project tree stores relationships.

---

## Core Rule

```text
Every artifact must have provenance.
```

Micro Mind should always be able to answer:

- Why does this file exist?
- Which task created it?
- Which recipe created it?
- Which node requested it?
- Which verification approved it?
- Which files depend on it?

---

## Files

### project_tree_record.py

Creates project tree records.

Owns:

- artifact identity
- ownership
- provenance metadata
- dependency references

---

### project_tree_store.py

Stores and loads project tree records.

Current version should be file based.

Example:

```text
.micro_mind/project_tree.jsonl
```

---

### project_tree_query.py

Provides deterministic lookup.

Examples:

- find by path
- find by task
- find by recipe
- find dependents
- find imports
- find verification chain

No AI calls allowed.

---

## Example Record

```json
{
  "artifact_id": "artifact_001",

  "path": "src/routes/user/get_user.js",

  "artifact_type": "file",

  "responsibility": "get_user_route",

  "created_by_task": "task_18.2",

  "recipe_id": "nodejs_backend_basic_v1",

  "node_id": "route_creation_node",

  "imports": ["src/routes/index.js"],

  "depends_on": [],

  "verified_by": ["task_18.4"],

  "status": "verified"
}
```

---

## Relationship With Recipes

Recipes describe how work should happen.

Project Tree describes what was created.

```text
Recipe
↓
Micro Tasks
↓
Project Tree Records
```

---

## Relationship With Apply Layer

Apply creates artifacts.

Project Tree records them.

```text
Apply
↓
File Created
↓
Project Tree Record Created
```

---

## Current Decision

The project tree is the memory of the workspace.

Recipes remember knowledge.

Project Tree remembers structure.

Together they allow deterministic modification of large projects without scanning the entire repository.
