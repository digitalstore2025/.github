# ExplainLLM

ExplainLLM is a local AI developer platform for prompt engineering workflows:

- Prompt analysis
- Prompt fixing
- Prompt variant generation
- Prompt benchmarking
- Prompt scanning
- Prompt optimization pipeline
- Prompt observability metrics

## Quick start

```bash
cd explainllm/infrastructure
docker-compose up --build
```

Services:

- API: http://localhost:8000
- Frontend: http://localhost:3000
- Redis: localhost:6379
- Postgres: localhost:5432

## CLI

```bash
python -m cli.main analyze "Write an API design"
python -m cli.main optimize "Build prompt monitoring"
```
