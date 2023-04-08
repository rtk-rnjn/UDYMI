from __future__ import annotations

from typing import Any, Callable, Generic, Optional, TypeVar
from lru import LRU  # type: ignore

KT = TypeVar("KT", bound=Any)
VT = TypeVar("VT", bound=Any)


class Cache(dict, Generic[KT, VT]):
    def __init__(
        self,
        cache_size: Optional[int] = None,
        *,
        callback: Optional[Callable[[KT, VT], Any]] = None,
    ) -> None:
        self.cache_size: int = 512 if cache_size is None else cache_size
        self.__internal_cache: "LRU" = LRU(
            self.cache_size, callback=callback or (lambda a, b: ...)
        )

        self.items: Callable[[], List[Tuple[int, Any]]] = self.__internal_cache.items  # type: ignore
        self.peek_first_item: Callable[[], Optional[Tuple[int, Any]]] = self.__internal_cache.peek_first_item  # type: ignore
        self.peek_last_item: Callable[[], Optional[Tuple[int, Any]]] = self.__internal_cache.peek_last_item  # type: ignore
        self.get_size: Callable[[], int] = self.__internal_cache.get_size  # type: ignore
        self.set_size: Callable[[int], None] = self.__internal_cache.set_size  # type: ignore
        self.has_key: Callable[[object], bool] = self.__internal_cache.has_key  # type: ignore
        self.update: Callable[..., None] = self.__internal_cache.update  # type: ignore
        self.values: Callable[[], List[Any]] = self.__internal_cache.values  # type: ignore
        self.keys: Callable[[], List[Any]] = self.__internal_cache.keys  # type: ignore
        self.get: Callable[[object, ...], Any] = self.__internal_cache.get  # type: ignore
        self.pop: Callable[[object, ...], Any] = self.__internal_cache.pop  # type: ignore

    def __repr__(self) -> str:
        return repr(self.__internal_cache)

    def __len__(self) -> int:
        return len(self.__internal_cache)

    def __getitem__(self, __k: KT) -> VT:
        return self.__internal_cache[__k]

    def __delitem__(self, __v: KT) -> None:
        del self.__internal_cache[__v]

    def __contains__(self, __o: object) -> bool:
        return self.has_key(__o)

    def __setitem__(self, __k: KT, __v: VT) -> None:
        self.__internal_cache[__k] = __v
