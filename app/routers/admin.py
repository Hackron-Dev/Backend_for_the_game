from typing import List

import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.oauth2 import JWTBearer, oauth2_scheme
from app.models import Users, User_Pydantic, UserIn_Pydantic
from app.schemas import UserOut
from app.utils import jwt_utils

router = APIRouter(
    tags=["Admin-only endpoints"],
    dependencies=[Depends(JWTBearer(require_admin=True)), Depends(oauth2_scheme)],
)


@router.get("/admin")
async def admin_check() -> Response:
    """Check if the authenticated member is an admin."""
    return Response("You're an admin!")


@router.get("/member", response_model=List[UserOut])
async def get_admin():
    user = await User_Pydantic.from_queryset(Users.all())
    return user


@router.get("/member/{id}", response_model=UserOut)
async def get_member(id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=id))


@router.post("/member", response_model=UserOut)
async def add_user(user: UserIn_Pydantic, is_admin: bool = False):
    """Create a new member."""
    user.password = jwt_utils.hash_(user.password)
    user.is_admin = is_admin
    try:
        user_obj = await Users.create(**user.dict())
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with this login already exist")
    return await User_Pydantic.from_tortoise_orm(user_obj)

# TODO form_data router.patch and learn what is it
