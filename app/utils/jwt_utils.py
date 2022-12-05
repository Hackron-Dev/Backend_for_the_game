from fastapi import HTTPException

from app import models
from passlib.context import CryptContext

# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(user_id: int) -> models.Users:
    user = await models.Users.get(id=user_id)
    return await models.User_Pydantic.from_tortoise_orm(user)


def make_member_blank() -> models.Users:
    return models.Users
