from typing import cast
from decouple import config


def _str_config(searching_path: str, *args, **kwargs) -> str:
    """Convert to string"""
    obj = config(searching_path, *args, **kwargs)

    return cast(str, obj)


class Connection:
    DATABASE_URL = _str_config("DATABASE_URL")
