#!/bin/bash

set -ex
uv sync
uv run patchright install firefox