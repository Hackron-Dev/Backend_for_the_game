from typing import Optional

from pydantic import BaseModel


# region: User
class UserOut(BaseModel):
    id: int
    login: str
    balance: int
    is_admin: bool

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    balance: int


class SimpleUser(BaseModel):
    login: str
    password: str


# endregion

# region: Shop
class ShopIn(BaseModel):
    user_id: int
    name: str
    description: str
    price: int
    image: str
    quantity: int

    class Config:
        orm_mode = True


# endregion

# region: Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# endregion

class Status(BaseModel):
    message: str
