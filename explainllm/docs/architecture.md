# Architecture

## Components

- **FastAPI backend** (`backend/`): API endpoints and orchestration.
- **Prompt engine** (`engine/`): parser, linter, optimizer, simulator logic.
- **Celery workers** (`workers/`): async benchmark and optimization jobs.
- **CLI** (`cli/`): command-line wrapper around HTTP API.
- **Frontend (Next.js)** (`frontend/`): prompt editor and action controls.
- **Infrastructure** (`infrastructure/`): Docker build/runtime definitions.

## Data flow

1. User submits prompt via UI, CLI, or direct API.
2. Backend routes request to module (`analyzer`, `fixer`, etc.).
3. Benchmark and optimization can run synchronously or asynchronously via Celery.
4. Metrics are recorded in observability store and exposed via `/metrics`.
