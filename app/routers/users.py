import tortoise
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app import oauth2, schemas
from app.utils import jwt_utils
from app.models import Users, User_Pydantic

router = APIRouter(tags=["Users"], prefix="/users")
user_router = APIRouter(dependencies=[Depends(oauth2.JWTBearer), Depends(oauth2.oauth2_scheme)])


@router.get("", response_model=List[schemas.UserOut])
async def get_users():
    user = await User_Pydantic.from_queryset(Users.filter(is_admin=False))
    return user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user_by_id(user_id: int):
    try:
        user = await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


@router.get("/login/{login}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user_by_login(login: str):
    try:
        user = await User_Pydantic.from_queryset_single(Users.get(login=login, is_admin=False))
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with login {login} not found")
    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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


@user_router.delete("/{user_id}", status_code=status.HTTP_410_GONE, response_model=schemas.Status)
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id, is_admin=False).delete()
    if not deleted_count:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return schemas.Status(message=f"Deleted form_data {user_id}")


router.include_router(user_router)
# TODO сделать так чтобы админ мог удалять кого хочет, а не админ могу удалить только свой аккаунт
# TODO try: except for `put` and `delete`
