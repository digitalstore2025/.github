import { config } from "dotenv";
import { Worker } from "bullmq";
import IORedis from "ioredis";
import { Pool } from "pg";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import pino from "pino";

config();
const log = pino({ name: "audio-service" });
const redis = new IORedis(process.env.REDIS_URL ?? "redis://localhost:6379", { maxRetriesPerRequest: null, enableReadyCheck: false });
const db = new Pool({ connectionString: process.env.DATABASE_URL });

const s3 = new S3Client({
  endpoint: process.env.S3_ENDPOINT,
  region: "auto",
  credentials: {
    accessKeyId: process.env.S3_ACCESS_KEY_ID ?? "",
    secretAccessKey: process.env.S3_SECRET_ACCESS_KEY ?? ""
  }
});

new Worker(
  "audio",
  async (job) => {
    const articleId = job.data.articleId as string;
    const res = await db.query<{ body: string }>("SELECT body FROM articles WHERE id = $1 AND state = 'APPROVED'", [articleId]);
    if (res.rowCount === 0) throw new Error("Audio generation blocked: article not APPROVED");

    const objectKey = `audio/${articleId}.mp3`;
    const syntheticAudio = Buffer.from(`PAL-AR TTS PLACEHOLDER\n${res.rows[0].body}`, "utf-8");

    await s3.send(new PutObjectCommand({
      Bucket: process.env.S3_BUCKET,
      Key: objectKey,
      Body: syntheticAudio,
      ContentType: "audio/mpeg"
    }));

    await db.query(
      "UPDATE audio_assets SET status = 'READY', object_key = $2, updated_at = now() WHERE article_id = $1",
      [articleId, objectKey]
    );

    log.info({ articleId, objectKey }, "Generated and uploaded broadcast audio");
  },
  { connection: redis, concurrency: 3 }
);
