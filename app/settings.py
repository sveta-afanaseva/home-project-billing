from pydantic import BaseSettings


class DbSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


class AppSettings(BaseSettings):
    host: str

    class Config:
        env_prefix = "APP_"
        env_file = ".env"
