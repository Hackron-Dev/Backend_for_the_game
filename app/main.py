from fastapi import FastAPI

from app.db.database import metadata, engine
from app.routers import users
app = FastAPI()#

metadata.create_all(engine)
# Сделать запрос о добавление  user Done
# Сделать запрос о получение  user score
# Сделать запрос о редактирование cash user


app.include_router(users.router)  # users router