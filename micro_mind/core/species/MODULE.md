# Core Species Module

## Purpose

This module owns local advisor species integrations.

It provides narrow adapters for local models that can classify or suggest, while leaving final decisions inside Micro Mind logic.

## Files

### local_llama_species.py

Calls a local OpenAI-compatible llama endpoint for JSON-only task classification advice.

## Inputs

This module receives:

- Local model endpoint
- Local model name
- Timeout
- Task text

## Outputs

This module returns structured advisor results containing parsed JSON, raw response data and failure details.

## Rules

- Local AI is advisor only.
- This module must not execute workflows.
- This module must not apply changes.
- This module must not call cloud models.
- This module must request JSON-only responses.
- This module must preserve simulation-first and human-guidance-first behavior by returning advice only.

## Related Modules

- `core/decision`
- `core/model_queue`
- `core/planning`
