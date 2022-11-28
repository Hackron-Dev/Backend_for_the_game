from passlib.context import CryptContext
from app.models import Users, User_Pydantic

# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(user_id: int) -> Users:
    return User_Pydantic.from_queryset_single(Users.get(id=user_id))


def make_member_blank() -> Users:
    return Users
