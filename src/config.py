from typing import Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    db: str = Field(..., env="POSTGRES_DB")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_password: str = Field(..., env="POSTGRES_PASSWORD")
    db_host: str = Field(..., env="POSTGRES_HOST")
    db_url_: str = Field(env="DATABASE_URL", default_factory=str)

    odoo_db: str = Field(..., env="ODOO_DB")
    odoo_url: str = Field(..., env="ODOO_URL")

    @property
    def db_url(self) -> str:
        if self.db_url_:
            return self.db_url_
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db}"
