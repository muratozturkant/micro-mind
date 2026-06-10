# Core Decision Module

## Purpose

This module owns validation of advisor suggestions before Micro Mind logic considers them.

It protects simulation-first and human-guidance-first behavior by rejecting or routing uncertain local AI output to human guidance.

## Files

### ai_suggestion_validator.py

Validates parsed local AI suggestion dictionaries.

## Inputs

This module receives parsed local AI advisor responses.

## Outputs

This module returns validation decisions:

- `accepted`
- `requires_human_guidance`
- `rejected`

## Rules

- This module must not execute workflows.
- This module must not apply changes.
- This module must not call local or cloud models.
- This module must reject invalid advisor output.
- This module must route low-confidence suggestions to human guidance.

## Related Modules

- `core/species`
- `core/model_queue`
- `core/planning`
