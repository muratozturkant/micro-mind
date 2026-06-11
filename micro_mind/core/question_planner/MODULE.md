# Core Question Planner Module

## Purpose

This module owns local-AI-assisted micro question planning.

It can ask a local advisor for a candidate question plan, validate and normalize that plan, and safely fall back to the default micro questions when the candidate is invalid.

## Files

### question_plan_generator.py

Builds the single deterministic prompt used to ask local AI for a question plan.

### question_plan_validator.py

Validates and normalizes AI-produced question plan objects.

### question_plan_runtime.py

Coordinates local AI question-plan generation with default-question fallback.

## Inputs

This module receives:

- User task strings
- Injected local AI objects with `ask` or `classify_task`
- AI-produced question plan candidates
- Fallback `MicroQuestionBuilder`

## Outputs

This module returns:

- Sleeping state when there is no work
- Accepted local AI question plans
- Default fallback questions when local AI fails or validation rejects a plan

## Rules

- This module must not write real project files.
- This module must not run shell commands.
- This module must not run package installation.
- This module must not deploy anything.
- This module must not use Docker.
- This module must not call cloud models.
- Local AI is a question-planning advisor only.
- Existing default questions must continue working.

## Related Modules

- `core/micro_task`
- `core/species`
- `core/decision`
