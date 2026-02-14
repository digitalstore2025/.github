import { getLatestArticles } from "../../../lib/api";

export default async function ArticlePage({ params }: { params: { id: string } }): Promise<JSX.Element> {
  const article = (await getLatestArticles()).find((a) => a.id === params.id);
  if (!article) return <div>المقال غير موجود</div>;

  return (
    <article className="card">
      <h1>{article.title}</h1>
      <p>{article.body}</p>
      <small>حالة التحرير: {article.state}</small>
      <div>معرّفات المصادر: {article.sourceTranscriptIds.join(" | ")}</div>
    </article>
  );
}
