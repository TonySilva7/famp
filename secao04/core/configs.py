from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://tony:123@localhost:5432/university4"
    DBBaseModel: declarative_base = declarative_base()

    """
    PS. O token em JWT_SECRET foi gerado pelo seguinte comando:
    import secrets
    token: str = secrets.token_urlsafe(32)
    print(token)
    """

    JWT_SECRET: str = "raNAfXV6bpEm8zpteNtFNCNeo2MmgE5IfzK46QuMk1s"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    class Config:
        env_file = ".env"
        case_sensitive = True


settings: Settings = Settings()
