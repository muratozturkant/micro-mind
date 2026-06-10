# Questioning Node Module

## Purpose

This module owns user-question behavior.

Questioning nodes are used when Micro Mind needs missing information before it can safely continue a workflow.

This module exists so clarification logic does not get mixed into planning, execution, filesystem or memory nodes.

---

## Files

### question_node.py

Asks for required project creation information in the original Phase 1 project creation flow.

Current responsibilities:

- Detect missing project name
- Detect missing project type
- Detect missing target directory
- Return question prompts or completed answers
- Support the early project creation organism

---

## Inputs

Questioning nodes may receive:

- raw user request
- partial project data
- execution context
- missing required fields

Example:

```python
{
    "request": "Create a Flutter project",
    "project_name": None,
    "project_type": "flutter",
    "target_directory": None,
}
```

---

## Outputs

Questioning nodes may return:

- required question text
- field name being requested
- completed project input data
- status showing whether more input is needed

Example:

```python
{
    "status": "needs_input",
    "field": "project_name",
    "question": "What is the project name?",
}
```

---

## Rules

- Questioning nodes must only ask for missing information.
- Questioning nodes must not create files.
- Questioning nodes must not create directories.
- Questioning nodes must not install packages.
- Questioning nodes must not run shell commands.
- Questioning nodes must not guess critical project information when it is missing.
- If the system cannot safely infer a value, it should ask the user or wait for human guidance.

---

## Related Modules

### core/project_creation

Uses `QuestionNode` in the original Phase 1 project creation flow.

### core/context

May provide partial execution context and missing fields.

### nodes/filesystem

Runs after questioning has enough directory/project information.

### nodes/memory

May record question and answer history later.
