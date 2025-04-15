from __future__ import annotations
from types import TracebackType
from uuid import uuid1
from typing import AsyncIterator, TypeVar, AsyncGenerator, Any, Coroutine, Callable

import asyncio

T = TypeVar("T")


class FlowManager[T]:
    def __init__(self) -> None:
        self._replay: T | None = None
        self._q_dict: dict[Flow[T], asyncio.Queue[T]] = {}
        # TODO handle cleanup

    def add_flow(self, flow: Flow[T]) -> None:
        if flow not in self._q_dict:
            self._q_dict[flow] = asyncio.Queue()
            # Replay the current value if we have it
            if self._replay:
                self._q_dict[flow].put_nowait(self._replay)

    def remove_flow(self, flow: Flow[T]) -> None:
        if flow in self._q_dict:
            del self._q_dict[flow]

    async def get_value(self, flow: Flow[T]) -> T:
        temp = await self._q_dict[flow].get()
        return temp
        # TODO catch exception

    async def emit(self, value: T) -> None:
        self._replay = value
        for q in self._q_dict.values():
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202


class Flow[T](AsyncGenerator[T, Any]):
    def __init__(self, manager: FlowManager[T]) -> None:
        self._id = uuid1().int
        self._current: T
        self._manager = manager
        self._manager.add_flow(self)
        # TODO handle cleanup

    def __hash__(self) -> int:
        return self._id

    @property
    def current(self) -> T:
        return self._current

    async def drop(self, num: int) -> Flow[T]:
        # TODO do we want current to reflect the dropped values?
        for _ in range(num):
            await anext(self)
        return self

    async def first(self, filter: Callable[[T], bool]) -> T:
        while (value := await anext(self)) is not None:
            if filter(value):
                return value
        raise NotImplementedError

    # Async Generator Methods

    async def asend(self, value: Any) -> Coroutine[Any, Any, T]:
        raise NotADirectoryError

    async def aclose(self) -> Coroutine[Any, Any, None]:
        raise NotImplementedError

    async def athrow(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ):
        raise NotImplementedError

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T | None:
        # TODO how do we handle None? I guess we don't.
        while (value := await self._manager.get_value(self)) is not None:
            self._current = value
            return value
        # TODO handle closing
