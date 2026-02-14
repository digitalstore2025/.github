import { Worker } from "bullmq";
import { redis } from "../queue/index.js";
import { db } from "../db/client.js";

const workerOpts = { connection: redis, concurrency: 4 };

new Worker(
  "publish",
  async (job) => {
    const { articleId } = job.data as { articleId: string };
    await db.query("UPDATE articles SET state = 'PUBLISHED', published_at = now() WHERE id = $1 AND state = 'APPROVED'", [articleId]);
  },
  workerOpts
);

new Worker(
  "audio",
  async (job) => {
    const { articleId } = job.data as { articleId: string };
    await db.query(
      `INSERT INTO audio_assets (article_id, object_key, voice, status)
       VALUES ($1, $2, 'palestinian-female', 'QUEUED')`,
      [articleId, `audio/${articleId}.mp3`]
    );
  },
  workerOpts
);
