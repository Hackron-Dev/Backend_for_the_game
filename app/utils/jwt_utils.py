from passlib.context import CryptContext
from app.models import Users, User_Pydantic

from ._db import cur

# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(user_id: int):
    user = cur.execute(f"SELECT id, is_admin from USERS WHERE id={user_id}")
    return list(user)


def make_member_blank() -> Users:
    return Users
