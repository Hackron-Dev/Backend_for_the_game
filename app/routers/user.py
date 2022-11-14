from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import engine, get_db
from app.utils import jwt_utils
from app import models
from app import schemas

# initialize router settings
router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# Get all users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def user(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# Create new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    hashed_password = jwt_utils.hash_(user.password)
    user.password = hashed_password
    try:
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This login already have been used")


# FOR VANYA
@router.get("/{id}{znak}{id2}")
def calc(id: int, znak, id2: int):
    if znak == '+':
        return id + id2
