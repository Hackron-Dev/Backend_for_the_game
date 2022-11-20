from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette import status

from app import oauth2
from app.models import User_Pydantic, UserIn_Pydantic, Users
from app.utils import jwt_utils
from app.schemas import UserOut, Token

router = APIRouter(
    tags=['Auth']
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)  # Create user
async def create_user(user: UserIn_Pydantic):
    user.password = jwt_utils.hash_(user.password)  # hashing password
    user_obj = await Users.create(**user.dict())
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post("/login", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    users = await User_Pydantic.from_queryset_single(Users.get(login=user.username))

    if not jwt_utils.verify(user.password, users.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_token(data={"current_user": users.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/admin")
async def root():
    pass
