import asyncio
import random
from app.db import products_collection

N = 200  # تعداد محصولات

CATEGORIES = [
    ("مانتو", ["بهار", "تابستان", "پاییز"]),
    ("شومیز", ["بهار", "تابستان"]),
    ("پیراهن", ["بهار", "تابستان", "پاییز"]),
    ("دامن", ["بهار", "تابستان"]),
    ("شلوار", ["بهار", "تابستان", "پاییز"]),
    ("کت", ["پاییز", "زمستان"]),
    ("بافت", ["پاییز", "زمستان"]),
    ("پالتو", ["زمستان"]),
    ("ست", ["بهار", "تابستان"]),
    ("شال", ["بهار", "پاییز", "زمستان"]),
]

STYLES = ["مینیمال", "پاستیلی", "کلاسیک", "لاکچری", "روزمره", "مجلسی", "کژوال", "ترندی"]
FABRICS = ["لینن", "نخی", "کرپ", "ساتن", "پنبه‌ای", "کتان", "ژاکارد", "پشمی", "ویسکوز"]
COLOR_POOL = ["صورتی", "کرم", "سفید", "یاسی", "هلویی", "آبی آسمانی", "سبز پاستیلی", "طوسی روشن"]

NAME_CODES = ["رُزا", "مهتاب", "نسترن", "باران", "آوینا", "سها", "آرتمیس", "ریحانه", "بهاره", "پریناز"]

SIZES_BY_CAT = {
    "مانتو": ["S", "M", "L", "XL"],
    "شومیز": ["S", "M", "L"],
    "پیراهن": ["S", "M", "L"],
    "دامن": ["36", "38", "40", "42"],
    "شلوار": ["36", "38", "40", "42"],
    "کت": ["M", "L", "XL"],
    "بافت": ["S", "M", "L", "XL"],
    "پالتو": ["M", "L", "XL"],
    "ست": ["S", "M", "L"],
    "شال": ["فری سایز"],
}

# عکس‌ها را بعداً داخل frontend/public/products می‌گذاری
IMAGES_BY_CAT = {
    "مانتو": ["/products/manto-1.jpg", "/products/manto-2.jpg", "/products/manto-3.jpg"],
    "شومیز": ["/products/shomiz-1.jpg", "/products/shomiz-2.jpg"],
    "پیراهن": ["/products/pirahan-1.jpg", "/products/pirahan-2.jpg"],
    "دامن": ["/products/daman-1.jpg", "/products/daman-2.jpg"],
    "شلوار": ["/products/shalvar-1.jpg", "/products/shalvar-2.jpg"],
    "کت": ["/products/kat-1.jpg", "/products/kat-2.jpg"],
    "بافت": ["/products/baft-1.jpg", "/products/baft-2.jpg"],
    "پالتو": ["/products/palto-1.jpg", "/products/palto-2.jpg"],
    "ست": ["/products/set-1.jpg", "/products/set-2.jpg"],
    "شال": ["/products/shal-1.jpg", "/products/shal-2.jpg"],
}

def gen_price(season: str) -> int:
    if season in ("زمستان",):
        lo, hi = 1200000, 3990000
    elif season in ("پاییز",):
        lo, hi = 900000, 2990000
    else:
        lo, hi = 450000, 2490000
    return random.randrange(lo, hi + 1, 10000)

def gen_product(i: int) -> dict:
    cat, seasons = random.choice(CATEGORIES)
    season = random.choice(seasons)
    style = random.choice(STYLES)
    fabric = random.choice(FABRICS)
    code = f"{random.choice(NAME_CODES)} {1000 + i}"
    title = f"{cat} {style} {fabric} مدل {code}"

    colors = random.sample(COLOR_POOL, k=random.randint(2, 4))
    sizes = SIZES_BY_CAT.get(cat, [])
    stock = random.randint(0, 35)

    desc = (
        f"{cat} {style} با پارچه {fabric} مناسب فصل {season}. "
        f"طراحی لطیف و دخترانه با رنگ‌های پاستیلی. "
        f"قابل ست با اکسسوری و کفش‌های مینیمال."
    )

    image_url = random.choice(IMAGES_BY_CAT.get(cat, ["/products/placeholder.jpg"]))

    return {
        "title": title,
        "description": desc,
        "category": cat,
        "season": season,
        "price_toman": gen_price(season),
        "sizes": sizes,
        "colors": colors,
        "stock": stock,
        "image_url": image_url,
    }

async def main():
    col = products_collection()

    # اگر می‌خوای هر بار دیتابیس خالی بشه:
    # await col.delete_many({})

    products = [gen_product(i) for i in range(N)]
    await col.insert_many(products)
    print("Seeded products:", len(products))

if __name__ == "__main__":
    asyncio.run(main())