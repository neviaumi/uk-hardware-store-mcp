#!/bin/bash

export BROWSERLESS_API_KEY=$(gcloud secrets versions access latest --secret="browserless-token")

docker compose up -d --build