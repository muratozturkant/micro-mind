# Core Micro Task Module

## Purpose

This module owns simulation-only micro task planning.

It decomposes a user task into small advisor questions, normalizes local AI facts and returns a planned micro task chain without executing or applying work.

## Files

### micro_question_builder.py

Builds small, specific local advisor questions.

### ai_fact_normalizer.py

Parses and normalizes local advisor answers into canonical facts.

### micro_task_chain_builder.py

Builds planned micro task chain JSON from normalized facts.

### micro_task_simulator.py

Coordinates the simulation-only planning pipeline with a local species and file queue.

## Inputs

This module receives:

- User task request dictionaries
- Local advisor JSON answers
- File-based queue directory

## Outputs

This module returns:

- Sleeping state when there is no work
- Simulated micro task chain JSON when facts are available
- Failed simulation state when local advisor answers cannot be used

## Rules

- This module must not write real project files.
- This module must not run shell commands.
- This module must not run package installation.
- This module must not deploy anything.
- This module must not use Docker.
- This module must not apply changes to a real workspace.
- This module must not add cloud fallback.
- This module is simulation-only and human-guidance-first.

## Related Modules

- `core/species`
- `core/model_queue`
- `core/decision`
- `core/execution`
