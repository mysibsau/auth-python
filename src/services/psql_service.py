from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Base


class PsqlService:
    def __init__(self, config: Config):

        self.__engine = create_async_engine(config.db_url)
        self.__async_session = sessionmaker(self.__engine, expire_on_commit=False, class_=AsyncSession)

    @asynccontextmanager
    async def __session_scope(self) -> AsyncSession:

        session = self.__async_session()

        try:
            await session.begin()
            yield session
            await session.commit()
        except Exception as ex:
            await session.rollback()
            raise ex
        finally:
            await session.close()

    async def insert_one(self, data: Base) -> None:

        async with self.__session_scope() as session:
            session.add(data)
            await session.flush()

    async def execute(self, query: Any) -> ChunkedIteratorResult:

        async with self.__session_scope() as session:
            return await session.execute(query)
