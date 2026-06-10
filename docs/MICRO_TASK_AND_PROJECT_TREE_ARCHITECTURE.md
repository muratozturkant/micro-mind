# Micro Task and Project Tree Architecture

This document defines how Micro Mind should decompose software work into very small tasks and map every task to a clear project tree location.

The goal is not to generate large blocks of code quickly.

The goal is to build software as a traceable hierarchy of tiny, verifiable steps.

---

## Core Principle

```text
One file = one clear responsibility when possible.
One route = one file.
One controller action = one file.
One import update = one task.
One verification = one task.
```

Micro Mind should not treat a feature as one large coding operation.

It should treat a feature as a chain of small operations.

---

## Why Micro Tasks?

Large tasks hide errors.

Small tasks expose them.

If a large generated feature fails, the system may not know where the problem is.

If every operation is tiny, the failure location becomes obvious.

Example:

```text
write controller file
↓
verify controller file
↓
write route file
↓
verify route file
↓
add route import to app.js
↓
verify app wiring
```

If the route fails, Micro Mind knows the problem is probably in:

```text
src/routes/<route>.route.js
```

or in the import wiring task.

It does not need to inspect the whole project.

---

## Slow Start, Fast Learning

The first time Micro Mind learns a workflow, it may ask many small questions.

This is expected.

Example first run:

```text
What base packages are needed?
Which files should exist?
What should app.js contain?
What should a route file contain?
What should a controller action contain?
Where should imports be added?
How should this be verified?
```

This may feel slow at the beginning.

But once the answers are validated, simulated and applied successfully, they become reusable recipe and memory material.

The next time, Micro Mind should not ask the model again for the same known step.

```text
Ask once.
Verify.
Apply.
Remember.
Reuse.
```

---

## AI Role

The local model should not generate whole features.

It should answer very small, specific questions.

Bad question:

```text
Create a Node.js backend API.
```

Better question:

```text
For a basic Node.js backend API setup, list required npm packages as compact JSON only.
```

Better question:

```text
For an Express app.js file, what minimal imports are required for express, cors and dotenv?
```

Better question:

```text
For a GET /health endpoint, what should the controller function return?
```

The smaller the question, the easier it is to normalize, verify and reuse.

---

## Project Tree as Knowledge Graph

Micro Mind should treat the project tree as a knowledge graph.

A file is not just a file.

A file is a node in the project graph.

Example project tree node:

```json
{
  "path": "src/controllers/health/getHealth.controller.js",
  "type": "controller_action",
  "purpose": "GET health endpoint response controller",
  "created_by_task": "task_0.18",
  "imports_required": [],
  "imported_by": ["src/routes/health.route.js"],
  "verified_by": "task_0.19"
}
```

This allows Micro Mind to know:

- why a file exists
- which task created it
- which file imports it
- which verification checks it
- where to modify it later

---

## Example: Basic Node.js Backend API

Macro task:

```text
Create a basic Node.js backend API.
```

Micro Mind should not jump directly to full code generation.

It should create a chain.

---

## Step Group 0 — Base Setup

```text
task_0: create_basic_nodejs_backend_api
```

### task_0.1 — Ask base packages

Question:

```text
For a basic Node.js backend API setup, list the required npm packages as compact JSON only. No descriptions. No Redis. No database-specific packages unless essential.
```

Observed local model answer:

```json
["express", "dotenv", "cors"]
```

### task_0.2 — Normalize package answer

Canonical fact:

```json
{
  "dependencies": ["express", "dotenv", "cors"]
}
```

### task_0.3 — Create package install tasks

```text
task_0.3.1: install_express
task_0.3.2: install_dotenv
task_0.3.3: install_cors
```

### task_0.4 — Verify package installation

```text
task_0.4.1: verify_package_json_contains_express
task_0.4.2: verify_package_json_contains_dotenv
task_0.4.3: verify_package_json_contains_cors
```

---

## Step Group 1 — Project Tree Discovery

### task_1.1 — Ask required files and directories

Question:

```text
For a basic Node.js backend API setup, list the recommended project structure as compact JSON only. Max 10 directories or files. No descriptions.
```

Observed local model answer:

```json
[
  "src",
  "src/app.js",
  "src/routes",
  "src/controllers",
  "src/middleware",
  "src/config",
  "src/models",
  "package.json",
  "README.md",
  ".gitignore"
]
```

### task_1.2 — Normalize project structure

Canonical fact:

```json
{
  "directories": [
    "src",
    "src/routes",
    "src/controllers",
    "src/middleware",
    "src/config",
    "src/models"
  ],
  "files": ["src/app.js", "package.json", "README.md", ".gitignore"]
}
```

### task_1.3 — Create directory tasks

```text
task_1.3.1: create_src_directory
task_1.3.2: create_routes_directory
task_1.3.3: create_controllers_directory
task_1.3.4: create_middleware_directory
task_1.3.5: create_config_directory
task_1.3.6: create_models_directory
```

### task_1.4 — Create file tasks

```text
task_1.4.1: create_src_app_js
task_1.4.2: create_package_json
task_1.4.3: create_readme_md
task_1.4.4: create_gitignore
```

### task_1.5 — Verify tree tasks

```text
task_1.5.1: verify_src_directory
task_1.5.2: verify_routes_directory
task_1.5.3: verify_controllers_directory
task_1.5.4: verify_middleware_directory
task_1.5.5: verify_config_directory
task_1.5.6: verify_models_directory
task_1.5.7: verify_src_app_js
task_1.5.8: verify_package_json
task_1.5.9: verify_readme_md
task_1.5.10: verify_gitignore
```

---

## Step Group 2 — File Responsibility Discovery

### task_2.1 — Ask file responsibilities

Question:

```text
For a basic Node.js backend API setup with Express, list the purpose of each file or directory as compact JSON only. Use this list: src, src/app.js, src/routes, src/controllers, src/middleware, src/config, src/models, package.json, README.md, .gitignore. No descriptions longer than 8 words.
```

Observed local model answer:

```json
{
  "src": "Application source code directory",
  "src/app.js": "Main application entry point",
  "src/routes": "API endpoint definitions",
  "src/controllers": "Request handling logic",
  "src/middleware": "Request processing utilities",
  "src/config": "Environment and app settings",
  "src/models": "Database schema definitions",
  "package.json": "Project dependencies and scripts",
  "README.md": "Project documentation and setup",
  ".gitignore": "Files excluded from version control"
}
```

### task_2.2 — Create project tree knowledge records

Example records:

```json
[
  {
    "path": "src/app.js",
    "type": "app_entry",
    "purpose": "Main application entry point"
  },
  {
    "path": "src/routes",
    "type": "routes_directory",
    "purpose": "API endpoint definitions"
  },
  {
    "path": "src/controllers",
    "type": "controllers_directory",
    "purpose": "Request handling logic"
  }
]
```

---

## Step Group 3 — app.js Creation

The system should not ask for the whole API.

It should ask only about `src/app.js`.

### task_3.1 — Ask app.js imports

Question:

```text
For a minimal Express src/app.js using express, cors and dotenv, list only required imports as compact JSON.
```

Expected kind of answer:

```json
["express", "cors", "dotenv/config"]
```

### task_3.2 — Ask app.js minimal wiring

Question:

```text
For minimal Express src/app.js, list required setup statements as compact JSON. No route code.
```

Expected kind of answer:

```json
[
  "create express app",
  "enable cors middleware",
  "enable json body parser",
  "export app"
]
```

### task_3.3 — Write app.js file

This is a file write task.

```text
task_3.3: write_src_app_js
```

### task_3.4 — Verify app.js file

This is a verification task.

```text
task_3.4.1: verify_app_js_exists
task_3.4.2: verify_app_js_imports_express
task_3.4.3: verify_app_js_imports_cors
task_3.4.4: verify_app_js_exports_app
```

---

## Step Group 4 — Health Route

A route should be decomposed into separate files and tasks.

Example route:

```text
GET /health
```

### task_4.1 — Ask controller file path

Question:

```text
For GET /health in an Express API with separate controller actions, what controller file path should be used? Return one JSON string only.
```

Expected kind of answer:

```json
"src/controllers/health/getHealth.controller.js"
```

### task_4.2 — Ask controller function behavior

Question:

```text
For GET /health controller in Express, what should the function return? Compact JSON only. No full file.
```

Expected kind of answer:

```json
{
  "statusCode": 200,
  "body": {
    "status": "ok"
  }
}
```

### task_4.3 — Write controller action file

```text
task_4.3: write_get_health_controller_file
```

### task_4.4 — Verify controller action file

```text
task_4.4.1: verify_get_health_controller_exists
task_4.4.2: verify_get_health_controller_exports_function
task_4.4.3: verify_get_health_controller_returns_status_ok
```

### task_4.5 — Ask route file path

Question:

```text
For GET /health in an Express API, what route file path should import the controller? Return one JSON string only.
```

Expected kind of answer:

```json
"src/routes/health.route.js"
```

### task_4.6 — Write route file

```text
task_4.6: write_health_route_file
```

### task_4.7 — Verify route file

```text
task_4.7.1: verify_health_route_exists
task_4.7.2: verify_health_route_imports_get_health_controller
task_4.7.3: verify_health_route_registers_get_health_endpoint
```

### task_4.8 — Add route import to app.js

This is not the same task as writing the route file.

```text
task_4.8: add_health_route_import_to_app_js
```

### task_4.9 — Mount route in app.js

This is not the same task as importing the route.

```text
task_4.9: mount_health_route_in_app_js
```

### task_4.10 — Verify app route wiring

```text
task_4.10.1: verify_app_imports_health_route
task_4.10.2: verify_app_mounts_health_route
```

---

## Import Tasks Are Separate Tasks

Writing a file and importing that file somewhere else are different responsibilities.

Example:

```text
write_get_health_controller_file
```

is separate from:

```text
import_get_health_controller_into_health_route
```

And:

```text
write_health_route_file
```

is separate from:

```text
import_health_route_into_app_js
```

This makes dependency wiring visible and debuggable.

---

## Verification Tasks Are Separate Tasks

Every meaningful write should have a verification task.

Examples:

```text
write_src_app_js
↓
verify_src_app_js
```

```text
write_get_health_controller_file
↓
verify_get_health_controller_file
```

```text
add_health_route_import_to_app_js
↓
verify_app_imports_health_route
```

This keeps errors local and understandable.

---

## Work Tree Record

Each file or directory should have a record in the project tree.

Example:

```json
{
  "path": "src/routes/health.route.js",
  "kind": "route_file",
  "purpose": "GET /health route definition",
  "created_by": "task_4.6",
  "imports": ["src/controllers/health/getHealth.controller.js"],
  "imported_by": ["src/app.js"],
  "verified_by": ["task_4.7.1", "task_4.7.2", "task_4.7.3"]
}
```

The work tree should answer:

```text
What is this file?
Why does it exist?
Who created it?
Who imports it?
What verifies it?
Where should a future change happen?
```

---

## Future Refactor Layer

Very small files and deep imports may create long import paths.

This is acceptable in early Micro Mind because clarity is more important than compactness.

If import complexity becomes painful later, a future refactor layer can reorganize the generated project.

Possible future flow:

```text
Micro Mind writes highly decomposed project tree
↓
All tests pass
↓
Refactor/Packager layer reorganizes files if needed
↓
Tests run again
```

This should happen after correctness, not before.

---

## Current Decision

Micro Mind should build software by creating a project tree of tiny, traceable tasks.

The correct unit of work is not:

```text
Generate backend API
```

The correct unit of work is closer to:

```text
write one file
add one import
mount one route
verify one thing
```

This keeps Micro Mind learnable, debuggable and economical.
