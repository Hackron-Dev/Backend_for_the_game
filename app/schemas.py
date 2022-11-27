from typing import Optional

from pydantic import BaseModel


class Status(BaseModel):  # Status msg for errors
    message: str


class UserOut(BaseModel):
    id: int
    login: str
    balance: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
