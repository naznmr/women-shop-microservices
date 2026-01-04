```mermaid
flowchart LR
  FE[Frontend (Next.js RTL)] -->|REST| O[Order Service]
  FE -->|REST| P[Product Service]
  FE -->|REST| U[User Service]

  O -->|REST| Pay[Payment Service]
  O -->|RabbitMQ Event: order_paid| MQ[(RabbitMQ)]
  MQ --> N[Notification Service]

  U --> UDB[(PostgreSQL)]
  O --> ODB[(PostgreSQL)]
  Pay --> PayDB[(PostgreSQL)]
  P --> MDB[(MongoDB)]

  Prom[(Prometheus)] --> U
  Prom --> P
  Prom --> O
  Prom --> Pay
  Prom --> N
  Graf[(Grafana)] --> Prom
```
