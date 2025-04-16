from __future__ import annotations

import asyncio
from collections import defaultdict
from types import TracebackType
from typing import Any, AsyncGenerator, AsyncIterator, Callable, Coroutine, TypeVar
from uuid import uuid1

T = TypeVar("T")


class FlowManager[T]:
    def __init__(self) -> None:
        self._replay: T | None = None
        self._q_dict: dict[Flow, asyncio.Queue[T]] = {}
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
        # TODO remove temp once done debugging
        temp = await self._q_dict[flow].get()
        return temp
        # TODO catch exception

    async def emit(self, value: T) -> None:
        self._replay = value
        for flow, q in self._q_dict.items():
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202


class Flow[T](AsyncGenerator[T, Any]):
    def __init__(self, manager: FlowManager[T], is_mapped: bool = False) -> None:
        self._count = 0
        self._id = uuid1().int
        self._current: T | None = None
        self._manager = manager
        self._on_start_actions: list[Callable[[T], None]] = []
        self._per_value_actions: list[Callable[[T], None]] = []
        if not is_mapped:
            self._manager.add_flow(self)
        # TODO handle cleanup

        # TODO there is certainly a better way to do this using the unimplemented dunders below
        self._should_close = False

    def __hash__(self) -> int:
        return self._id

    @property
    def current(self) -> T | None:
        return self._current

    async def drop(self, num: int) -> Flow[T]:
        # TODO do we want current to reflect the dropped values?
        for _ in range(num):
            await anext(self)
        return self

    def on_start(self, action: Callable[[T], None]) -> Flow[T]:
        self._on_start_actions.append(action)
        return self

    async def first(self, filter: Callable[[T], bool]) -> T:
        if self.current and filter(self.current):
            return self.current
        while (value := await anext(self)) is not None:
            if filter(value):
                return value
        raise NotImplementedError

    async def single(self) -> T:
        value = await anext(self)
        assert value is not None
        return value

    async def collect(
        self,
        action: Callable[[T], Coroutine[Any, Any, None]] | None,
    ) -> T:
        while not self._should_close:
            value = await self.single()
            if action:
                await action(value)
        raise NotImplementedError

    async def collect_until(
        self,
        filter: Callable[[T], bool],
        action: Callable[[T], Coroutine[Any, Any, None]],
    ) -> T:
        if self.current and filter(self.current):
            return self.current
        while not self._should_close:
            if filter(value := await self.single()):
                return value
            await action(value)
        raise NotImplementedError

    async def collect_while(
        self,
        action: Callable[[T], Coroutine[Any, Any, bool]],
    ) -> T:
        if self.current and not await action(self.current):
            return self.current
        while not self._should_close:
            if not await action(value := await self.single()):
                return value
        raise NotImplementedError

    # TODO this needs more design
    # def map[O](self, mapper: Callable[[T], O]) -> Flow[O]:
    #     new_flow = Flow(self._manager, is_mapped=True)
    #     self._manager.add_mapped_flow(self, mapper, new_flow)  # type: ignore
    #     return new_flow  # type: ignore

    # Async Generator Methods

    async def asend(self, value: Any) -> T:
        raise NotImplementedError

    async def aclose(self) -> None:
        raise NotImplementedError

    # TODO figure out the signature here
    async def athrow(self, base_exception: BaseException, traceback_type: TracebackType | None) -> Any:  # type: ignore
        raise NotImplementedError

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        while (value := await self._manager.get_value(self)) is not None:
            self._current = value
            for action in self._per_value_actions:
                action(value)
            self._count += 1
            if self._count == 1:
                for action in self._on_start_actions:
                    action(value)
            return value
        raise StopAsyncIteration
