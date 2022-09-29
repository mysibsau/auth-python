from typing import Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    db: str = Field(..., env="POSTGRES_DB")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_password: str = Field(..., env="POSTGRES_PASSWORD")
    db_host: str = Field(..., env="POSTGRES_HOST")
    _db_url: Optional[str] = Field(None, env="DATABASE_URL")

    odoo_db: str = Field(..., env="ODOO_DB")
    odoo_url: str = Field(..., env="ODOO_URL")

    @property
    def db_url(self) -> str:
        if self._db_url is not None:
            return self._db_url
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db}"
