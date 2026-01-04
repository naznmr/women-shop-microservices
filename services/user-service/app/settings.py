from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    user_db_url: str = "postgresql+psycopg://user_service:user_service@localhost:5432/user_service"
    jwt_secret: str = "change_me"
    jwt_alg: str = "HS256"
    jwt_expire_minutes: int = 60

    class Config:
        env_prefix = ""
        case_sensitive = False

settings = Settings()
