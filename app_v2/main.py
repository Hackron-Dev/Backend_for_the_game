from fastapi import FastAPI

from app_v2.routers import users
from app_v2.db.database import init_db

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="TESTETSETSE")

app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    init_db(app)
