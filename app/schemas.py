from typing import Optional, List
from pydantic import BaseModel

from app.models import Shop_Pydantic


class Status(BaseModel):  # Status msg for errors
    message: str


class UserOut(BaseModel):
    id: int
    login: str
    balance: int
    is_admin: bool
    shop: List[Shop_Pydantic] = None

    class Config:
        orm_mode = True


class SimpleUser(BaseModel):
    login: str
    password: str


class UpdateUser(BaseModel):
    balance: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ShopIn(BaseModel):
    user_id: int
    name: str
    description: str
    price: int
    image: str
    quantity: int

    class Config:
        orm_mode = True

# TODO Сделать красиво, почистить и упорядочить
