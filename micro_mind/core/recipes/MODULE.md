# Core Recipes Module

## Purpose

This module owns reusable workflow knowledge.

A recipe is a verified, reusable description of how Micro Mind should perform a known task without asking the model again.

Recipes are how Micro Mind learns.

The first time a task is unknown, Micro Mind may ask micro questions, normalize facts, simulate a task chain and wait for human guidance.

After a successful simulation/apply cycle, the result can become a recipe candidate.

Once a recipe is approved and stored, future similar tasks should use the recipe instead of spending tokens on the same questions again.

---

## Core Rule

```text
Ask once.
Simulate.
Verify.
Apply.
Remember.
Reuse.
```

Recipes reduce future local model usage.

They also make Micro Mind more deterministic over time.

---

## Files

### recipe_store.py

Owns file-based recipe persistence.

Current expected responsibilities:

- Save recipe JSON files
- Load recipe JSON files
- List available recipes
- Avoid database dependency in the first version
- Keep recipes readable and versionable

Initial storage should be file-based.

Example path:

```text
.micro_mind/recipes/nodejs_backend_basic_v1.json
```

---

### recipe_matcher.py

Owns matching a new task or normalized facts against stored recipes.

Current expected responsibilities:

- Search recipes by task type
- Search recipes by tags
- Search recipes by normalized facts
- Return best match candidates
- Avoid LLM calls for known tasks

The matcher should return candidates, not execute them.

---

### recipe_builder.py

Owns building recipe candidates from successful simulation/apply results.

Current expected responsibilities:

- Read simulation report
- Read apply simulation report
- Preserve micro questions
- Preserve normalized facts
- Preserve micro tasks
- Preserve project tree records when available
- Create a recipe candidate JSON
- Mark recipe as unapproved by default

Recipe candidates should require human approval before becoming reusable recipes.

---

## Recipe Lifecycle

```text
Unknown task
↓
Micro questions
↓
Local AI fact collection
↓
Normalization
↓
Micro task chain
↓
Simulation
↓
Apply simulation
↓
Real apply later
↓
Verification
↓
Recipe candidate
↓
Human approval
↓
Stored recipe
↓
Future reuse without model call
```

---

## Recipe Shape

Example recipe:

```json
{
  "recipe_id": "nodejs_backend_basic_v1",
  "status": "candidate",
  "approved": false,
  "task_family": "nodejs_backend_api",
  "title": "Basic Node.js Backend API",
  "description": "Creates a basic Express backend API skeleton.",
  "tags": ["nodejs", "express", "backend_api"],
  "facts": {
    "dependencies": ["express", "dotenv", "cors"],
    "directories": ["src", "src/routes", "src/controllers", "src/config"],
    "files": ["src/app.js", "package.json"]
  },
  "micro_tasks": [],
  "verification": {
    "status": "pending"
  },
  "source": {
    "created_from": "simulation_report",
    "requires_human_approval": true
  }
}
```

---

## Inputs

The recipes module may receive:

- user task text
- normalized facts
- micro task chains
- simulation reports
- apply simulation reports
- verification reports
- human approval metadata

---

## Outputs

The recipes module may produce:

- recipe candidates
- stored recipes
- recipe match candidates
- recipe lists
- recipe load results

---

## Rules

- Recipes must not execute tasks directly.
- Recipes must not write project files directly.
- Recipes must not call local AI directly.
- Recipes must not run shell commands.
- Recipes must not deploy projects.
- Recipes must be inspectable JSON.
- Recipes must preserve enough information to reproduce the task chain.
- Recipe candidates must not become trusted recipes without approval.
- Failed or unverified runs should not become approved recipes.
- Matching should prefer deterministic metadata before model calls.

---

## Relationship With Other Modules

### core/micro_task

Produces micro questions, normalized facts, micro task chains and simulation reports that can become recipe candidates.

### core/apply

Produces apply plans and apply simulation reports that help determine whether a recipe is safe.

### core/model_queue

May provide local AI response history, but recipes should reduce future queue usage.

### core/decision

May ask the recipe matcher before deciding whether local AI is needed.

### core/logging

Work tree logs can later enrich recipes with file-level provenance.

---

## Current Decision

The recipes module is the learning memory of Micro Mind.

The goal is not only to solve one task.

The goal is to turn a successful task into reusable structured knowledge.

```text
Model helps once.
Recipe helps forever.
```
