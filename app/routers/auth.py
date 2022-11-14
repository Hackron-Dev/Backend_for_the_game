from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from app.db import database
from app import models, schemas, oauth2
from app.utils import jwt_utils

router = APIRouter(
    tags=['Authentications']
)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.login == user_credentials.login).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not jwt_utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id_user})

    return {"access_token": access_token, "token_type": "bearer"}
