# Project Documentation

## Project Architecture
This repository follows a clean and structured architecture based on the workspace root:
- `src/app/`: Contains the main application source code (FastAPI application).
- `tests/`: Contains the automated test suite for the application.
- `scripts/`: Contains utility scripts for starting the application (`start.sh`), testing (`test.sh`), deploying (`deploy.sh`), and environment setup.
- `Dockerfile` / `docker-compose.yml`: Configurations for containerized deployment and local service setup.
- `pyproject.toml` / `uv.lock`: Dependency management and project definitions managed directly by `uv`.
- `mcp.json`: Model Context Protocol configuration.

## Starting the Application
The application can be started using the provided bash script, which relies on `uv run fastapi` for isolated and reliable execution.

To start the application in development mode (runs on port 8080):
```bash
./scripts/start.sh --dev
```

To start the application in production mode (runs on port 8081):
```bash
./scripts/start.sh --prod
```

## Testing
To run code formatting checks and linting rules (via Ruff), you can use the included testing script:
```bash
./scripts/test.sh
```

**Testing Framework**: For executing the actual test suite, this repository utilizes **`uv pytest`**. To run all unit and integration tests defined in the `tests/` directory, ensure you execute:
```bash
uv pytest
```
