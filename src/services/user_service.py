from uuid import uuid4

from sqlalchemy import update, select

from services import PsqlService
from schemas.user import LoginUserScheme, UserResponseScheme
from models.user import User


class UserService:

    __slots__ = '__psql_service'

    def __init__(self, psql_service: PsqlService):
        self.__psql_service = psql_service

    async def create_token(self, request: LoginUserScheme):
        search_query = select(User)
        search_query = search_query.where(User.login == request.login)
        result = await self.__psql_service.execute(search_query)
        user = result.scalars().first()
        if (user is not None) and user.check_password(request.password):
            new_token = str(uuid4())
            update_query = (
                update(User)
                .where(User.login == request.login)
                .values({
                    "token": new_token
                })
            )
            await self.__psql_service.execute(update_query)
            return new_token

        else:
            return "Неверный логин или пароль"

    async def logout(self, token):
        update_query = (
                update(User)
                .where(User.token == token)
                .values({
                    "token": None
                })
            )
        await self.__psql_service.execute(update_query)

    async def search_user(self, token) -> UserResponseScheme:
        search_query = select(User)
        search_query = search_query.where(User.token == token)

        result = await self.__psql_service.execute(search_query)
        result = result.scalars().first()
        return UserResponseScheme(
            id=str(result.id),
            full_name=result.full_name
        )

    async def create_user(self, full_name: str, login: str, password: str):
        user = User(full_name=full_name, login=login)
        user.set_password(password=password)

        await self.__psql_service.insert_one(user)
