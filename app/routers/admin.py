# Only admin router
import tortoise
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.oauth2 import JWTBearer
from app.models import Users, User_Pydantic, UserIn_Pydantic
from app.schemas import UserOut
from app.utils import jwt_utils

router = APIRouter(
    tags=["Admin-only endpoints"],
    dependencies=[Depends(JWTBearer(require_admin=True))],
)


@router.get("/admin")
async def admin_check() -> Response:
    """Check if the authenticated member is an admin."""
    return Response("You're an admin!")


@router.get("/users/{id}", response_model=UserOut)
async def get_member(id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=id))


@router.post("/users", response_model=UserOut)
async def add_user(user: UserIn_Pydantic, is_admin: bool = False):
    """Create a new member."""
    user.password = jwt_utils.hash_(user.passowrd)
    user.is_admin = is_admin
    try:
        user_obj = await Users.create(**user.dict())
    except tortoise.exceptions.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with this login already exist")
    return await User_Pydantic.from_tortoise_orm(user_obj)

# TODO user router.patch and learn what is it
