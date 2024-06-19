import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE = os.path.join(BASE_DIR, ".env")


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class DbSettings(CustomSettings):
    mysql_root_password: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    echo: bool = True

    @property
    def db_url(self):
        return (f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}@"
                f"{self.mysql_host}:{self.mysql_port}/{self.mysql_database}")


class RedisSettings(CustomSettings):
    redis_host: str
    redis_port: int
    cache_db: int
    broker_url: str

    @property
    def cache_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.cache_db}"


class Settings(CustomSettings):
    app_url: str
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
