# Core Model Queue Module

## Purpose

This module owns local, file-based model request queues.

It lets Micro Mind persist advisor requests and outcomes without introducing external services.

## Files

### file_model_queue.py

Stores pending, completed and failed model requests in JSONL files.

## Inputs

This module receives:

- Queue directory
- Request dictionaries
- Local advisor responses
- Failure reasons

## Outputs

This module produces JSONL records for pending, completed and failed advisor requests.

## Rules

- This module must be file based only.
- This module must not use Redis or other queue services.
- This module must not execute workflows.
- This module must not apply changes.
- This module must not call local or cloud models.

## Related Modules

- `core/species`
- `core/decision`
