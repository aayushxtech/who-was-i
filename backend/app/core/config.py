from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


# ---------- App ----------

class AppSettings(BaseModel):
    name: str = "who-was-i"
    environment: str = Field(default="development")
    debug: bool = Field(default=False)


# ---------- Server ----------

class ServerSettings(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)


# ---------- Database ----------

class DatabaseSettings(BaseModel):
    # REQUIRED: must come from env
    url: str = Field(
        ...,
        description="PostgreSQL connection URL"
    )

    pool_size: int = Field(default=5)
    echo: bool = Field(default=False)


# ---------- Logging ----------

class LoggingSettings(BaseModel):
    level: str = Field(default="INFO")
    format: str = Field(
        default="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


# ---------- Root Settings ----------

class Settings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    database: DatabaseSettings
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    class Config:
        env_prefix = "WWI_"
        env_nested_delimiter = "__"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """
    Load settings once and cache them.
    Fail fast if required env vars are missing.
    """
    return Settings()
