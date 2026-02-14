import Fastify from "fastify";
import pino from "pino";
import { env } from "./config/env.js";
import { articleRoutes } from "./modules/articles/routes.js";
import { ingestionRoutes } from "./modules/ingestion/routes.js";
import { audioRoutes } from "./modules/audio/routes.js";
import { publishRoutes } from "./modules/publish/routes.js";
import { registerQueueObservers } from "./middleware/queue-observability.js";

const app = Fastify({ logger: pino({ level: "info" }) });
registerQueueObservers(app.log);

app.get("/health", async () => ({ status: "ok" }));
app.register(articleRoutes, { prefix: "/v1" });
app.register(ingestionRoutes, { prefix: "/v1" });
app.register(audioRoutes, { prefix: "/v1" });
app.register(publishRoutes, { prefix: "/v1" });

app.listen({ port: env.PORT, host: "0.0.0.0" }).catch((error) => {
  app.log.error(error);
  process.exit(1);
});
