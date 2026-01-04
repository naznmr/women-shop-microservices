from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    payment_db_url: str = "postgresql+psycopg://payment_service:payment_service@localhost:5432/payment_service"
    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
