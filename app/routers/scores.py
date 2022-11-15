from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app import schemas, oauth2, models
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


# Post score
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ScoreOut)
def create_scores(score: schemas.CreateScore, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user
)):
    new_score = models.Score(id_user=current_user.id, **score.dict())  # adding score by users id

    db.add(new_score)
    db.commit()
    db.refresh(new_score)

    return new_score
