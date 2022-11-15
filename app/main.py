from fastapi import FastAPI

from app.db.database import Base, engine
from app.routers import users

app = FastAPI()

Base.metadata.create_all(engine)
# Сделать запрос о добавление  user Done
# Сделать запрос о получение  user score
# Сделать запрос о редактирование cash user


app.include_router(users.router)  # users router
