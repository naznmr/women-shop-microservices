from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    rabbitmq_exchange: str = "orders"
    rabbitmq_queue: str = "order_events"

    # DB
    notification_db_url: str = "postgresql+psycopg://notification_service:notification_service@notification-db:5432/notification_service"

    # SMTP (MailHog by default)
    smtp_host: str = "mailhog"
    smtp_port: int = 1025
    smtp_from: str = "no-reply@women-shop.local"

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()