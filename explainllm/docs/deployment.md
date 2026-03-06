# Deployment

## Local docker-compose

```bash
cd explainllm/infrastructure
docker-compose up --build
```

## Validation checklist

- API health: `curl http://localhost:8000/health`
- Analyze endpoint: `curl -X POST http://localhost:8000/analyze -H 'Content-Type: application/json' -d '{"prompt":"..."}'`
- Frontend loaded at `http://localhost:3000`
- Celery worker logs show connected to Redis

## Production hardening suggestions

- Add PostgreSQL persistence for library/metrics.
- Add authentication and tenant isolation.
- Add rate-limiting and API keys.
- Replace prompt simulator with real model provider adapters.
