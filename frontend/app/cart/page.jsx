"use client";

import { useEffect, useMemo, useState } from "react";
import { cartTotal, getCart, removeFromCart, updateCartQty } from "../lib/store";

export default function CartPage() {
  const [cart, setCart] = useState([]);

  function refresh() {
    setCart(getCart());
  }

  useEffect(() => {
    refresh();
    const onChanged = () => refresh();
    window.addEventListener("shop:changed", onChanged);
    return () => window.removeEventListener("shop:changed", onChanged);
  }, []);

  const total = useMemo(() => cartTotal(), [cart]);

  if (!cart.length) return <div>سبد شما خالی است.</div>;

  return (
    <div>
      <h1 className="h1">سبد خرید</h1>

      <div className="cartList">
        {cart.map((x) => (
          <div key={x.line_id} className="cartItem">
            <div className="cartLeft">
              {x.image_url ? <img className="cartImg" src={x.image_url} alt={x.title} /> : <div className="cartImg cartImg--ph" />}
              <div>
                <div className="cartTitle">{x.title}</div>
                <div className="muted">{(x.price_toman || 0).toLocaleString("fa-IR")} تومان</div>
                <div className="muted">
                  {x.color ? `رنگ: ${x.color}` : ""} {x.size ? ` • سایز: ${x.size}` : ""}
                </div>
              </div>
            </div>

            <div className="cartRight">
              <div className="qty">
                <button className="btn" onClick={() => updateCartQty(x.line_id, x.qty - 1)}>-</button>
                <b>{x.qty}</b>
                <button className="btn" onClick={() => updateCartQty(x.line_id, x.qty + 1)}>+</button>
              </div>
              <button className="btn" onClick={() => removeFromCart(x.line_id)}>حذف</button>
            </div>
          </div>
        ))}
      </div>

      <div className="cartTotal">
        <div><b>جمع کل:</b> {total.toLocaleString("fa-IR")} تومان</div>
        <a className="btn btn--primary" href="/checkout">ادامه و پرداخت</a>
      </div>
    </div>
  );
}