# گزارش نهایی (Template)

## 1) تصمیم‌های طراحی
- چرا FastAPI؟ (Swagger خودکار، سرعت توسعه، مناسب میکروسرویس)
- چرا PostgreSQL برای User/Order/Payment؟ (تراکنش/یکپارچگی)
- چرا MongoDB برای Product؟ (انعطاف اسکیمای محصولات)

## 2) استراتژی ارتباطی
- Sync: REST بین Order↔Payment و Order↔Product
- Async: RabbitMQ بین Order→Notification (event-driven)

## 3) تحمل خطا
- retry با Tenacity
- circuit breaker با pybreaker

## 4) دیپلوی
- Docker Compose محلی
- Kubernetes + Ingress (Minikube)

## 5) مانیتورینگ
- Prometheus scrape `/metrics`
- Grafana dashboard

## 6) تست‌ها
- Unit tests برای Payment
- Load test با k6

## 7) چالش‌ها و بهبودهای آینده
- Idempotency در پرداخت
- Saga/Outbox pattern برای تضمین ارسال رویداد
- API Gateway رسمی (Kong/Istio)
