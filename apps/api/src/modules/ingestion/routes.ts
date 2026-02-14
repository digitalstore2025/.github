import { FastifyInstance } from "fastify";
import { ingestionQueue } from "../../queue/index.js";

export async function ingestionRoutes(app: FastifyInstance): Promise<void> {
  app.post<{ Body: { platform: "FACEBOOK" | "YOUTUBE" | "TELEGRAM" | "X"; sourceUrl: string } }>("/ingestion/jobs", async (request, reply) => {
    const job = await ingestionQueue.add("fetch-source", request.body);
    return reply.code(202).send({ jobId: job.id });
  });
}
