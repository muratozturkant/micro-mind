Micro Mind - Evolutionary Project Brain (Phase 1)

Vision

Micro Mind is not an LLM replacement.

Micro Mind is an evolutionary task execution and learning system that sits above LLMs, local models, tools and executors.

The goal is to create a living network of nodes that can:

- Learn procedures
- Execute tasks
- Remember successful workflows
- Forget useless workflows
- Create specialists
- Evolve over time

The first phase focuses only on project creation and project setup workflows.

⸻

Phase 1 Goal

Create a project from a user request.

Example:

User:

“Create a Flutter project called Block Heaven.”

Micro Mind should:

1. Ask required questions
2. Create folders
3. Run commands
4. Verify results
5. Save execution history
6. Learn from successful executions

No code generation intelligence is required in Phase 1.

Only task execution.

## Minimum Viable Organism (MVO)

The first working version of Micro Mind is not a coding system.

Its only responsibility is creating project structures.

Example:

User:

"Create a Flutter project called Block Heaven"

Execution chain:

RootPlanner
→ ProjectCreateNetwork
→ QuestionNode
→ DirectoryCreateNode
→ StructureVerifyNode
→ MemoryNode

Expected result:

projects/
└── block_heaven/
├── frontend/
├── backend/
├── database/
├── docs/
├── PROJECT_STATE.md
└── DEVELOPMENT_RULES.md

No Flutter commands yet.
No code generation yet.
No AI coding yet.

Only directory creation, verification and memory recording.

---

## Phase 1.1 Directory Creation Network

Node chain:

RootPlanner
↓
ProjectCreateNetwork
↓
QuestionNode
↓
DirectoryCreateNode
↓
StructureVerifyNode
↓
MemoryNode

Responsibilities:

QuestionNode

- Ask project name
- Ask project type
- Ask target directory

DirectoryCreateNode

- Create folders
- Create empty state files
- Create execution metadata

StructureVerifyNode

- Verify folders exist
- Verify files exist
- Produce verification result

MemoryNode

- Save execution JSON
- Save node statistics
- Save execution duration

---

## First Evolution Rules

Nodes start with life statistics.

Example:

activation_count
success_count
failure_count
last_execution
sleep_score
fitness_score

Node states:

ACTIVE

- Currently executing work

SLEEPING

- Not used recently
- Can be reactivated

PROMOTED

- High success rate
- Can manage child nodes

DEPRECATED

- Replaced by better nodes

ARCHIVED

- Removed from active network
- History preserved

---

## First Memory Record Example

{
"task": "create_project_structure",
"project_name": "block_heaven",
"result": "success",
"nodes": [
"QuestionNode",
"DirectoryCreateNode",
"StructureVerifyNode"
],
"duration_seconds": 3,
"created_directories": 4,
"created_files": 2
}

---

This is the first living organism stage.

The organism can:

- Ask questions
- Create folders
- Verify work
- Store memory

The organism cannot yet:

- Write code
- Use LLMs
- Deploy projects
- Create Flutter applications

Those abilities evolve in later phases.

## Phase 1.1 Python Usage

Micro Mind is Python-first in this phase and uses only the standard library.

Create a project structure:

```bash
python main.py create-project --name "Block Heaven" --type flutter --target ./projects
```

If your shell exposes Python as `python3`, use:

```bash
python3 main.py create-project --name "Block Heaven" --type flutter --target ./projects
```

The command normalizes the project name and creates:

```text
projects/
└── block_heaven/
    ├── frontend/
    ├── backend/
    ├── database/
    ├── docs/
    ├── PROJECT_STATE.md
    ├── DEVELOPMENT_RULES.md
    └── .micro_mind/
        ├── executions/
        └── nodes/
```

Each run prints a verification result. Running the same command again is safe:
existing folders and files are reused, while a new execution memory JSON is saved
under `.micro_mind/executions/` and node lifecycle statistics are updated under
`.micro_mind/nodes/`.

## Phase 1.2 Memory Summary Usage

Micro Mind can read saved project memory and print a JSON summary:

```bash
python3 main.py memory-summary --project /Volumes/HDD/MM_projects/block_heaven
```

The command reads:

```text
<project_root>/.micro_mind/executions/
<project_root>/.micro_mind/nodes/
```

The summary includes:

- `project_root`
- `total_executions`
- `successful_executions`
- `failed_executions`
- `last_execution`
- `tasks_seen`
- `node_stats`
- `most_used_nodes`
- `average_duration_seconds`

If `.micro_mind` or the memory folders are missing, the command returns an empty
summary instead of failing.

⸻

Core Architecture

Root Brain

The system starts from a Root Planner Node.

Responsibilities:

- Receive task
- Classify task
- Activate required networks
- Monitor execution
- Save results

Example:

Task:

Create Flutter Project

Activated chain:

RootPlanner
→ ProjectCreateNetwork
→ FlutterCreateNode
→ VerificationNode
→ MemoryNode

⸻

Node Types

Planner Nodes

Purpose:

Determine what should happen.

Examples:

- ProjectCreatePlanner
- ReleasePlanner
- DeployPlanner
- FirebaseSetupPlanner

⸻

Execution Nodes

Purpose:

Perform actions.

Examples:

- CreateDirectoryNode
- FlutterCreateNode
- GitInitNode
- NpmInstallNode

Execution nodes can:

- Read files
- Write files
- Execute commands
- Create folders
- Launch tools

⸻

Verification Nodes

Purpose:

Verify success.

Examples:

- FlutterProjectVerifier
- FirebaseVerifier
- ReleaseVerifier

Checks:

- Required files exist
- Commands succeeded
- Project structure is valid

⸻

Memory Nodes

Purpose:

Store experience.

Examples:

- Successful execution
- Failed execution
- Fix history
- Workflow history

Stored as structured JSON.

⸻

Observer Nodes

Purpose:

Observe execution.

Responsibilities:

- Track execution time
- Track failures
- Track repeated actions
- Detect unnecessary work

⸻

Reviewer Nodes

Purpose:

Review work produced by execution nodes.

Responsibilities:

- Detect mistakes
- Suggest improvements
- Approve workflow

⸻

Node Lifecycle

Every node has a lifecycle.

Birth

Node is created when:

- A new workflow appears
- A new recurring problem appears
- Existing nodes cannot solve a task

Example:

Repeated Firebase SHA1 problems

↓

FirebaseShaVerifierNode created

⸻

Active

Node is actively executing tasks.

Statistics collected:

- Activation count
- Success rate
- Failure rate
- Average execution time

⸻

Sleep

Inactive nodes enter sleep mode.

Conditions:

- Not used recently
- Low activation count

Sleeping nodes consume no resources.

⸻

Promotion

Successful nodes can evolve.

Example:

FlutterCreateNode

↓

FlutterProjectExpert

Conditions:

- High success rate
- High usage
- Low failure rate

⸻

Reproduction

Successful nodes can create child nodes.

Example:

FirebaseSetupNode

↓

FirebaseSetupNode_v2

↓

FirebaseProjectVerifierNode

⸻

Death

Nodes are removed when:

- Repeated failures
- Never used
- Replaced by better nodes

Dead nodes remain archived for analysis.

⸻

Evolution System

Every node receives a score.

Positive rewards:

- Task completed
- Validation passed
- Deployment successful
- Build successful

Negative rewards:

- Validation failed
- Wrong project structure
- Build failure
- Repeated mistakes

⸻

First Real Workflow

Task:

Create Flutter Project

Execution:

User Request
↓
Root Planner
↓
ProjectCreateNetwork
↓
QuestionNode
↓
ProjectName
PackageName
Directory
↓
CreateDirectoryNode
↓
FlutterCreateNode
↓
VerificationNode
↓
MemoryNode
↓
Workflow Complete

⸻

Memory Format

All executions are stored.

Example:

{
“task”: “create_flutter_project”,
“project_name”: “BlockHeaven”,
“package_name”: “com.wimlocs.blockheaven”,
“status”: “success”,
“duration_seconds”: 32,
“nodes_used”: [
“CreateDirectoryNode”,
“FlutterCreateNode”,
“VerificationNode”
]
}

⸻

Future Phases

Phase 2

- Firebase setup
- GitHub setup
- Git initialization
- Environment creation

Phase 3

- Deployment workflows
- Release workflows
- Google Play workflows
- App Store workflows

Phase 4

- Specialist node creation
- Node evolution
- Node tournaments
- Workflow optimization

Phase 5

- Micro Models
- Expert Networks
- Self-improving execution chains

Long-term goal:

Create a living software engineering organism capable of continuously learning, evolving and improving project workflows.

# Micro Mind

**An Evolutionary Execution Architecture for AI Systems**

Micro Mind is an experimental research project exploring whether AI execution systems can evolve like living organisms.

Instead of building a larger language model, Micro Mind investigates a persistent network of specialized execution nodes that can learn procedures, execute tasks, remember successful workflows, forget ineffective workflows, create specialists, and evolve over time.

Micro Mind is not an LLM replacement.

It is designed to sit above LLMs, local models, tools, command runners, project executors, and future agent systems.

---

## Core Idea

Modern AI systems are powerful, but most of them are transient.

Every new session often starts from zero.
Every workflow is rediscovered.
Successful execution patterns are not naturally preserved as living behavior.

Micro Mind starts from a different question:

> If an AI system truly learns, why should it be reborn from scratch after every task?

The inspiration comes from biological evolution.

The earliest organisms were not intelligent because they had large brains. They survived because they could react, remember, adapt, preserve successful behavior, and discard unsuccessful behavior.

Micro Mind applies this idea to software execution workflows.

---

## What Micro Mind Is

Micro Mind is an evolutionary task execution and learning system.

Its long-term goal is to create a living software engineering organism capable of:

- Learning repeatable procedures
- Executing software tasks through specialized nodes
- Remembering successful workflows
- Forgetting or archiving useless workflows
- Creating specialist nodes
- Measuring node fitness
- Evolving execution chains over time

---

## What Micro Mind Is Not

Micro Mind is currently **not**:

- A replacement for GPT, Claude, Gemini, Qwen, Llama, or any other LLM
- A general-purpose coding agent
- A code generation engine
- A deployment platform
- A commercial SaaS product

At this stage, Micro Mind is a research prototype focused on persistent execution memory and evolutionary workflow growth.

---

## Current Stage

**Phase:** 1  
**Status:** Active Research Prototype  
**Current Capability:** Project structure creation, verification, and memory recording

The first working version of Micro Mind is intentionally small.

It behaves like a minimal digital organism.

It can:

- Ask required project questions
- Create a project folder structure
- Verify the created structure
- Save execution history
- Update basic node lifecycle statistics
- Read saved memory and summarize past executions

It cannot yet:

- Generate application code
- Create real Flutter projects
- Deploy software
- Use LLMs as active planners
- Run full release workflows

Those abilities are planned for later phases.

---

## Minimum Viable Organism

The first organism only creates project structures.

Example request:

```text
Create a Flutter project called Block Heaven.
```

Execution chain:

```text
RootPlanner
→ ProjectCreateNetwork
→ QuestionNode
→ DirectoryCreateNode
→ StructureVerifyNode
→ MemoryNode
```

Expected result:

```text
projects/
└── block_heaven/
    ├── frontend/
    ├── backend/
    ├── database/
    ├── docs/
    ├── PROJECT_STATE.md
    ├── DEVELOPMENT_RULES.md
    └── .micro_mind/
        ├── executions/
        └── nodes/
```

This is the first living organism stage.

It does not write code yet.  
It only creates, verifies, remembers, and updates its own node statistics.

---

## Quick Start

Micro Mind is Python-first in Phase 1 and currently uses only the Python standard library.

Create a project structure:

```bash
python3 main.py create-project \
  --name "Block Heaven" \
  --type flutter \
  --target ./projects
```

If your shell exposes Python as `python`, use:

```bash
python main.py create-project \
  --name "Block Heaven" \
  --type flutter \
  --target ./projects
```

The command normalizes the project name, creates the directory structure, verifies the result, saves an execution memory JSON, and updates node statistics.

Running the same command again is safe. Existing folders and files are reused while a new execution memory record is saved.

---

## Memory Summary

Micro Mind can read saved project memory and print a JSON summary:

```bash
python3 main.py memory-summary --project ./projects/block_heaven
```

The command reads:

```text
<project_root>/.micro_mind/executions/
<project_root>/.micro_mind/nodes/
```

The summary includes:

- Project root
- Total executions
- Successful executions
- Failed executions
- Last execution
- Tasks seen
- Node statistics
- Most used nodes
- Average duration

If `.micro_mind` or memory folders are missing, the command returns an empty summary instead of failing.

---

## Node Types

### Planner Nodes

Planner nodes decide what should happen.

Examples:

- RootPlanner
- ProjectCreatePlanner
- ReleasePlanner
- DeployPlanner
- FirebaseSetupPlanner

### Execution Nodes

Execution nodes perform actions.

Examples:

- DirectoryCreateNode
- FlutterCreateNode
- GitInitNode
- NpmInstallNode

Execution nodes may eventually read files, write files, execute commands, create folders, and launch tools.

### Verification Nodes

Verification nodes check whether a task succeeded.

Examples:

- StructureVerifyNode
- FlutterProjectVerifier
- FirebaseVerifier
- ReleaseVerifier

### Memory Nodes

Memory nodes store experience.

Examples:

- Successful executions
- Failed executions
- Fix history
- Workflow history
- Node statistics

### Observer Nodes

Observer nodes monitor execution quality.

They may track execution time, repeated failures, unnecessary work, and performance patterns.

### Reviewer Nodes

Reviewer nodes review produced work, detect mistakes, suggest improvements, and approve or reject workflow results.

---

## Node Lifecycle

Every node has a lifecycle.

### Birth

A node is created when a new workflow appears, a recurring problem is detected, or existing nodes cannot solve a task.

### Active

The node is currently executing work.

Tracked statistics may include:

- Activation count
- Success count
- Failure count
- Last execution time
- Sleep score
- Fitness score

### Sleep

Inactive nodes can enter sleep mode.

Sleeping nodes remain available but consume no active execution attention.

### Promotion

Successful nodes can become more important or manage child nodes.

Example:

```text
FlutterCreateNode
→ FlutterProjectExpert
```

### Reproduction

Successful nodes may produce specialized child nodes.

Example:

```text
FirebaseSetupNode
→ FirebaseSetupNode_v2
→ FirebaseProjectVerifierNode
```

### Deprecation

A node can be deprecated when it is replaced by a better node.

### Archive

Failed, unused, or replaced nodes are removed from the active network while their history is preserved for analysis.

---

## Evolution System

Each node receives feedback from execution results.

Positive signals:

- Task completed
- Validation passed
- Build succeeded
- Deployment succeeded
- Workflow reused successfully

Negative signals:

- Validation failed
- Wrong project structure
- Build failure
- Repeated mistakes
- Unnecessary work

Over time, Micro Mind should learn which workflows deserve to survive, which should sleep, which should evolve, and which should be archived.

---

## Memory Record Example

```json
{
  "task": "create_project_structure",
  "project_name": "block_heaven",
  "project_type": "flutter",
  "result": "success",
  "nodes_used": [
    "QuestionNode",
    "DirectoryCreateNode",
    "StructureVerifyNode",
    "MemoryNode"
  ],
  "duration_seconds": 0.003,
  "created_directories": 7,
  "created_files": 2
}
```

---

## Research Roadmap

### Phase 1 — Project Creation Organism

- Project structure creation
- Structure verification
- Execution memory
- Node lifecycle statistics
- Memory summary reader

### Phase 2 — Tool Learning

- Git initialization
- GitHub setup
- Flutter project creation
- Node.js project creation
- Environment file creation
- Command execution history

### Phase 3 — Workflow Execution

- Firebase setup workflows
- Docker setup workflows
- Deployment workflows
- Release workflows
- Google Play / App Store preparation workflows

### Phase 4 — Specialist Nodes

- Specialist node creation
- Node promotion
- Node sleep and reactivation
- Node tournaments
- Workflow optimization

### Phase 5 — Micro Models

- Local model integration
- Task-specific expert models
- Model jury evaluation
- Prompt minimization
- Execution planning

### Phase 6 — Digital Organism

- Persistent evolutionary execution network
- Self-improving workflow chains
- Long-term memory
- Specialist reproduction
- Continuous software engineering assistance

---

## Long-Term Vision

The long-term goal is not to create a bigger model.

The goal is to create a living software engineering organism that continuously learns, evolves, specializes, and improves project workflows over time.

Micro Mind explores a future where AI systems do not simply answer questions, but build persistent execution experience across years of real work.

---

## Repository Structure

```text
micro_mind/
├── docs/
│   └── ARCHITECTURE.md
├── micro_mind/
│   ├── cli/
│   ├── core/
│   └── nodes/
├── tests/
├── main.py
├── readme.md
└── .gitignore
```

---

## License

License will be added later.

---

## Author

Created by **Murat Öztürk** as an independent AI research project.

Micro Mind is being developed from İzmir, Türkiye, using a local-first AI and software engineering environment.
