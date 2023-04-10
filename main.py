from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

from src import app


if __name__ == "__main__":
    app.run(load_dotenv=True)
