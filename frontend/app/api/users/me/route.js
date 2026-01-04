const USER_INTERNAL = process.env.USER_BASE_INTERNAL || "http://user-service:8000";

export async function GET(req) {
  const auth = req.headers.get("authorization") || "";
  const r = await fetch(`${USER_INTERNAL}/users/me`, {
    headers: auth ? { Authorization: auth } : {},
    cache: "no-store",
  });

  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: { "Content-Type": r.headers.get("content-type") || "application/json" },
  });
}