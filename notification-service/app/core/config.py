from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_ID: str

    class Config:
        env_file = ".env"

settings = Settings()