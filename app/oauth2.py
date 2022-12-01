from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, cast
from enum import Enum

from app import schemas
from app.utils import jwt_utils
from app.utils.constants import Server
from app.utils.jwt_utils import get_user
from app.models import User_Pydantic, Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthState(Enum):
    """Represents possible outcomes of a member attempting to authorize."""

    NO_TOKEN = (
        "There is no token provided, provide one in an Authorization header in the format 'Bearer {your token here}'."
        "If you don't have a token, ask an administrator to generate you one."
    )
    INVALID_TOKEN = (
        "The token provided is not a valid token or has expired, ask an administrator to generate you a new token."
    )
    NEEDS_ADMIN = "This endpoint is limited to admins."


def validate_token(token: Optional[str], needs_admin: bool = False) -> tuple[schemas.TokenData, Users]:
    """Check given token and matches our database"""
    if token is None:
        return HTTPException(status.HTTP_403_FORBIDDEN, AuthState.NO_TOKEN.value)
    try:
        token_data = cast(schemas.TokenData, jwt.decode(token, Server.SECRET_KEY, algorithms=[Server.ALGORITHM]))
    except JWTError:
        raise HTTPException(403, AuthState.INVALID_TOKEN.value)
    member = get_user(int(token_data["current_user"]))

    if member is None:
        raise HTTPException(403, AuthState.INVALID_TOKEN.value)
    if needs_admin and not member[1]:
        return HTTPException(403, AuthState.NEEDS_ADMIN.value)

    return token_data, member


class JWTBearer(HTTPBearer):
    """Dependency for routes to enforce JWT auth."""

    def __init__(self, auto_error: bool = True, require_admin: bool = False):
        super().__init__(auto_error=auto_error)
        self.require_admin = require_admin

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """Check if the supplied credentials are valid for this endpoint."""
        credentials = cast(HTTPAuthorizationCredentials, await super().__call__(request))
        jwt_token = credentials.credentials
        _, member = await validate_token(jwt_token, needs_admin=self.require_admin)

        # Token is valid, store the member_id and is_admin data into the request
        request.state.member = member
        request.state.is_admin = member
        return credentials


def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=Server.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, Server.SECRET_KEY, algorithm=Server.ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, Server.SECRET_KEY, algorithms=[Server.ALGORITHM])
        id: str = payload.get("current_user")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials",
                                           headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exceptions)
    user = User_Pydantic.from_queryset_single(Users.get(id=token.id))
    return user


# TODO generate new member with admin roots
def generate_member(member: Users) -> schemas.TokenData:
    """Member with admin status and ID"""
    return schemas.TokenData(current_user=member.id, is_admin=member.is_admin)
