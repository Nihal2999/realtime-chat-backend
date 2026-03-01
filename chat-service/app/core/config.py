from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    MONGODB_URL: str
    MONGODB_DB: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()