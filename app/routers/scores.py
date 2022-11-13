from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import engine, get_db
from app import models

router = APIRouter(
    prefix="/scores",
    tags=['Scores']
)


@router.get("/", status_code=status.HTTP_200_OK)
def get_scores(db: Session = Depends(get_db)):
    return db.query(models.Score).all()


@router.get("/", status_code=status.HTTP_201_CREATED)
def create_scores(db: Session = Depends(get_db)):
    pass
