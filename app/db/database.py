from fastapi import FastAPI

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.utils.constants import Connection

DATABASE_URL = f'postgres://{Connection.DATABASE_URL}'


def init_db(app: FastAPI) -> None:
    Tortoise.init_models(["app.models"], "models")
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )
