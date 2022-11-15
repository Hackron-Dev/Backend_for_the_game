from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: int = Field(alias="id_user")  # для того чтобы читать как id_user и писать как id
    login: str
    create_date = datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    login: str
    password: str


class ScoreOut(BaseModel):
    id: int = Field(alias="id_user")
    score: int
    create_at: datetime


class CreateScore(BaseModel):
    score: int


class TokenData(BaseModel):
    id: Optional[str] = None
