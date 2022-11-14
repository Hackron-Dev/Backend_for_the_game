from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas
from app import models
from app.db.database import get_db

# initialize router settings
router = APIRouter(
    prefix="/scores",
    tags=['Scores']
)


# Get all scores
@router.get("/", status_code=status.HTTP_200_OK)
def get_scores(db: Session = Depends(get_db)):
    return db.query(models.Score).all()


# Post score  TODO: depends on user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ScoreOut)
def create_scores(score: schemas.Score, db: Session = Depends(get_db)):
    pass
