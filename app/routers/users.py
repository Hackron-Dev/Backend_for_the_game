from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.models import Users, User_Pydantic, UserIn_Pydantic
from app.utils import jwt_utils

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.get("/", response_model=List[User_Pydantic])  # Get All users
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_Pydantic)  # Create user
async def create_user(user: UserIn_Pydantic):
    user.password = jwt_utils.hash_(user.password)  # hashing password
    user_obj = await Users.create(**user.dict())
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User_Pydantic)  # Get user by id
async def get_user_by_id(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.put("/{user_id}", status_code=status.HTTP_426_UPGRADE_REQUIRED, response_model=User_Pydantic)  # Update user
async def update_user(user_id: int, user: UserIn_Pydantic):
    user.password = jwt_utils.hash_(user.password)
    await Users.filter(id=user_id).update(**user.dict())
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


class Status(BaseModel):  # Status msg for errors
    message: str


@router.delete("/{user_id}", status_code=status.HTTP_410_GONE, response_model=Status)  # Delete user
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Status(message=f"Deleted user {user_id}")
