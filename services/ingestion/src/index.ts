import { config } from "dotenv";
import { Worker, Queue } from "bullmq";
import IORedis from "ioredis";
import pino from "pino";

config();
const log = pino({ name: "ingestion-service" });
const redis = new IORedis(process.env.REDIS_URL ?? "redis://localhost:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

const transcriptionQueue = new Queue("transcription", { connection: redis });

new Worker(
  "ingestion",
  async (job) => {
    log.info({ jobId: job.id, data: job.data }, "Fetched source metadata from social platform");
    await transcriptionQueue.add("extract-and-transcribe", {
      ...job.data,
      fetchedAt: new Date().toISOString()
    });
  },
  { connection: redis, concurrency: 5 }
);
