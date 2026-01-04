const USER_INTERNAL = process.env.USER_BASE_INTERNAL || "http://user-service:8000";

export async function POST(req) {
  const body = await req.json();
  const r = await fetch(`${USER_INTERNAL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });

  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: { "Content-Type": r.headers.get("content-type") || "application/json" },
  });
}