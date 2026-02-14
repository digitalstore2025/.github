#!/usr/bin/env bash
set -euo pipefail

cp -n apps/api/.env.example apps/api/.env || true
cp -n services/audio/.env.example services/audio/.env || true
cp -n services/ingestion/.env.example services/ingestion/.env || true

echo "Run docker compose -f infra/docker/docker-compose.yml up -d"
echo "Then run psql \"$DATABASE_URL\" -f infra/sql/001_init.sql"
