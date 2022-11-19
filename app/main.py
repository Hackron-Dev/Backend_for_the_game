from fastapi import FastAPI

from app.routers import users
from app.routers import shop
from app.db.database import init_db

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="TESTETSETSE")

app.include_router(users.router)
app.include_router(shop.router)



@app.on_event("startup")
async def startup_event():
    init_db(app)
