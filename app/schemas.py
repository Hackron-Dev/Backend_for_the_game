from typing import Optional

from pydantic import BaseModel


class Status(BaseModel):  # Status msg for errors
    message: str


class UserOut(BaseModel):
    id: int
    login: str
    balance: int
    is_admin: bool

    class Config:
        orm_mode = True


class CreateSimpleUser(BaseModel):
    login: str
    password: str
    balance: int


class UpdateUser(BaseModel):
    balance: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
