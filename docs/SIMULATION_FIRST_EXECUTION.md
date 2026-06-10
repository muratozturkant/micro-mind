# Simulation First Execution

This document defines Micro Mind's simulation-first execution model.

The goal is simple:

```text
No direct apply without simulation.
```

Micro Mind should not immediately modify the real project when a workflow is produced. It should first run the workflow in a controlled simulation workspace, verify the result, and only then apply the same workflow to the real project workspace.

---

## Core Principle

Micro Mind prioritizes:

1. Learnability
2. Consistency
3. Safety
4. Economy
5. Debuggability

Speed is useful, but it is not the primary goal.

Therefore, every risky action should follow this flow:

```text
Plan
↓
Simulate
↓
Verify
↓
Apply
↓
Log
↓
Memory
```

---

## Why Simulation First?

Without simulation, a node may directly damage or pollute a real project.

Example risks:

- Wrong file path
- Wrong project structure
- Wrong generated code
- Wrong package plan
- Broken dependency installation
- Invalid workflow step
- Missing context value
- Overwriting existing files

Simulation creates a safe laboratory where nodes can prove that their planned behavior works before touching the real project.

---

## Workspace Rules

Real projects live under:

```text
/Volumes/HDD/MM_projects
```

Simulations should live under:

```text
/Volumes/HDD/MM_projects/.simulations
```

Forbidden workspace:

```text
/Volumes/HDD/projects
```

Micro Mind must not create project output under the forbidden workspace.

---

## Simulation Workspace Structure

A simulated run should create an isolated workspace:

```text
/Volumes/HDD/MM_projects/.simulations/<project_slug>/<run_id>/
├── workspace/
├── logs/
│   └── work_tree.jsonl
├── result.json
└── verification.json
```

Example:

```text
/Volumes/HDD/MM_projects/.simulations/block_heaven/2026-06-10T10-30-00Z/
```

---

## Execution Flow

### 1. Plan

The planner creates a workflow.

Example:

```python
[
    "analyze_task",
    "create_project_structure",
    "install_dependencies",
    "verify_api",
    "save_memory",
]
```

Planning should not modify the project.

---

### 2. Simulate

The execution runner runs available nodes against the simulation workspace, not the real project path.

Example:

```python
simulation_context = {
    "project_name": "Block Heaven",
    "base_path": "/Volumes/HDD/MM_projects/.simulations/block_heaven/<run_id>/workspace",
    "work_tree_log_path": "/Volumes/HDD/MM_projects/.simulations/block_heaven/<run_id>/logs/work_tree.jsonl",
}
```

Nodes should behave as if they are working on the real project, but all writes stay inside the simulation workspace.

---

### 3. Verify

Verification checks whether the simulated result is valid.

Verification can include:

- Required directories exist
- Required files exist
- JSON files are valid
- Workflow steps are known
- No forbidden paths were touched
- No unexpected file writes happened
- Node results are complete
- Work tree log contains expected actions

If verification fails, Micro Mind must not apply to the real project.

---

### 4. Apply

Only after successful simulation and verification can the workflow run against the real project workspace.

Example:

```python
real_context = {
    "project_name": "Block Heaven",
    "base_path": "/Volumes/HDD/MM_projects",
    "work_tree_log_path": "/Volumes/HDD/MM_projects/block_heaven/.micro_mind/work_tree.jsonl",
}
```

Apply should use the same workflow and same node logic as simulation.

---

### 5. Log

Both simulation and real application must be logged.

Simulation log:

```text
/Volumes/HDD/MM_projects/.simulations/<project_slug>/<run_id>/logs/work_tree.jsonl
```

Real project log:

```text
/Volumes/HDD/MM_projects/<project_slug>/.micro_mind/work_tree.jsonl
```

The logs should allow comparison between planned, simulated and applied actions.

---

### 6. Memory

After successful apply, Micro Mind should store an execution memory record.

Memory should include:

- task
- workflow
- simulation result
- verification result
- apply result
- used nodes
- duration
- skipped nodes
- failed nodes
- human guidance if any

Failed simulations should also be stored because failures are learning material.

---

## Node Behavior Rule

Nodes should not know whether they are in simulation or real apply mode unless absolutely necessary.

Instead, nodes should receive context paths.

Example:

```python
node.execute(context)
```

The same node should work in both modes:

```text
Simulation context → writes to simulation workspace
Real context       → writes to real workspace
```

This keeps node behavior consistent and testable.

---

## Verification Before Apply

A workflow may be applied only when:

```text
simulation.status == completed or completed_with_skipped_nodes
verification.status == passed
forbidden_path_touched == false
critical_failures == []
```

If any critical check fails:

```text
status = waiting_for_human_guidance
```

or:

```text
status = simulation_failed
```

The real project must remain untouched.

---

## Human Guidance Rule

If the simulation result is uncertain, Micro Mind must stop and ask for human guidance.

Examples:

- Unknown node required
- Local model suggests an unsupported workflow
- Verification cannot prove safety
- The workflow would touch forbidden paths
- Confidence is below the required threshold

Micro Mind must not guess its way into the real project.

---

## Relationship With Local LLM

Local LLMs may suggest plans or classifications, but they must not directly apply changes.

Correct role:

```text
Local LLM = advisor
Micro Mind logic = decision layer
Human = teacher / final guide for uncertain cases
```

LLM output must go through:

```text
Local LLM suggestion
↓
Validation
↓
Simulation
↓
Verification
↓
Human approval when needed
↓
Apply
```

---

## Queue Rule

Multiple nodes must not spam the local model at the same time.

Local model requests should go through a queue.

Initial simple queue can be file-based:

```text
.micro_mind/model_queue/pending.jsonl
.micro_mind/model_queue/completed.jsonl
.micro_mind/model_queue/failed.jsonl
```

Redis is not required in the first version.

File-based queues are easier to debug, inspect and version during early development.

---

## Future Modules

The simulation-first model will likely introduce these modules:

```text
micro_mind/core/simulation/
├── simulation_runner.py
├── simulation_workspace.py
├── simulation_verifier.py
└── MODULE.md

micro_mind/core/apply/
├── apply_runner.py
└── MODULE.md
```

Potential future nodes:

```text
nodes/verification/project_structure_verifier_node.py
nodes/dependency/dependency_plan_verifier_node.py
nodes/code/code_test_node.py
```

---

## First Implementation Target

The first implementation should simulate only project structure creation.

Flow:

```text
ProjectCreationExecutionNetwork
↓
SimulationRunner
↓
ProjectStructureNode executes in simulation workspace
↓
ProjectStructure verification passes
↓
ProjectStructureNode executes in real workspace
↓
WorkTreeLogger records real actions
```

The first implementation does not need to run package installs or generated code tests.

---

## Current Decision

From this point forward, risky Micro Mind workflows should be designed as simulation-first.

A node may be unit tested directly, but a real workflow should not be applied to the real project workspace until simulation and verification pass.
