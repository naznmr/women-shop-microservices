"use client";

import { useMemo, useState } from "react";
import { addToCart, isWishlisted, toggleWishlist } from "../../lib/store";

export default function ProductClient({ product }) {
  const colors = product.colors || [];
  const sizes = product.sizes || [];

  const [color, setColor] = useState(colors[0] || "");
  const [size, setSize] = useState(sizes[0] || "");
  const [qty, setQty] = useState(1);
  const [liked, setLiked] = useState(isWishlisted(product.id));

  const price = useMemo(() => Number(product.price_toman || 0), [product.price_toman]);

  function onAdd() {
    addToCart(product, { color, size, qty });
    alert("به سبد خرید اضافه شد ✅");
  }

  function onToggleWish() {
    toggleWishlist(product.id);
    setLiked(isWishlisted(product.id));
  }

  return (
    <div className="detail">
      <div className="detail__grid">
        <div className="detail__media">
          {product.image_url ? (
            <img className="detail__img" src={product.image_url} alt={product.title} />
          ) : (
            <div className="detail__img detail__img--placeholder">بدون تصویر</div>
          )}
        </div>

        <div className="detail__info">
          <h1 className="detail__title">{product.title}</h1>
          <div className="detail__meta">
            <span className="badge">{product.category}</span>
            <span className="badge badge--rose">{product.season}</span>
            <span className="badge">موجودی: {product.stock}</span>
          </div>

          {product.description ? <p className="detail__desc">{product.description}</p> : null}

          <div className="detail__price">{price.toLocaleString("fa-IR")} تومان</div>

          <div className="detail__row">
            <div className="detail__label">رنگ</div>
            {colors.length ? (
              <select className="input" value={color} onChange={(e) => setColor(e.target.value)}>
                {colors.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            ) : (
              <div className="muted">ندارد</div>
            )}
          </div>

          <div className="detail__row">
            <div className="detail__label">سایز</div>
            {sizes.length ? (
              <select className="input" value={size} onChange={(e) => setSize(e.target.value)}>
                {sizes.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            ) : (
              <div className="muted">فری‌سایز / ندارد</div>
            )}
          </div>

          <div className="detail__row">
            <div className="detail__label">تعداد</div>
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <button className="btn" type="button" onClick={() => setQty((q) => Math.max(1, q - 1))}>-</button>
              <b>{qty}</b>
              <button className="btn" type="button" onClick={() => setQty((q) => q + 1)}>+</button>
            </div>
          </div>

          <div className="detail__actions">
            <button className="btn btn--primary" type="button" onClick={onAdd}>
              افزودن به سبد خرید
            </button>

            <button className="btn" type="button" onClick={onToggleWish}>
              {liked ? "♥ در علاقه‌مندی‌ها" : "♡ افزودن به علاقه‌مندی"}
            </button>

            <a className="btn" href="/cart">رفتن به سبد خرید</a>
          </div>
        </div>
      </div>
    </div>
  );
}