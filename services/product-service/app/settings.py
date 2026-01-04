from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "product_service"
    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
