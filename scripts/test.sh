#!/bin/bash

set -ex

uv run ruff format --check
uv run ruff check
uv run pytest