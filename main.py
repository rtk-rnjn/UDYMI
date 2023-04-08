from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask

from src import app
import asyncio
import os

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def return_app() -> Flask:
    return app


if __name__ == "__main__":
    app.run(load_dotenv=True)
else:
    return_app()
