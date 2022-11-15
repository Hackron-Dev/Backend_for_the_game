import hashlib

from fastapi import APIRouter

from app.db.database import conn
from app.models import users
from app.schemas import User_

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/register")
async def create_user(user: User_):
    check_register = conn.execute(users.select().where(users.c.Login == user.Login_)).fetchone()
    hash_password = hashlib.md5(user.Password_.encode()).hexdigest()
    if check_register:
        return {"message": "User already exist"}
    else:
        insLogin = users.insert().values(Login=user.Login_, Hash_Password=hash_password)
        conn.execute(insLogin)
        return {"message": "User created"}


@router.post("/login")
async def create_user(user: User_):
    check_login = conn.execute(users.select().where(users.c.Login == user.Login_)).fetchone()
    hash_password = hashlib.md5(user.Password_.encode()).hexdigest()
    if check_login:
        if check_login.Hash_Password == hash_password:
            return {"message": "Login success"}
        else:
            return {"message": "Wrong password"}
    else:
        return {"message": "User not found"}


@router.get("/get_score/{Login}")
async def get_user_score(Login: str):
    check_login = conn.execute(users.select().where(users.c.Login == Login)).fetchone()
    if check_login:
        return {"message": Login, "score": check_login.Score}
    else:
        return {"message": "User does not exist"}
