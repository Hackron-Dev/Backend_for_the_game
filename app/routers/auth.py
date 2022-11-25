import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import oauth2
from app.models import User_Pydantic, UserIn_Pydantic, Users
from app.utils import jwt_utils
from app.schemas import UserOut, Token

router = APIRouter(
    tags=['Auth']
)
user_router = APIRouter(dependencies=[Depends(oauth2.JWTBearer())])


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)  # Create user
async def create_user(user: UserIn_Pydantic, is_admin: bool = False):
    user.password = jwt_utils.hash_(user.password)  # hashing password
    user.id_admin = is_admin
    try:
        user_obj = await Users.create(**user.dict())
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with this login already exist")
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.post("/login", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends()):
    users = await User_Pydantic.from_queryset_single(Users.get(login=user.username))

    if not jwt_utils.verify(user.password, users.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_token(data={"current_user": users.id})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/admin")
async def root():
    return "You are admin"
