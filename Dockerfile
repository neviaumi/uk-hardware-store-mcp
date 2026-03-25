FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./mcp.json ./.python-version ./
COPY ./app ./app/
COPY ./scripts/docker/ ./scripts/docker

RUN sh ./scripts/docker/setup.sh