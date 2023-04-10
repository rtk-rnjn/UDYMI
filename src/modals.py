from __future__ import annotations

from flask_login import UserMixin
from typing import Any

from src import login_manager, app


class _User:
    username: str
    email: str

    def __init__(self, **kwargs: Any) -> None:
        self.id = str(kwargs["_id"])

        for key, val in kwargs.items():
            setattr(self, key, val)


class User(_User, UserMixin):
    id: str

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)


@login_manager.user_loader
def load_user(user_id: Any) -> User:
    return User(_id=user_id)  # type: ignore
