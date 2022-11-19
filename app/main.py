from fastapi import FastAPI

from app.routers import users
from app.routers import shop
from app.db.database import init_db

app = FastAPI(title="Using Tortoise")

app.include_router(users.router)
app.include_router(shop.router)


@app.on_event("startup")  # before starting creating database
async def startup_event():
    init_db(app)
