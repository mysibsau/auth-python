from pydantic import BaseModel, Field, UUID4


class TokenScheme(BaseModel):
    token: str = Field(...)


class LoginUserScheme(BaseModel):
    login: str = Field(...)
    password: str = Field(...)


class UserResponseScheme(BaseModel):
    id: str = Field(...)
    full_name: str = Field(...)
