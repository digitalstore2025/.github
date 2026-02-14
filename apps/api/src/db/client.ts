import { Pool } from "pg";
import { env } from "../config/env.js";

export const db = new Pool({
  connectionString: env.DATABASE_URL,
  max: 20,
  ssl: env.NODE_ENV === "production" ? { rejectUnauthorized: false } : false
});
