from typing import cast, Optional, Callable, NewType, TypeVar, Union, overload
from decouple import config

T = TypeVar("T")
V = TypeVar("V")
Sentinel = NewType("Sentinel", object)
_MISSING = cast(Sentinel, object())


def _str_config(searching_path: str, *args, **kwargs) -> str:
    """Convert to string"""
    obj = config(searching_path, *args, **kwargs)

    return cast(str, obj)


def _int_config(searching_path: int, *args, **kwargs) -> int:
    obj = config(searching_path, *args, **kwargs)

    return int(obj)


@overload
def _get_config(search_path: str, cast: None = None, default: Union[V, Sentinel] = _MISSING) -> Union[str, V]:
    ...


@overload
def _get_config(search_path: str, cast: Callable[[str], T], default: Union[V, Sentinel] = _MISSING) -> Union[T, V]:
    ...


def _get_config(
        search_path: str,
        cast: Optional[Callable[[str], object]] = None,
        default: object = _MISSING,
) -> object:
    """Wrapper around decouple.config that can handle typing better."""
    if cast is None:
        cast = lambda x: x

    if default is not _MISSING:
        obj = config(search_path, cast=cast, default=default)
    else:
        obj = config(search_path, cast=cast)

    return obj


class Connection:
    DATABASE_URL = _str_config("DATABASE_URL")


class Server:
    SECRET_KEY = _str_config("SECRET_KEY")
    ALGORITHM = _str_config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = _int_config("ACCESS_TOKEN_EXPIRE_MINUTES")


class Logging:
    """Logging related configuration"""

    DEBUG = _get_config("DEBUG", cast=bool, default=False)
    LOG_FILE = _get_config("LOG_FILE", default=None)
    MAX_FILE_SIZE = _get_config("LOG_FILE_MAX_SIZE", cast=int, default=-1)
