from datetime import datetime, timedelta
from jose import JWSError, jwt

from app.utils.constants import Server


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=Server.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update()

    encode_jwt = jwt.encode(to_encode, Server.SECRET_KEY, algorithm=Server.ALGORITHM)

    return encode_jwt
