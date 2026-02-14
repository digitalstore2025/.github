import { FastifyInstance } from "fastify";
import { assertApproved } from "../articles/service.js";
import { publishQueue } from "../../queue/index.js";

export async function publishRoutes(app: FastifyInstance): Promise<void> {
  app.post<{ Params: { id: string } }>("/articles/:id/publish", async (request, reply) => {
    await assertApproved(request.params.id);
    const job = await publishQueue.add("publish-article", { articleId: request.params.id });
    return reply.code(202).send({ jobId: job.id });
  });
}
