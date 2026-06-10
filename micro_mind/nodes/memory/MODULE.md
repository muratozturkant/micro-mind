# Memory Node Module

## Purpose

This module owns memory-related node behavior.

Memory nodes record, read and summarize Micro Mind execution history so the organism can learn from successful and failed workflows over time.

---

## Files

### memory_node.py

Records execution results and node statistics for the original Phase 1 project creation flow.

Current responsibilities:

- Save execution records
- Save node usage information
- Save basic success/failure metadata
- Preserve workflow history for later learning

---

### memory_read_node.py

Reads stored memory records.

Current responsibilities:

- Load previous execution records
- Provide memory data to higher-level networks
- Support memory reader workflows

---

### memory_summary_node.py

Summarizes stored memory records.

Current responsibilities:

- Convert raw memory records into readable summaries
- Extract useful workflow history
- Prepare memory output for CLI or future UI layers

---

## Inputs

Memory nodes may receive:

- task name
- project name
- execution result
- used nodes
- duration
- success/failure status
- created files and directories
- previous memory records

Example memory input:

```python
{
    "task": "create_project_structure",
    "project_name": "block_heaven",
    "result": "success",
    "nodes": [
        "QuestionNode",
        "DirectoryCreateNode",
        "StructureVerifyNode",
    ],
    "duration_seconds": 3,
}
```

---

## Outputs

Memory nodes may produce:

- saved memory records
- loaded memory records
- summarized memory reports
- workflow history data

Example output:

```python
{
    "status": "saved",
    "memory_type": "execution_record",
    "task": "create_project_structure",
}
```

---

## Rules

- Memory nodes must not execute project work.
- Memory nodes must not create project source files.
- Memory nodes must not install dependencies.
- Memory nodes must not decide planning strategy alone.
- Memory records should be structured and readable.
- Failed executions must be preserved, not hidden.
- Memory should support future learning, scoring and evolution.

---

## Related Modules

### core/project_creation

Uses memory nodes in the original Phase 1 project creation chain.

### core/execution

May later send execution results into memory nodes.

### core/logging

Stores work tree action logs that may later be summarized into memory.

### core/context

May pass execution metadata into memory nodes.
