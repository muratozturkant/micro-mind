# Core Apply Module

## Purpose

This module owns the safe transition from simulation output to real execution planning.

It does not directly write project files in the first version.

Instead, it converts a verified simulation report into an explicit apply plan and then simulates what the real apply phase would do.

The apply module exists to keep real workspace changes separate from planning, AI questioning, micro task simulation and final execution.

---

## Core Rule

```text
Simulation report first.
Apply plan second.
Apply simulation third.
Real apply later.
```

No real file writes should happen in this module until a dedicated real apply runner exists and all safety checks are satisfied.

---

## Files

### apply_plan_builder.py

Builds an apply plan from a micro task simulation report.

Current expected responsibility:

- Read `simulation.micro_tasks`
- Convert planned micro tasks into apply tasks
- Mark which actions would affect the real workspace
- Preserve source task IDs
- Preserve target paths
- Add approval and safety metadata

Example apply task:

```json
{
  "id": "apply_1.1",
  "from_micro_task": "task_1.1",
  "action": "create_directory",
  "target": "src/routes",
  "status": "planned",
  "requires_approval": true
}
```

---

### apply_simulator.py

Simulates the apply plan without touching the real workspace.

Current expected responsibility:

- Receive an apply plan
- Verify that no forbidden path is targeted
- Verify that no real write command is executed
- Return a report describing what would happen
- Keep `will_write_real_files` as `false`

Example apply simulation result:

```json
{
  "status": "apply_simulated",
  "will_write_real_files": false,
  "will_run_commands": false,
  "apply_task_count": 12,
  "safe_to_request_human_approval": true
}
```
