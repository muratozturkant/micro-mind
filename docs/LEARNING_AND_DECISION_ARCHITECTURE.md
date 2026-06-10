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
Micro Question Builder
↓
Local AI Fact Collector
↓
Raw Fact Normalizer
↓
Task Decomposer
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

## Layer 4 — Micro Question Builder

The system should not ask broad questions when a smaller question is enough.

Bad broad question:

```text
Classify task: Create Fastify API with Redis cache
```

This produces model-specific answers such as:

```text
software_development
backend_development
Backend Development
feature_implementation
```

Those are useful signals, but they are not stable enough to directly drive Micro Mind workflows.

Instead, Micro Mind should split a macro task into micro questions.

Example macro task:

```text
Create Fastify API with Redis cache
```

Example micro questions:

```text
For a Node.js Fastify backend API with Redis cache, which npm packages are typically required?
```

```text
For Node.js Fastify API with Redis cache, list required implementation steps as compact JSON. No descriptions. Max 8 steps.
```

Micro questions should ask for one small fact or one small list.

---

## Layer 5 — Local AI Fact Collector

The local model is used only when deterministic logic and memory are not enough.

The local model is a fact collector, not the authority.

Allowed local AI tasks:

- answer one specific micro question
- extract required packages
- list compact implementation steps
- identify technologies mentioned in a task
- suggest missing facts needed for planning
- explain why a task is unfamiliar

Not allowed:

- directly applying file changes
- directly running commands
- bypassing simulation
- deciding final workflow alone
- using cloud fallback automatically
- being trusted to know Micro Mind's internal enum names

---

## Layer 6 — Raw Fact Normalizer

AI providers and local models will return different shapes for the same question.

Example Gemini-style response:

```json
{
  "task_type": "Backend Development",
  "technologies": ["Fastify", "Redis", "Node.js"],
  "action": "Create API with caching"
}
```

Example Copilot-style response:

```json
{
  "task": "Create Fastify API with Redis cache",
  "classification": {
    "category": "backend_development",
    "subcategories": ["api_development", "caching", "infrastructure"],
    "technologies": ["fastify", "redis", "node.js"],
    "complexity": "medium",
    "type": "feature_implementation"
  }
}
```

Example local model response:

```json
{
  "task_type": "software_development",
  "category": "backend_development",
  "description": "Create a Fastify API with Redis cache",
  "tags": ["fastify", "redis", "api", "caching", "node.js"]
}
```

The normalizer converts these raw facts into Micro Mind's canonical internal representation.

Example canonical output:

```json
{
  "task_type": "backend_api",
  "runtime": "nodejs",
  "framework": "fastify",
  "cache": "redis",
  "technologies": ["fastify", "redis", "nodejs"],
  "confidence": 0.82
}
```

The AI does not need to know this canonical schema.

Micro Mind owns normalization.

---

## Layer 7 — Task Decomposer

The task decomposer converts normalized facts into an ordered task chain.

Example normalized facts:

```json
{
  "task_type": "backend_api",
  "runtime": "nodejs",
  "framework": "fastify",
  "cache": "redis"
}
```

Example task chain:

```text
task_0: backend_project_setup
task_0.1: prepare_node_runtime
task_0.2: create_project_structure
task_0.3: install_fastify
task_0.4: install_redis_client
task_0.5: create_fastify_app
task_0.6: create_redis_connection
task_0.7: integrate_cache_layer
task_0.8: verify_backend_boot
```

Everything becomes a chain.

If information is missing, the decomposer should add an information request task instead of guessing.

Example:

```text
task_0.4: ask_required_redis_connection_details
```

The decomposer does not apply changes. It only builds task chains.

---

## Layer 8 — Validation

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

## Layer 9 — Simulation

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

## Layer 10 — Human Guidance

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
Micro Question Builder creates specific questions
↓
Local AI Fact Collector gathers raw facts
↓
Raw Fact Normalizer converts facts to canonical representation
↓
Task Decomposer builds task chain
↓
Validation checks chain safety
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

Also:

```text
Do not spend tokens teaching every model Micro Mind's private enum schema.
Ask smaller factual questions and normalize the answers locally.
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

micro_mind/core/normalization/
├── ai_response_normalizer.py
├── task_decomposer.py
├── micro_question_builder.py
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
Micro questions third.
Local AI fact collection fourth.
Normalize locally.
Decompose into task chains.
Human guidance when uncertain.
Simulation before apply.
```
