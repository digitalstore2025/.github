CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'article_state') THEN
    CREATE TYPE article_state AS ENUM ('INGESTED', 'TRANSCRIBED', 'GENERATED', 'VERIFIED', 'APPROVED', 'PUBLISHED');
  END IF;
END $$;

CREATE TABLE IF NOT EXISTS ingestion_sources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  platform TEXT NOT NULL CHECK (platform IN ('FACEBOOK', 'YOUTUBE', 'TELEGRAM', 'X')),
  source_url TEXT NOT NULL,
  external_id TEXT NOT NULL,
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transcripts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES ingestion_sources(id) ON DELETE CASCADE,
  language TEXT NOT NULL DEFAULT 'ar',
  text TEXT NOT NULL,
  audio_object_key TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  state article_state NOT NULL DEFAULT 'INGESTED',
  source_transcript_ids UUID[] NOT NULL DEFAULT '{}',
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT generated_has_sources CHECK (
    state != 'GENERATED' OR cardinality(source_transcript_ids) > 0
  )
);

CREATE TABLE IF NOT EXISTS audio_assets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_id UUID NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
  object_key TEXT NOT NULL,
  voice TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('QUEUED', 'READY', 'FAILED')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_articles_state ON articles(state);
CREATE INDEX IF NOT EXISTS idx_transcripts_source_id ON transcripts(source_id);
