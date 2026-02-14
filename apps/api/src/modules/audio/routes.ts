import { FastifyInstance } from "fastify";
import { assertApproved } from "../articles/service.js";
import { audioQueue } from "../../queue/index.js";

export async function audioRoutes(app: FastifyInstance): Promise<void> {
  app.post<{ Params: { id: string } }>("/articles/:id/audio", async (request, reply) => {
    await assertApproved(request.params.id);
    const job = await audioQueue.add("synthesize-article", { articleId: request.params.id });
    return reply.code(202).send({ jobId: job.id });
  });
}
