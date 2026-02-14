import Link from "next/link";
import { getLatestArticles } from "../lib/api";

export default async function HomePage(): Promise<JSX.Element> {
  const articles = await getLatestArticles();

  return (
    <section>
      <h1>Quds Radio AI</h1>
      <p>أخبار فورية موثقة بالمصادر الصوتية والنصية.</p>
      {articles.map((article) => (
        <article className="card" key={article.id}>
          <h2>{article.title}</h2>
          <p>{article.body}</p>
          <p>المصادر: {article.sourceTranscriptIds.join(", ")}</p>
          <Link href={`/article/${article.id}`}>قراءة التفاصيل</Link>
        </article>
      ))}
    </section>
  );
}
