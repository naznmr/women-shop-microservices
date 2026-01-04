const PRODUCT_BASE =
  process.env.PRODUCT_BASE_INTERNAL ||
  (typeof window === "undefined" ? "http://product-service:8000" : "http://localhost:8002");

import ProductClient from "./product-client";

async function getProduct(id) {
  const res = await fetch(`${PRODUCT_BASE}/products/${encodeURIComponent(id)}`, { cache: "no-store" });
  if (!res.ok) return null;
  return res.json();
}

export default async function ProductPage({ params }) {
  const p = await getProduct(params.id);
  if (!p) return <div>محصول پیدا نشد.</div>;
  return <ProductClient product={p} />;
}