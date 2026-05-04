#!/bin/bash

set -ex
uv sync
uv run playwright install firefox