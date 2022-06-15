from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    Configurações gerais usadas na aplicação.
    """

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API de Curso"
    DB_URL: str = "postgresql+asyncpg://tony:123@localhost:5432/university"
    DBBaseModel: declarative_base = declarative_base()

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
