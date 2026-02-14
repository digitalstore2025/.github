import { z } from "zod";

export const ArticleState = {
  INGESTED: "INGESTED",
  TRANSCRIBED: "TRANSCRIBED",
  GENERATED: "GENERATED",
  VERIFIED: "VERIFIED",
  APPROVED: "APPROVED",
  PUBLISHED: "PUBLISHED"
} as const;

export type ArticleState = (typeof ArticleState)[keyof typeof ArticleState];

export const TranscriptSchema = z.object({
  id: z.string().uuid(),
  sourcePlatform: z.enum(["FACEBOOK", "YOUTUBE", "TELEGRAM", "X"]),
  sourceId: z.string().min(1),
  audioObjectKey: z.string().min(1),
  language: z.literal("ar"),
  text: z.string().min(1)
});

export const GenerateArticleRequestSchema = z.object({
  transcriptIds: z.array(z.string().uuid()).min(1),
  titleHint: z.string().min(3).optional()
});

export const TransitionMap: Record<ArticleState, ArticleState[]> = {
  INGESTED: ["TRANSCRIBED"],
  TRANSCRIBED: ["GENERATED"],
  GENERATED: ["VERIFIED"],
  VERIFIED: ["APPROVED"],
  APPROVED: ["PUBLISHED"],
  PUBLISHED: []
};

export const canTransition = (from: ArticleState, to: ArticleState): boolean =>
  TransitionMap[from].includes(to);
