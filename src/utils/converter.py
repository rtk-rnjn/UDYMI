from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, Optional


class ToAsync:
    """Converts a blocking function to an async function"""

    def __init__(self, *, executor: Optional[ThreadPoolExecutor] = None) -> None:
        self.executor = executor or ThreadPoolExecutor()

    def __call__(self, blocking) -> Callable[..., Any]:
        @wraps(blocking)
        async def wrapper(*args, **kwargs) -> Any:
            return await asyncio.get_event_loop().run_in_executor(
                self.executor, partial(blocking, *args, **kwargs)
            )

        return wrapper


class ToSync:
    """Converts an async function to a blocking function"""

    def __init__(self, *, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.loop = loop or asyncio.get_event_loop()

    def __call__(self, async_func) -> Callable[..., Any]:
        @wraps(async_func)
        def wrapper(*args, **kwargs) -> Any:
            return self.loop.run_until_complete(async_func(*args, **kwargs))

        return wrapper
