"use client";

const CART_KEY = "rimberio_cart_v1";
const WISH_KEY = "rimberio_wishlist_v1";

function read(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function write(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
  // رو همین تب هم آپدیت UI بده
  window.dispatchEvent(new CustomEvent("shop:changed", { detail: { key } }));
}

export function getCart() {
  return read(CART_KEY, []);
}

export function setCart(next) {
  write(CART_KEY, next);
}

export function addToCart(product, { color = "", size = "", qty = 1 } = {}) {
  const cart = getCart();

  // هر ترکیب (محصول/رنگ/سایز) یک ردیف جدا
  const lineId = `${product.id}::${color}::${size}`;
  const found = cart.find((x) => x.line_id === lineId);

  if (found) found.qty += qty;
  else {
    cart.push({
      line_id: lineId,
      product_id: product.id,
      title: product.title,
      price_toman: Number(product.price_toman || 0),
      image_url: product.image_url || null,
      color,
      size,
      qty,
    });
  }

  setCart(cart);
}

export function updateCartQty(line_id, qty) {
  const cart = getCart().map((x) => (x.line_id === line_id ? { ...x, qty: Math.max(1, qty) } : x));
  setCart(cart);
}

export function removeFromCart(line_id) {
  const cart = getCart().filter((x) => x.line_id !== line_id);
  setCart(cart);
}

export function clearCart() {
  setCart([]);
}

export function cartCount() {
  return getCart().reduce((s, x) => s + Number(x.qty || 0), 0);
}

export function cartTotal() {
  return getCart().reduce((s, x) => s + Number(x.price_toman || 0) * Number(x.qty || 0), 0);
}

// Wishlist
export function getWishlist() {
  return read(WISH_KEY, []);
}

export function isWishlisted(productId) {
  return getWishlist().includes(productId);
}

export function toggleWishlist(productId) {
  const w = getWishlist();
  const next = w.includes(productId) ? w.filter((id) => id !== productId) : [productId, ...w];
  write(WISH_KEY, next);
  return next;
}