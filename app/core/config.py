"""Модуль настройки приложения."""
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Класс настроек."""
    app_title: str = 'Input title in .env'
    app_title: str = 'Later'
    app_description: str = 'Later'
    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_host: str = 'postgres_container'
    postgres_port: str = '5432'
    pgdata: str = '/var/lib/postgresql/data/pgdata'
    secret: str = 'SECRET'

    class Config:
        """Класс конфигурации класса настроек."""
        env_file = '.env'


settings = Settings()
