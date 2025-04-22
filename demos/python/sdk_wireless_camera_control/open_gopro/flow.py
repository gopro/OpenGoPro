"""Async generators to process asynchronous data flows."""

from __future__ import annotations

import asyncio
import logging
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Callable,
    Coroutine,
    Generic,
    TypeVar,
)
from uuid import uuid1

T = TypeVar("T")

# pylint: disable=redefined-builtin

logger = logging.getLogger(__name__)


class FlowManager(Generic[T]):
    """Flow manager to manage sending values from one data stream to one or more flows"""

    def __init__(self) -> None:
        self._replay: T | None = None
        self._q_dict: dict[Flow, asyncio.Queue[T]] = {}
        # TODO handle cleanup

    def add_flow(self, flow: Flow[T]) -> None:
        """Add a flow to receive collected values

        Args:
            flow (Flow[T]): Flow to add
        """
        if flow not in self._q_dict:
            self._q_dict[flow] = asyncio.Queue()
            # Replay the current value if we have it
            if self._replay:
                self._q_dict[flow].put_nowait(self._replay)

    def remove_flow(self, flow: Flow[T]) -> None:
        """Remove a flow from receiving collected values

        Args:
            flow (Flow[T]): Flow to remove
        """
        if flow in self._q_dict:
            del self._q_dict[flow]

    async def get_value(self, flow: Flow[T]) -> T:
        """Get the next value per-flow

        Args:
            flow (Flow[T]): flow to access value for

        Raises:
            RuntimeError: Flow has not yet been added

        Returns:
            T: Received value
        """
        # TODO remove temp once done debugging
        if flow not in self._q_dict:
            logger.error("Attempted to get value from a non-registered flow.")
            raise RuntimeError("Flow has not been added!")
            # TODO exception is not propagating
        temp = await self._q_dict[flow].get()
        return temp

    async def emit(self, value: T) -> None:
        """Receive a value and queue it for per-flow retrieval

        Args:
            value (T): Value to queue
        """
        self._replay = value
        for q in self._q_dict.values():
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202


class Flow(AsyncGenerator[T, Any], Generic[T]):
    """The asynchronous data flow

    Args:
        manager (FlowManager[T]): manager to send data to the flow
    """

    def __init__(self, manager: FlowManager[T]) -> None:
        self._count = 0
        self._id = uuid1().int
        self._current: T | None = None
        self._manager = manager
        self._on_start_actions: list[Callable[[T], None]] = []
        self._per_value_actions: list[Callable[[T], None]] = []
        self._manager.add_flow(self)
        # TODO handle cleanup
        # TODO there is certainly a better way to do this using the unimplemented dunders below
        self._should_close = False

    def __hash__(self) -> int:
        return self._id

    @property
    def current(self) -> T | None:
        """Get the most recently collected value of the flow.

        Note that this does not indicate the value in real-time. It is the most recent value that was collected
        from a receiver.

        Returns:
            T | None: Most recently collected value, or None if no values were collected yet
        """
        return self._current

    async def drop(self, num: int) -> Flow[T]:
        """Collect the first num values and ignore them

        Args:
            num (int): number of values to ignore

        Returns:
            Flow[T]: modified flow
        """
        # TODO do we want current to reflect the dropped values? Probably not...
        for _ in range(num):
            await anext(self)
        return self

    def on_start(self, action: Callable[[T], None]) -> Flow[T]:
        """Register a callback action to be called when the flow starts collecting

        Args:
            action (Callable[[T], None]): Callback action

        Returns:
            Flow[T]: modified flow
        """
        self._on_start_actions.append(action)
        return self

    async def first(self, filter: Callable[[T], bool]) -> T:
        """Terminal receiver to collect only the first received value that matches a given filter

        Args:
            filter (Callable[[T], bool]): Filter to apply

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered

        Returns:
            T: first value matching filter
        """
        while (value := await anext(self)) is not None:
            if filter(value):
                return value
        raise NotImplementedError

    async def single(self) -> T:
        """Terminal receiver to collect the first received value.

        Returns:
            T: First received value
        """
        value = await anext(self)
        assert value is not None
        return value

    async def collect(
        self,
        action: Callable[[T], Coroutine[Any, Any, None]] | None,
    ) -> None:
        """Terminal receiver to indefinitely collect received values

        Args:
            action (Callable[[T], Coroutine[Any, Any, None]] | None): Action to call on each received value

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered
        """
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
        """Terminal receiver to collected received values until a filter is matched

        Args:
            filter (Callable[[T], bool]): Filter to apply
            action (Callable[[T], Coroutine[Any, Any, None]]): Action called on each received value

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered

        Returns:
            T: Last value that was received when the filter matched
        """
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
        """Terminal receiver to collect received value while a filter is matched

        Args:
            action (Callable[[T], Coroutine[Any, Any, bool]]): Action / filter that is called one ach received value.
                It also functions as the filter and should thus return whether or not the filter matches.

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered

        Returns:
            T: Last value that was received while the filter matched.
        """
        if self.current and not await action(self.current):
            return self.current
        while not self._should_close:
            if not await action(value := await self.single()):
                return value
        raise NotImplementedError

    # Async Generator Methods

    async def asend(self, value: Any) -> T:
        """TODO

        Args:
            value (Any): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            T: _description_
        """
        raise NotImplementedError

    async def aclose(self) -> None:
        """TODO

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    # TODO figure out the signature here
    async def athrow(  # type: ignore
        self,
        typ: type[BaseException],
        val: BaseException | object = None,
        tb: TracebackType | None = None,
    ) -> Any:
        """_summary_

        Args:
            typ (type[BaseException]): _description_
            val (BaseException | object): _description_. Defaults to None.
            tb (TracebackType | None): _description_. Defaults to None.

        Raises:
            NotImplementedError: _description_

        Returns:
            Any: _description_
        """
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
