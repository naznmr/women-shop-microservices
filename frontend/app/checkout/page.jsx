"use client";

import { useEffect, useMemo, useState } from "react";
import { apiFetch } from "../lib/api";
import { cartTotal, clearCart, getCart } from "../lib/store";

export default function Checkout() {
  const [cart, setCart] = useState([]);
  const [cardLast4, setCardLast4] = useState("1234");
  const [msg, setMsg] = useState("");

  useEffect(() => setCart(getCart()), []);
  const total = useMemo(() => cartTotal(), [cart]);

  async function pay() {
    setMsg("");
    const token = localStorage.getItem("token");
    if (!token) {
      setMsg("برای پرداخت باید وارد حساب شوید.");
      return;
    }
    if (!/^\d{4}$/.test(cardLast4)) {
      setMsg("چهار رقم آخر کارت باید دقیقاً ۴ رقم باشد.");
      return;
    }

    try {
      const payload = {
        items: cart.map((x) => ({ product_id: x.product_id, qty: x.qty })),
        card_last4: cardLast4,
      };
      const order = await apiFetch("/api/orders", { method: "POST", body: JSON.stringify(payload) });
      clearCart();
      setMsg(`✅ سفارش ثبت شد. شماره: ${order.id} | وضعیت: ${order.status}`);
    } catch (e) {
      setMsg("❌ " + e.message);
    }
  }

  if (!cart.length) return <div>سبد شما خالی است.</div>;

  return (
    <div style={{ maxWidth: 680 }}>
      <h1 className="h1">پرداخت</h1>
      <div className="box">
        <div><b>جمع کل:</b> {total.toLocaleString("fa-IR")} تومان</div>

        <div style={{ marginTop: 12 }}>
          <label className="label">چهار رقم آخر کارت (شبیه‌سازی)</label>
          <input className="input" value={cardLast4} onChange={(e) => setCardLast4(e.target.value)} />
        </div>

        <button className="btn btn--primary" style={{ marginTop: 12 }} onClick={pay}>
          پرداخت و ثبت سفارش
        </button>

        {msg ? <p style={{ marginTop: 12 }}>{msg}</p> : null}
        <p style={{ marginTop: 10 }}><a className="btn" href="/auth">رفتن به ورود/ثبت‌نام</a></p>
      </div>
    </div>
  );
}