from logging import getLogger
from typing import Optional
from uuid import uuid4
from xmlrpc.client import ProtocolError

from fastapi import HTTPException
from sqlalchemy import select, update

from models.user import User
from schemas.user import LoginResponseScheme, LoginUserScheme, UserResponseScheme
from services import OdooService, PsqlService

logger = getLogger(__name__)


class UserService:

    __slots__ = ["__psql_service", "odoo_service"]

    def __init__(self, psql_service: PsqlService, odoo_service: OdooService):
        self.__psql_service = psql_service
        self.odoo_service = odoo_service

    async def get_user_from_odoo(self, request: LoginUserScheme) -> Optional[User]:
        try:
            self.odoo_service.login(request.login, request.password)
        except (ProtocolError, TimeoutError):
            raise HTTPException(status_code=500, detail="Паллада не доступна, повторите запрос позже")

        if not self.odoo_service.uid:
            logger.warning("UID is none")
            return None

        fio, group, average = self.odoo_service.get_fio_group_and_average()

        return await self.create_user(fio, request.login, request.password)

    async def get_user(self, request: LoginUserScheme) -> Optional[User]:
        search_query = select(User).where(User.login == request.login)
        result = await self.__psql_service.execute(search_query)
        user = result.scalars().first()
        if user is None:
            logger.warning("Not found user in db, call odoo")
            return await self.get_user_from_odoo(request)
        if user.check_password(request.password):
            return user
        logger.warning("bad password")
        return None

    async def login(self, request: LoginUserScheme) -> LoginResponseScheme:
        if user := await self.get_user(request):
            if not user.token:
                logger.warning("Blank token")
                new_token = str(uuid4())
                update_query = update(User).where(User.login == request.login).values({"token": new_token})
                await self.__psql_service.execute(update_query)
            return LoginResponseScheme(id=user.id, token=user.token)

        logger.warning("Not found user in db and odoo")

        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    async def logout(self, token):
        update_query = update(User).where(User.token == token).values({"token": None})
        await self.__psql_service.execute(update_query)

    async def search_user(self, token) -> UserResponseScheme:
        search_query = select(User)
        search_query = search_query.where(User.token == token)

        result = await self.__psql_service.execute(search_query)
        result = result.scalars().first()
        return UserResponseScheme(id=str(result.id), full_name=result.full_name)

    async def create_user(self, full_name: str, login: str, password: str) -> User:
        user = User(full_name=full_name, login=login, token=str(uuid4()))
        user.set_password(password=password)

        await self.__psql_service.insert_one(user)

        return user
