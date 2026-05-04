#!/bin/bash
set -ex
MODE=${1:---dev}
export BROWSERLESS_API_KEY=$(gcloud secrets versions access latest --secret="browserless-token")

if [ "$MODE" == "--dev" ]; then
  uv run fastapi dev --port 8080 app/main.py
elif [ "$MODE" == "--prod" ]; then
  uv run fastapi run --port 8082 app/main.py
else
    echo "Invalid argument: $MODE"
    exit 1
fi

