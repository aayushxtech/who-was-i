from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


settings = Settings()
