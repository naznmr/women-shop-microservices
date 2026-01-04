from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    order_db_url: str = "postgresql+psycopg://order_service:order_service@localhost:5432/order_service"
    user_service_url: str = "http://localhost:8001"
    product_service_url: str = "http://localhost:8002"
    payment_service_url: str = "http://localhost:8004"

    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_exchange: str = "orders"
    rabbitmq_queue: str = "order_events"

    jwt_secret: str = "change_me"
    jwt_alg: str = "HS256"

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
