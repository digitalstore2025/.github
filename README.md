# Quds Radio AI

Production-grade AI-powered digital radio platform for Arabic RTL news, transcript-grounded article generation, and automated audio broadcasting.

## Architecture

- **Frontend:** Next.js App Router, dark RTL UI, persistent audio player.
- **Backend API:** Node.js + TypeScript + Fastify + PostgreSQL.
- **Queue:** BullMQ + Redis for fault-tolerant, retryable jobs.
- **Ingestion Service:** adapters for Facebook, YouTube, Telegram, X.
- **Audio Service:** converts APPROVED articles into Palestinian Arabic broadcast audio.
- **Storage:** S3-compatible object storage for media and generated audio.
- **Database:** PostgreSQL with strict article lifecycle state machine.

## Monorepo layout

- `apps/web` - user-facing Arabic website.
- `apps/api` - backend API, queue workers, state machine enforcement.
- `services/ingestion` - social ingestion producer.
- `services/audio` - TTS producer/consumer utility.
- `packages/shared` - shared DTOs, enums, validation.
- `infra` - SQL, Docker compose, Cloudflare + Terraform templates.

## Article lifecycle

`INGESTED -> TRANSCRIBED -> GENERATED -> VERIFIED -> APPROVED -> PUBLISHED`

- Generation fails if no transcript sources are available.
- Publishing and audio generation are blocked unless state is `APPROVED`.
- Every generated article stores and returns source transcript IDs.

## Quick start

1. Copy `.env.example` into each service as `.env`.
2. Start local infra:
   - `docker compose -f infra/docker/docker-compose.yml up -d`
3. Run migrations:
   - `psql "$DATABASE_URL" -f infra/sql/001_init.sql`
4. Install and run:
   - `npm install`
   - `npm run build`

## Deployment

- **Frontend:** Cloudflare Pages (`infra/cloudflare/pages.json`).
- **Backend + workers:** container runtime (Fly/Render/Railway-ready Dockerfiles).
- **PostgreSQL:** managed service (Neon/Supabase/RDS).
- **Object storage:** Cloudflare R2/S3-compatible bucket.

See `infra/terraform` for baseline cloud resource configuration.
