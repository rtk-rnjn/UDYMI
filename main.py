from __future__ import annotations

from src import app
import asyncio
import os

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    app.run(debug=True)
