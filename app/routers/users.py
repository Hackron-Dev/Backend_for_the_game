import tortoise
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app import oauth2, schemas
from app.utils import jwt_utils
from app.models import Users, User_Pydantic

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)
user_router = APIRouter(
    prefix="/users",
    dependencies=[Depends(oauth2.oauth2_scheme), Depends(oauth2.JWTBearer)]
)


@router.get("", response_model=List[schemas.UserOut])  # Get All users
async def get_users():
    user = await User_Pydantic.from_queryset(Users.filter(is_admin=False).all())
    return user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)  # Get form_data by id
async def get_user_by_id(user_id: int):
    user = await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  # Create form_data
async def create_user(user: schemas.SimpleUser):
    user.password = jwt_utils.hash_(user.password)  # hashing password
    try:
        user_obj = await Users.create(**user.dict())
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with this login already exist")
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.put("/{user_id}", status_code=status.HTTP_426_UPGRADE_REQUIRED,
                 response_model=schemas.UserOut)  # Update form_data
async def update_user(user_id: int, user: schemas.UpdateUser):
    await Users.filter(id=user_id).update(**user.dict())
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@user_router.delete("/{user_id}", status_code=status.HTTP_410_GONE, response_model=schemas.Status)  # Delete form_data
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id, is_admin=False).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return schemas.Status(message=f"Deleted form_data {user_id}")


router.include_router(user_router)
# TODO сделать так чтобы админ мог удалять кого хочет, а не админ могу удалить только свой аккаунт
