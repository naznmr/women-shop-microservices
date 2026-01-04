# فروشگاه میکروسرویسی لباس زنانه 

طراحی، توسعه و استقرار یک سامانه‌ی تجارت‌الکترونیک مبتنی بر معماری میکروسرویس:
- User Service (احراز هویت JWT + پروفایل)
- Product Service (کاتالوگ محصولات + جستجو)
- Order Service (ثبت سفارش + اتصال به پرداخت + انتشار رویداد)
- Payment Service (شبیه‌سازی پرداخت + خطا)
- Notification Service (مصرف رویدادها از RabbitMQ و ارسال اعلان — شبیه‌سازی)

---

## 1) اجرای سریع با Docker Compose

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
# سپس در فایل hosts دامنه‌های زیر را به IP بالا نگاشت کنید:
# api.womenswear.local / shop.womenswear.local
```

---

## 4) تست‌ها و لودتست
- Unit/Integration: `pytest` داخل سرویس‌ها
- Load test: پوشه `tests/k6/`

---

- طراحی معماری + قراردادهای API + طراحی DB
- پیاده‌سازی سرویس‌ها
- ارتباط sync (REST) و async (RabbitMQ)
- تحمل خطا: retry + circuit breaker در Order Service
- Docker + Compose + Kubernetes YAML + Ingress
- CI/CD با GitHub Actions
- Monitoring با Prometheus/Grafana
