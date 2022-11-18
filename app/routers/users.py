import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/register")
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hash_password = hashlib.md5(user.password.encode()).hexdigest()
    user.password = hash_password
    try:
        new_user = models.Users(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This login already have been used")


@router.post("/login", response_model=schemas.LoginUser)
def create_user(user: schemas.LoginUser, db: Session = Depends(get_db)):
    check_login = db.query(models.Users).filter(models.Users.login == user.login).first()
    hash_password = hashlib.md5(user.password.encode()).hexdigest()
    if check_login:
        if check_login.password == hash_password:
            return check_login
        else:
            return {"Login or password is not correct"}
    else:
        return {"message": "User not found"}


# TODO: add update user score
@router.get("/get_score/{login}")
async def get_user_score(login: str, db: Session = Depends(get_db)):
    check_login = db.query(models.Users).filter(models.Users.login == login).first()
    if check_login:
        return {"message": login, "Mcoin": check_login.mcoin, "Rcoin": check_login.rcoin}
    else:
        return {"message": "User does not exist"}
