from fastapi import APIRouter, status, HTTPException, Depends


router = APIRouter()


@router.get("/user")
def user():
    return {"Some": "user stuff"}


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user():
    return {"Some": "user info"}
