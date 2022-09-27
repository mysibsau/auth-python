from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from di_container import Container
from schemas.user import LoginResponseScheme, LoginUserScheme, UserResponseScheme
from services.user_service import UserService

router = APIRouter(tags=["user"])


@router.post("/login/", response_model=LoginResponseScheme)
@inject
async def login(request: LoginUserScheme, user_service: UserService = Depends(Provide[Container.user_service])):
    return await user_service.login(request)


@router.post("/logout/")
@inject
async def logout(token: str, user_service: UserService = Depends((Provide[Container.user_service]))):
    return await user_service.logout(token)


@router.post("/me", response_model=UserResponseScheme)
@inject
async def me(token: str, user_service: UserService = Depends((Provide[Container.user_service]))):
    return await user_service.search_user(token)
