from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API de Curso"
    DB_URL: str = "postgresql+asyncpg://tony:123@localhost:5432/university2"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings: Settings = Settings()
