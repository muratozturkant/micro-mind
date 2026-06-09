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
