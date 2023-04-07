from __future__ import annotations
import os

from typing import Any, List, Optional, Union

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def _bool_converter(value: str) -> Optional[bool]:
    """Convert a string to a boolean."""

    if value.lower() in {
        "true",
        "yes",
        "y",
        "1",
        "on",
        "enable",
        "enabled",
        "t",
    }:
        return True
    
    if value.lower() in {
        "false",
        "no",
        "n",
        "0",
        "off",
        "disable",
        "disabled",
        "f",
    }:
        return False
    
    return None

def _parse_env(
    *, key: Optional[str], default: Any = None
) -> Union[str, int, float, bool, List[Any]]:
    """Parse an environment variable into a Python type."""

    value = os.environ.get(str(key), default)
    if value is None:
        raise ValueError(f"{key} is not set")
    if "|" in value:
        return [_parse_env(key=None, default=key) for key in value.split("|")]
    if value.isdigit():
        return int(value)
    if value.replace(".", "", 1).isdigit():
        return float(value)
    return value.lower() == "true" if value.lower() in ("true", "false") else value


class Config:
    """A class to hold all the environment variables."""

    __class__ = None  # type: ignore

    def __init__(self):
        for key, value in os.environ.items():
            setattr(self, str(key), _parse_env(key=key, default=value))

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            return __name


CONFIG = Config()
