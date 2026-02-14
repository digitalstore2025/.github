import OpenAI from "openai";
import { canTransition, type ArticleState } from "@quds/shared";
import { db } from "../../db/client.js";
import { env } from "../../config/env.js";

const openai = new OpenAI({ apiKey: env.OPENAI_API_KEY });

export async function transitionArticleState(articleId: string, nextState: ArticleState): Promise<void> {
  const current = await db.query<{ state: ArticleState }>("SELECT state FROM articles WHERE id = $1", [articleId]);
  if (current.rowCount === 0) throw new Error("Article not found");
  const currentState = current.rows[0].state;
  if (!canTransition(currentState, nextState)) {
    throw new Error(`Invalid transition ${currentState} -> ${nextState}`);
  }
  await db.query("UPDATE articles SET state = $2, updated_at = now() WHERE id = $1", [articleId, nextState]);
}

export async function generateGroundedArticle(transcriptIds: string[], titleHint?: string): Promise<{ id: string }> {
  if (transcriptIds.length === 0) throw new Error("At least one transcript source is required");

  const transcriptQuery = await db.query<{ id: string; text: string }>(
    "SELECT id, text FROM transcripts WHERE id = ANY($1::uuid[])",
    [transcriptIds]
  );

  if (transcriptQuery.rowCount === 0) throw new Error("Generation aborted: no source transcripts found");

  const sourceBundle = transcriptQuery.rows.map((r) => `SOURCE_ID=${r.id}\n${r.text}`).join("\n\n");
  const prompt = `اكتب مقالًا إخباريًا عربيًا مهنيًا اعتمادًا فقط على النصوص التالية دون اختلاق معلومات.\n${sourceBundle}`;

  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    temperature: 0,
    messages: [
      { role: "system", content: "التزم حصريًا بالمصادر المعطاة واذكر المعرفات في النهاية." },
      { role: "user", content: `${titleHint ?? ""}\n${prompt}` }
    ]
  });

  const content = completion.choices[0]?.message?.content?.trim();
  if (!content) throw new Error("No generated content produced");

  const created = await db.query<{ id: string }>(
    `INSERT INTO articles (title, body, state, source_transcript_ids)
     VALUES ($1, $2, 'GENERATED', $3::uuid[])
     RETURNING id`,
    [titleHint ?? "خبر مستند", content, transcriptIds]
  );

  return created.rows[0];
}

export async function assertApproved(articleId: string): Promise<void> {
  const result = await db.query<{ state: ArticleState }>("SELECT state FROM articles WHERE id = $1", [articleId]);
  if (result.rowCount === 0) throw new Error("Article not found");
  if (result.rows[0].state !== "APPROVED") throw new Error("Only APPROVED articles can be published or synthesized");
}
