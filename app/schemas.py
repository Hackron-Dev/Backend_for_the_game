from pydantic import BaseModel


class CreateUser(BaseModel):
    login: str
    password: str
    mcoin: int
    rcoin: int


class LoginUser(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True
