export type Article = {
  id: string;
  title: string;
  body: string;
  state: "PUBLISHED" | "APPROVED" | "VERIFIED";
  sourceTranscriptIds: string[];
};

export async function getLatestArticles(): Promise<Article[]> {
  return [
    {
      id: "demo-1",
      title: "تحديثات ميدانية من القدس",
      body: "هذا نموذج لعرض المقالات المنشورة من واجهة الأخبار.",
      state: "PUBLISHED",
      sourceTranscriptIds: ["a1", "b2"]
    }
  ];
}
