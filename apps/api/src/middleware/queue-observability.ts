import { QueueEvents } from "bullmq";
import { redis } from "../queue/index.js";

export function registerQueueObservers(logger: { info: Function; error: Function }): void {
  ["ingestion", "transcription", "generation", "audio", "publish"].forEach((queueName) => {
    const events = new QueueEvents(queueName, { connection: redis });
    events.on("failed", ({ jobId, failedReason }) => logger.error({ queueName, jobId, failedReason }, "Queue job failed"));
    events.on("completed", ({ jobId }) => logger.info({ queueName, jobId }, "Queue job completed"));
  });
}
