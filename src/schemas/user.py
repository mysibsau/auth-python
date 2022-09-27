from pydantic import UUID4, BaseModel, Field


class TokenScheme(BaseModel):
    token: str = Field(...)


class LoginUserScheme(BaseModel):
    login: str = Field(...)
    password: str = Field(...)


class ErrorScheme(BaseModel):
    message: str


class LoginResponseScheme(BaseModel):
    id: UUID4
    token: UUID4


class UserResponseScheme(BaseModel):
    id: str = Field(...)
    full_name: str = Field(...)
