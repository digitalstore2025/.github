export async function GET(): Promise<Response> {
  return new Response("Radio stream proxy placeholder", {
    status: 200,
    headers: { "Content-Type": "text/plain; charset=utf-8" }
  });
}
