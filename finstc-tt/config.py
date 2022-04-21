from functools import lru_cache
from os import environ

from pydantic import BaseSettings


class Config(BaseSettings):
    db_user: str = environ.get("DB_USER", "")
    db_password: str = environ.get("DB_PASSWORD", "")
    db_address: str = environ.get("DB_ADDRESS", "")
    db_name: str = environ.get("DB_NAME", "")
    db_url: str = (
        f"mysql+pymysql://{db_user}:{db_password}@{db_address}/{db_name}"
    )
    service_port: int = int(environ.get("SERVICE_PORT", 3520))
    service_host: str = environ.get("SERVICE_HOST", "10.50.2.10")
    log_level: str = environ.get("LOG_LEVEL", "debug")


@lru_cache
def get_config() -> Config:
    return Config()
