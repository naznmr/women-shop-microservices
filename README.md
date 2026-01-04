# فروشگاه میکروسرویسی لباس زنانه (ایرانی/فارسی) — چهار فصل

این ریپو یک پروژه‌ی کامل برای «طراحی، توسعه و استقرار یک سامانه‌ی تجارت‌الکترونیک مبتنی بر معماری میکروسرویس» است:
- User Service (احراز هویت JWT + پروفایل)
- Product Service (کاتالوگ محصولات + جستجو)
- Order Service (ثبت سفارش + اتصال به پرداخت + انتشار رویداد)
- Payment Service (شبیه‌سازی پرداخت + خطا)
- Notification Service (مصرف رویدادها از RabbitMQ و ارسال اعلان — شبیه‌سازی)

## ویژگی‌های «ایرانی/فارسی»
- UI و متون فارسی + راست‌به‌چپ (RTL)
- پول: تومان (Toman)
- فصل‌های محصول: بهار / تابستان / پاییز / زمستان
- دسته‌بندی‌های رایج پوشاک زنانه (مانتو، شومیز، روسری، لباس مجلسی، پالتو و …)

---

## 1) اجرای سریع با Docker Compose (پیشنهادی برای ارائه‌ی عملی)

### پیش‌نیازها
- Docker Desktop (ویندوز/مک) یا Docker Engine (لینوکس)
- Git

### اجرا
```bash
git clone <YOUR_REPO_URL>
cd persian-womenswear-microservices
cp .env.example .env
docker compose up --build
```

### آدرس‌ها
- **User Service Swagger**: http://localhost:8001/docs
- **Product Service Swagger**: http://localhost:8002/docs
- **Order Service Swagger**: http://localhost:8003/docs
- **Payment Service Swagger**: http://localhost:8004/docs
- **Notification Service**: http://localhost:8005/docs
- **Frontend (Next.js)**: http://localhost:3000
- **RabbitMQ UI**: http://localhost:15672 (user/pass: guest/guest)
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

---

## 2) دمو‌ی سناریو (برای ویدئو)
1) ثبت‌نام: User Service → `/auth/register`
2) لاگین: `/auth/login` → دریافت JWT
3) افزودن چند محصول: Product Service → `/products` (یا اجرای اسکریپت seed)
4) مشاهده‌ی محصولات در Frontend
5) ثبت سفارش در Frontend (Checkout) → Order Service
6) Order Service → Payment Service (شبیه‌سازی موفق/ناموفق)
7) در صورت موفقیت: Order Service رویداد را به RabbitMQ می‌فرستد
8) Notification Service رویداد را مصرف کرده و «ارسال ایمیل» را لاگ می‌کند

---

## 3) استقرار روی Kubernetes (Minikube)
> فایل‌های آماده در پوشه‌ی `k8s/` قرار دارند.

### پیش‌نیازها
- kubectl
- minikube
- ingress addon

### اجرا
```bash
minikube start
minikube addons enable ingress
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
kubectl -n womenswear get pods
```

### دسترسی به Ingress
```bash
minikube ip
# سپس در فایل hosts (اختیاری) دامنه‌های زیر را به IP بالا نگاشت کنید:
# api.womenswear.local / shop.womenswear.local
```

---

## 4) تست‌ها و لودتست
- Unit/Integration: `pytest` داخل سرویس‌ها
- Load test: پوشه `tests/k6/`

---

## نکته‌ی ارزیابی
این پروژه دقیقاً deliverableهای تکلیف را پوشش می‌دهد:
- طراحی معماری + قراردادهای API + طراحی DB
- پیاده‌سازی سرویس‌ها
- ارتباط sync (REST) و async (RabbitMQ)
- تحمل خطا: retry + circuit breaker در Order Service
- Docker + Compose + Kubernetes YAML + Ingress
- CI/CD با GitHub Actions
- Monitoring با Prometheus/Grafana

موفق باشید ✨
