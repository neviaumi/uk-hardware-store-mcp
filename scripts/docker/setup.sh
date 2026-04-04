#!/bin/bash
set -ex
apt-get update && apt-get install -y gcc python3-dev

uv sync --no-dev --locked
