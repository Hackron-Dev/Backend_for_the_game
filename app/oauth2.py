from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, models
from app.db import database
from app.utils.constants import Server

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # I don't know but need for using


def create_access_token(data: dict):  # creating token
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=Server.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update()

    encode_jwt = jwt.encode(to_encode, Server.SECRET_KEY, algorithm=Server.ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credential_exception):  # verify token
    try:
        payload = jwt.decode(token, Server.SECRET_KEY, algorithms=[Server.ALGORITHM])
        id: str = payload.get("current_user")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credential_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):  # get curr user
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exceptions)
    user = db.query(models.User).filter(models.User.id_user == token.id).first()

    return user
