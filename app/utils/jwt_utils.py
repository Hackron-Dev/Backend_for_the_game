from app import models
from passlib.context import CryptContext

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(session: AsyncSession, user_id: int) -> models.Users:
    stmt = select(models.Users).filter(models.Users.id == user_id)
    r = await session.execute(stmt)
    db_model = r.scalars().first()
    return db_model


def make_member_blank() -> models.Users:
    return models.Users
