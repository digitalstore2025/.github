import { FastifyInstance } from "fastify";
import { GenerateArticleRequestSchema } from "@quds/shared";
import { generateGroundedArticle, transitionArticleState } from "./service.js";

export async function articleRoutes(app: FastifyInstance): Promise<void> {
  app.post("/articles/generate", async (request, reply) => {
    const payload = GenerateArticleRequestSchema.parse(request.body);
    const article = await generateGroundedArticle(payload.transcriptIds, payload.titleHint);
    return reply.code(201).send(article);
  });

  app.patch<{ Params: { id: string }; Body: { nextState: string } }>("/articles/:id/state", async (request) => {
    await transitionArticleState(request.params.id, request.body.nextState as any);
    return { ok: true };
  });
}
