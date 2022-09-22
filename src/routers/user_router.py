from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from di_container import Container
from schemas.user import LoginUserScheme
from services.user_service import UserService

router = APIRouter(tags=["user"])


@router.post("/login/", response_model=str)
@inject
async def login(request: LoginUserScheme, user_service: UserService = Depends(Provide[Container.user_service])):
    return await user_service.create_token(request)


@router.post("/logout/")
@inject
async def logout(token: str, user_service: UserService = Depends((Provide[Container.user_service]))):
    return await user_service.logout(token)


@router.post("/me")
@inject
async def me(token: str, user_service: UserService = Depends((Provide[Container.user_service]))):
    return await user_service.search_user(token)
