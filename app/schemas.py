from pydantic import BaseModel


class Status(BaseModel):  # Status msg for errors
    message: str


class UserOut(BaseModel):
    id: int
    login: str
    balance: str
