# Core Logging Module

## Purpose

This module owns persistent logs about what Micro Mind plans to do and what it actually does inside the project work tree.

It is the first layer for future timeline, project graph, audit trail and learning dataset features.

## Files

### work_tree_logger.py

Writes and reads work tree action logs in JSONL format.

Each log entry records:

- `timestamp`
- `node_name`
- `action`
- `target_path`
- `status`
- `metadata`

Example actions:

- `create_directory`
- `write_file`
- `update_file`
- `delete_file`
- `run_command`

Example statuses:

- `planned`
- `executed`
- `failed`
- `skipped`

## Inputs

The module receives explicit logging calls from nodes and execution systems.

Typical input:

```python
logger.log(
    node_name="ProjectStructureNode",
    action="create_directory",
    target_path="/Volumes/HDD/MM_projects/block_heaven/backend",
    status="executed",
    metadata={"project_slug": "block_heaven"},
)
```

## Outputs

The module writes JSONL records to a log file such as:

```text
/Volumes/HDD/MM_projects/<project_slug>/.micro_mind/work_tree.jsonl
```

Each line is one JSON record.

## Rules

- This module must only log actions.
- This module must not decide which node should run.
- This module must not create project source files except its own log file.
- This module must not execute commands.
- Log entries should be append-only.
- Logs should be readable later for timeline and memory processing.

## Related Modules

- `nodes/project_structure`: calls this module when creating directories and initial files.
- `core/execution`: may later use this module to log node execution lifecycle events.
- `core/context`: may later pass shared log paths and execution metadata.
