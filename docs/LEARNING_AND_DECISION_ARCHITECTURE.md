# Learning and Decision Architecture

This document defines how Micro Mind decides what to do, how it learns new workflows, and when it asks for help.

Micro Mind is not designed to be a fast guessing agent.

Micro Mind is designed to be:

1. Learnable
2. Consistent
3. Economical
4. Inspectable
5. Safe to extend

The core idea:

```text
Micro Mind does not guess.
Micro Mind remembers.
If it cannot remember, it searches its experience.
If experience is not enough, it asks a local advisor.
If the answer is still uncertain, it waits for human guidance.
```

---

## Core Decision Law

Final decisions must stay inside Micro Mind's logic layer.

Local LLMs may advise, classify or suggest.

They must not directly apply changes.

```text
LLM = advisor
Micro Mind logic = decision layer
Human = teacher for uncertain cases
```

This keeps the system consistent, debuggable and economical.

---

## Decision Stack

Every task should move through the following stack:

```text
User Task
↓
Known Recipe Search
↓
Species Knowledge
↓
Memory Search
↓
Local AI Advisor
↓
Validation
↓
Simulation
↓
Human Guidance if needed
↓
Apply
↓
Memory Update
```

Not every task must reach every layer.

If a known recipe exists, Micro Mind should not ask the local model.

---

## Layer 1 — Known Recipe Search

Recipes are reusable workflow definitions.

A recipe is a known solution for a known task type.

Example recipe:

```json
{
  "recipe_id": "nodejs_express_mongodb_jwt_api",
  "description": "Create a Node.js Express API with MongoDB and JWT authentication",
  "matches": {
    "runtime": "nodejs",
    "framework": "express",
    "database": "mongodb",
    "auth": "jwt"
  },
  "workflow": [
    "analyze_task",
    "create_project_structure",
    "install_dependencies",
    "create_mongo_connection",
    "create_user_model",
    "create_jwt_service",
    "create_auth_middleware",
    "create_register_route",
    "create_login_route",
    "create_protected_route",
    "verify_api",
    "save_memory"
  ]
}
```

If a recipe matches confidently, use it.

No local LLM call is needed.

---

## Layer 2 — Species Knowledge

Species knowledge is the built-in expertise of specialist nodes.

Examples:

### DependencyNode

Knows that:

```text
Express → express, cors
MongoDB → mongoose
JWT → jsonwebtoken, bcryptjs
Environment config → dotenv
```

### ProjectStructureNode

Knows how to create:

```text
frontend/
backend/
database/
docs/
PROJECT_STATE.md
DEVELOPMENT_RULES.md
```

Species knowledge should be deterministic whenever possible.

It should not call an LLM for simple known behavior.

---

## Layer 3 — Memory Search

If no direct recipe exists, Micro Mind should search previous memories.

Memory can answer questions like:

```text
Have we done something similar before?
Which workflow succeeded?
Which nodes failed?
Which human guidance fixed it?
```

Memory search should produce candidates, not final decisions.

Example memory candidate:

```json
{
  "memory_id": "exec_2026_06_10_001",
  "similarity": 0.82,
  "task": "Create Node.js Express MongoDB API",
  "successful_workflow": [
    "create_project_structure",
    "install_dependencies",
    "create_mongo_connection"
  ]
}
```

The logic layer decides whether the memory is close enough to reuse.

---

## Layer 4 — Local AI Advisor

The local model is used only when deterministic logic and memory are not enough.

The local model is an advisor, not the authority.

Allowed local AI tasks:

- classify an unknown task
- extract technologies
- suggest a workflow candidate
- explain why a task is unfamiliar
- suggest which existing species may be relevant

Not allowed:

- directly applying file changes
- directly running commands
- bypassing simulation
- deciding final workflow alone
- using cloud fallback automatically

---

## Local AI Request Rules

For `ik_llama.cpp`, calls should use low-cost deterministic settings.

Known working pattern:

```json
{
  "temperature": 0,
  "max_tokens": 128,
  "chat_template_kwargs": {
    "enable_thinking": false
  }
}
```

Reason:

- `enable_thinking=false` prevents long reasoning output.
- `temperature=0` improves consistency.
- low `max_tokens` keeps response economical.
- JSON-only prompts are easier to validate.

The local model should return compact JSON.

Example output:

```json
{
  "task_type": "backend_api",
  "runtime": "nodejs",
  "framework": "express",
  "database": "mongodb",
  "auth": "jwt",
  "confidence": 0.86
}
```

---

## Layer 5 — Validation

Every AI suggestion must be validated before it can be used.

Validation checks:

- Is the JSON valid?
- Are fields known?
- Are workflow steps supported?
- Are node names registered?
- Is confidence high enough?
- Does it touch forbidden paths?
- Does it require unsupported commands?

If validation fails:

```text
status = waiting_for_human_guidance
```

or:

```text
status = rejected_ai_suggestion
```

---

## Layer 6 — Simulation

Even validated plans should not directly touch the real project.

They must go through simulation-first execution.

See:

```text
docs/SIMULATION_FIRST_EXECUTION.md
```

Required flow:

```text
Validated plan
↓
Simulation workspace
↓
Verification
↓
Apply to real workspace only if safe
```

---

## Layer 7 — Human Guidance

Human guidance is not a failure.

It is how Micro Mind learns safely.

The system should ask for human guidance when:

- no recipe exists
- no memory match is strong enough
- local AI response is invalid
- local AI confidence is too low
- validation fails
- simulation fails
- workflow contains unknown nodes
- the system cannot prove safety

Human guidance should be stored as learning material.

Example:

```json
{
  "status": "waiting_for_human_guidance",
  "reason": "unknown_workflow_step",
  "question": "Which node should handle create_redis_cache_layer?",
  "context": {
    "task": "Create Fastify API with Redis cache"
  }
}
```

---

## Queue Rule for Local AI

Multiple nodes must not call the local model at the same time.

All local model requests must pass through a queue.

Initial queue can be file-based:

```text
.micro_mind/model_queue/
├── pending.jsonl
├── processing.jsonl
├── completed.jsonl
└── failed.jsonl
```

Redis is not required in the first version.

File-based queues are preferred early because they are:

- inspectable
- simple
- cheap
- easy to debug
- easy to preserve in project history

Redis may be added later if concurrency or multi-worker coordination becomes necessary.

---

## Suggested Local AI Queue Entry

```json
{
  "request_id": "local_ai_2026_06_10_001",
  "created_at": "2026-06-10T10:00:00Z",
  "request_type": "task_classification",
  "status": "pending",
  "model_endpoint": "http://192.168.1.197:18080/v1/chat/completions",
  "payload": {
    "task": "Create Fastify API with Redis cache"
  },
  "constraints": {
    "temperature": 0,
    "max_tokens": 128,
    "enable_thinking": false,
    "response_format": "json_only"
  }
}
```

---

## Suggested Local AI Response Record

```json
{
  "request_id": "local_ai_2026_06_10_001",
  "completed_at": "2026-06-10T10:00:04Z",
  "status": "completed",
  "raw_response": {},
  "parsed_response": {
    "task_type": "backend_api",
    "runtime": "nodejs",
    "framework": "fastify",
    "cache": "redis",
    "confidence": 0.74
  },
  "validation": {
    "status": "requires_human_guidance",
    "reason": "no_known_recipe_for_fastify_redis"
  }
}
```

---

## Recipe Creation From Human Guidance

When a human resolves an unknown task, Micro Mind should be able to turn that guidance into a new recipe candidate.

Flow:

```text
Unknown task
↓
Human guidance
↓
Simulation
↓
Verification
↓
Successful apply
↓
Recipe candidate created
↓
Human approval
↓
Recipe saved
```

Recipes should not be created from failed or unverified workflows.

---

## Recipe Storage

Initial recipe storage can be file-based.

Suggested structure:

```text
.micro_mind/recipes/
├── nodejs_express_mongodb_jwt_api.json
├── flutter_basic_project.json
└── README.md
```

Later, recipes can be moved to a database if needed.

File-based recipes are preferred first because they are:

- easy to inspect
- easy to diff
- easy to edit manually
- easy to version
- cheap to maintain

---

## Memory Storage

Initial memory storage can stay file-based or JSONL-based.

Suggested structure:

```text
.micro_mind/memory/
├── executions.jsonl
├── failures.jsonl
├── human_guidance.jsonl
└── summaries.jsonl
```

Memory and recipes are different:

```text
Recipe = known reusable workflow
Memory = historical execution experience
```

---

## Confidence Rules

Suggested thresholds:

```text
confidence >= 0.90
↓
May become candidate for simulation

0.70 <= confidence < 0.90
↓
Requires human approval before simulation

confidence < 0.70
↓
Reject and ask human guidance
```

These thresholds are starting values and can evolve later.

---

## Unknown Task Behavior

When the task is unknown:

```text
Unknown task
↓
Recipe search fails
↓
Species knowledge fails
↓
Memory search has no strong match
↓
Local AI advisor creates suggestion
↓
Suggestion is validated
↓
If valid but uncertain → human guidance
↓
If invalid → human guidance
```

The system must not invent unsupported behavior.

---

## Known Task Behavior

When the task is known:

```text
Known task
↓
Recipe or deterministic species handles it
↓
No local AI call
↓
Simulation
↓
Verification
↓
Apply
↓
Memory update
```

Known tasks should be fast and deterministic.

---

## Economic Rule

Local AI calls are not free.

They cost:

- time
- CPU/GPU resources
- queue delay
- debugging complexity

Therefore:

```text
Do not ask the model what deterministic code already knows.
```

---

## Current Implementation Direction

The next likely modules are:

```text
micro_mind/core/decision/
├── decision_engine.py
├── recipe_store.py
├── memory_search.py
└── MODULE.md

micro_mind/core/species/
├── local_llama_species.py
├── local_model_queue.py
└── MODULE.md
```

But before implementing local model integration, the first target should be:

```text
Recipe search
↓
Known workflow decision
↓
Simulation-first execution
```

This keeps Micro Mind deterministic before adding model-based advice.

---

## Current Decision

Micro Mind should not become an agent that guesses.

Micro Mind should become an organism that learns.

The correct order is:

```text
Recipes first.
Memory second.
Local AI advisor third.
Human guidance when uncertain.
Simulation before apply.
```
