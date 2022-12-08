from passlib.context import CryptContext

from app.models import Users, User_Pydantic

# Hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(user_id: int) -> Users:
    user = await Users.get(id=user_id)
    return await User_Pydantic.from_tortoise_orm(user)


def make_member_blank() -> Users:
    db_model = Users()
    Users.save(db_model)
    return Users
