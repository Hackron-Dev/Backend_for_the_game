from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app import schemas
from app.utils.constants import Server
from app.models import User_Pydantic, UserIn_Pydantic, Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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
