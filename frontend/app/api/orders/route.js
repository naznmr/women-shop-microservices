const ORDER_INTERNAL = process.env.ORDER_BASE_INTERNAL || "http://order-service:8000";

export async function POST(req) {
  const auth = req.headers.get("authorization") || "";
  const body = await req.json();

  const r = await fetch(`${ORDER_INTERNAL}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(auth ? { Authorization: auth } : {}),
    },
    body: JSON.stringify(body),
    cache: "no-store",
  });

  const text = await r.text();
  return new Response(text, {
    status: r.status,
    headers: { "Content-Type": r.headers.get("content-type") || "application/json" },
  });
}