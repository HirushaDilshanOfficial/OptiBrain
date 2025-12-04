from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "OptiBrain"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "optibrain"
    
    # Security
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE" # Change this in production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    # ML Service
    ML_SERVICE_URL: str = "http://ml:8001"

    class Config:
        case_sensitive = True

settings = Settings()
