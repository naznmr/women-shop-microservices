# Database Schema Design (PostgreSQL + MongoDB)

This project uses **database-per-service**:
- PostgreSQL for: User Service, Order Service, Payment Service
- MongoDB for: Product Service

There are **no cross-service foreign keys** (microservices boundary). Services exchange data via REST and events.

---

## 1) User Service DB (PostgreSQL) — database: `user_service`

### Table: `users`
Stores user identity and authentication data.

| Column | Type | Null | Constraints / Notes |
|---|---|---:|---|
| id | INTEGER | NO | Primary Key (auto increment / identity) |
| email | VARCHAR(255) | NO | **UNIQUE**, indexed |
| full_name | VARCHAR(255) | NO | |
| hashed_password | VARCHAR(255) | NO | Password hash (never store raw password) |
| phone | VARCHAR(50) | YES | optional |
| created_at | TIMESTAMPTZ | NO | default = now() |

**Indexes**
- PK on `id`
- Unique index on `email`
- Index on `email` (for fast login/search)

---

## 2) Order Service DB (PostgreSQL) — database: `order_service`

### Table: `orders`
Stores order header (tracking) data.

| Column | Type | Null | Constraints / Notes |
|---|---|---:|---|
| id | INTEGER | NO | Primary Key (auto increment / identity) |
| user_email | VARCHAR(255) | NO | indexed (user tracking) |
| status | VARCHAR(30) | NO | e.g. `created`, `paid`, `failed`, `cancelled`, `shipped`, `delivered` |
| total_toman | INTEGER | NO | default 0 |
| created_at | TIMESTAMPTZ | NO | default = now() |

**Indexes**
- PK on `id`
- Index on `user_email`

---

### Table: `order_items`
Stores order line items (snapshot of product data at purchase time).

| Column | Type | Null | Constraints / Notes |
|---|---|---:|---|
| id | INTEGER | NO | Primary Key (auto increment / identity) |
| order_id | INTEGER | NO | **FK → orders.id**, indexed |
| product_id | VARCHAR(64) | NO | Product Mongo ObjectId as string |
| title | VARCHAR(200) | NO | Product title snapshot |
| unit_price_toman | INTEGER | NO | Price snapshot |
| qty | INTEGER | NO | default 1 |

**Relationships**
- `order_items.order_id` references `orders.id`
- On delete order → delete its items (cascade in ORM)

**Indexes**
- PK on `id`
- Index on `order_id`

---

## 3) Payment Service DB (PostgreSQL) — database: `payment_service`

### Table: `payments`
Stores payment results (success/failure simulation supported).

| Column | Type | Null | Constraints / Notes |
|---|---|---:|---|
| id | INTEGER | NO | Primary Key (auto increment / identity) |
| order_id | VARCHAR(64) | NO | indexed; order id stored as string |
| amount_toman | INTEGER | NO | |
| status | VARCHAR(20) | NO | `success` or `failed` |
| created_at | TIMESTAMPTZ | NO | default = now() |

**Indexes**
- PK on `id`
- Index on `order_id`

---

## 4) Product Service DB (MongoDB) — database: (env `MONGO_DB`), collection: `products`

### Collection: `products`
Each document represents one product.

**Document structure**
```json
{
  "_id": "ObjectId",
  "title": "string (2..200)",
  "description": "string (<=2000)",
  "category": "string (2..100)",
  "season": "بهار | تابستان | پاییز | زمستان",
  "price_toman": "int (>=0)",
  "sizes": ["string"],
  "colors": ["string"],
  "stock": "int (>=0)",
  "image_url": "string | null"
}