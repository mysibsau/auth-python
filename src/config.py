from pydantic import BaseSettings, Field


class Config(BaseSettings):
    db: str = Field(..., env="POSTGRES_DB")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_password: str = Field(..., env="POSTGRES_PASSWORD")
    db_host: str = Field(..., env="POSTGRES_HOST")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db}"
