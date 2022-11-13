from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import engine, get_db
from app import models

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/")
def user(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user():
    return {"Some": "user info"}


# FOR VANYA
@router.get("/{id}{znak}{id2}")
def calc(id: int, znak, id2: int):
    if znak == '+':
        return id + id2
