from fastapi import FastAPI

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.utils.constants import Connection

DATABASE_URL = f'postgres://{Connection.DATABASE_URL}'


def init_db(app: FastAPI) -> None:
    Tortoise.init_models(["app.models"], "models")
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )


# Config For migration [aerich]
TORTOISE_ORM = {
    "connections": {"default": f'postgres://{Connection.DATABASE_URL}'},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
