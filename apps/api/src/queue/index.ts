import { Queue } from "bullmq";
import IORedis from "ioredis";
import { env } from "../config/env.js";

export const redis = new IORedis(env.REDIS_URL, {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

const defaultJobOptions = {
  removeOnComplete: 200,
  removeOnFail: 500,
  attempts: 5,
  backoff: {
    type: "exponential" as const,
    delay: 2_000
  }
};

export const ingestionQueue = new Queue("ingestion", { connection: redis, defaultJobOptions });
export const transcriptionQueue = new Queue("transcription", { connection: redis, defaultJobOptions });
export const generationQueue = new Queue("generation", { connection: redis, defaultJobOptions });
export const audioQueue = new Queue("audio", { connection: redis, defaultJobOptions });
export const publishQueue = new Queue("publish", { connection: redis, defaultJobOptions });
