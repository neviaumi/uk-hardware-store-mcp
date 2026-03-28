# Project Documentation

## Spec Driven Development (SDD) Workflow
This project STRICTLY adheres to the Spec Driven Development workflow. The Agent **MUST** follow these steps before modifying any runtime logic or configuration:
1. **Discovery & Investigation**: Understand the goal, read relevant files, and check current system statuses.
2. **Drafting the Plan**: Produce a clear `implementation_plan.md` and `task.md` detailing all architectural adjustments.
3. **Safety Hook (Approval)**: Use the `notify_user` tool with `BlockedOnUser: true` to pause and receive explicit user authorization. **No file modifications are allowed before this step.**
4. **Execution**: Apply the approved changes strictly.
5. **Testing & Verification**: Validate code utilizing `scripts/test.sh` (lint/format) and `uv run pytest` (behavioral).
6. **Documentation Walkthrough**: Produce a final `walkthrough.md` capturing what was executed and proven through testing.

## Agent Behavioral Primitives
- **Mandatory Plan Approval**: The agent cannot execute destructive or constructive changes on the primary codebase without an approved implementation plan.
- **Architectural Boundary Adherence**: Follow the exact folder conventions established for `app/`, `tests/`, and `scripts/`. Do not produce files in arbitrary locations.
- **Verification-First**: Always verify application behavior immediately after execution via `pytest` and Ruff linting checks.

## Debugging Protocol
This project utilizes a dedicated `.debug/` folder at the root for temporary file debugging and execution state analysis.
- **Autonomous Analysis**: The agent is authorized to create, read, and delete files within `.debug/` to capture stack traces, variable states, or raw tool outputs.
- **Overhead Reduction**: The agent should utilize this folder to resolve execution ambiguities independently before querying the user.
- **Persistence**: Files in `.debug/` are temporary and excluded from version control.

## Project Architecture
This repository uses the following directory structure:
- `app/`: Contains the main application source code, FastAPI entry points, MCP server definitions, and web crawlers.
- `tests/`: Contains the automated test suite for the application.
- `scripts/`: Contains utility scripts for starting the application (`start.sh`), testing (`test.sh`), deploying (`deploy.sh`), and environment setup.
- `Dockerfile` / `docker-compose.yml`: Configurations for containerized deployment and local service setup.
- `pyproject.toml` / `uv.lock`: Dependency management and project definitions managed directly by `uv`.
- `mcp.json`: Model Context Protocol configuration.

## Starting the Application
The application can be started using the provided bash scripts, which run the FastAPI server via `uv`.

To start the application in development mode (runs on port 8080):
```bash
bash ./scripts/start.sh --dev
```

To start the application in production mode (runs on port 8081):
```bash
bash ./scripts/start.sh --prod
```

## Testing
To run code formatting checks and linting rules (via Ruff):
```bash
bash ./scripts/test.sh
```

**Testing Framework**: For executing the actual test suite, this repository utilizes **`uv run pytest`**. To run all unit and integration tests defined in the `tests/` directory, ensure you execute:
```bash
uv run pytest
```

### Mocking and Test Generation
All new test generation for HTTP-based interactions **MUST** utilize `pytest-httpserver` for mock setups.
- **Reference Patterns**: Consult `@tests/mock_server` for established mock server configurations and HTML fixture usage.
- **Exceptions**: Direct MCP server integration tests (e.g., `tests/test_mcp_product_search.py`) are exempted from this requirement as they interact with the server via `stdio` rather than HTTP.
