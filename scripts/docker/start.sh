#!/bin/bash
set -ex
uv run --no-dev fastapi run --port 8080 app/main.py