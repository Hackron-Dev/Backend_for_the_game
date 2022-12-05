from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import oauth2
from app.schemas import Token

router = APIRouter(
    tags=['Auth']
)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = await oauth2.authenticate_user(form_data.username, form_data.password)

    access_token = oauth2.create_token(data={"current_user": users.id})
    return {"access_token": access_token, "token_type": "bearer"}
