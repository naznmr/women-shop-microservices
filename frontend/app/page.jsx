const PRODUCT_BASE =
  process.env.PRODUCT_BASE_INTERNAL ||
  (typeof window === "undefined" ? "http://product-service:8000" : "http://localhost:8002");

async function getProducts() {
  const res = await fetch(`${PRODUCT_BASE}/products?limit=24`, { cache: "no-store" });
  if (!res.ok) return [];

  const data = await res.json();

  // اگر API آرایه برگرداند
  if (Array.isArray(data)) return data;

  // اگر API مثل { value: [...] } برگرداند
  if (data && Array.isArray(data.value)) return data.value;

  return [];
}

export default async function Page() {
  const products = await getProducts();

  return (
    <>
      <section className="hero">
        <h1 className="hero__title">Rimberio ✨ استایل دخترونه، پاستیلی و خاص</h1>
        <p className="hero__sub">
          کالکشن لباس زنانه برای هر چهار فصل؛ انتخاب‌های لطیف، شیک و چشم‌نواز برای استایل روزمره تا مجلسی.
        </p>

        <div className="hero__chips">
          <span className="chip">🌸 بهار</span>
          <span className="chip">☀️ تابستان</span>
          <span className="chip">🍂 پاییز</span>
          <span className="chip">❄️ زمستان</span>
        </div>
      </section>

      <div className="section__head">
        <h2 className="h1">جدیدترین محصولات</h2>
        <p className="sub">منتخب‌های امروز با حس لطیف و شیک</p>
      </div>

      {products?.length ? (
        <div className="grid">
          {products.map((p) => {
            const pid = p.id || p._id;
            return (
              <a key={pid} href={`/p/${pid}`} className="card">
                <div className="card__inner">
                  {p.image_url ? (
                    <img className="card__img" src={p.image_url} alt={p.title} loading="lazy" />
                  ) : (
                    <div className="card__img card__img--placeholder">بدون عکس</div>
                  )}

                  <div className="card__title">{p.title}</div>
                  <div className="card__meta">{p.category} • {p.season}</div>

                  <div className="badges">
                    <span className="badge badge--rose">پاستیلی</span>
                    <span className="badge">محبوب</span>
                  </div>

                  <div className="price">{Number(p.price_toman || 0).toLocaleString("fa-IR")} تومان</div>
                  <div className="stock">📦 موجودی: {p.stock}</div>

                  <span className="btn">مشاهده جزئیات →</span>
                </div>
              </a>
            );
          })}

        </div>
      ) : (
        <div className="empty">هنوز محصولی ثبت نشده است.</div>
      )}
    </>
  );
}