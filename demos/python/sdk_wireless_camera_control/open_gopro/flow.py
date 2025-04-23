"""Async generators to process asynchronous data flows."""

from __future__ import annotations

import asyncio
from doctest import debug
import logging
from inspect import iscoroutinefunction
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Callable,
    Coroutine,
    Generic,
    TypeAlias,
    TypeVar,
)
from uuid import uuid1

T = TypeVar("T")

# pylint: disable=redefined-builtin

logger = logging.getLogger(__name__)


class FlowManager(Generic[T]):
    """Flow manager to manage sending values from one data stream to one or more flows"""

    def __init__(self, debug_id: str = "") -> None:
        self._debug_id = debug_id
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
        if flow not in self._q_dict:
            logger.error("Attempted to get value from a non-registered flow.")
            raise RuntimeError("Flow has not been added!")
            # TODO exception is not propagating
        return await self._q_dict[flow].get()

    async def emit(self, value: T) -> None:
        """Receive a value and queue it for per-flow retrieval

        Args:
            value (T): Value to queue
        """
        self._replay = value
        for flow, q in self._q_dict.items():
            logger.trace(f"Flow manager {self._debug_id} emitting {value} to flow {flow._debug_id}")  # type: ignore
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202

C = TypeVar("C", bound="Flow")


SyncAction: TypeAlias = Callable[[T], None]
AsyncAction: TypeAlias = Callable[[T], Coroutine[Any, Any, None]]
SyncFilter: TypeAlias = Callable[[T], bool]
AsyncFilter: TypeAlias = Callable[[T], Coroutine[Any, Any, bool]]


class Flow(AsyncGenerator[T, Any], Generic[T]):
    """The asynchronous data flow

    Args:
        manager (FlowManager[T]): manager to send data to the flow
    """

    def __init__(self, manager: FlowManager[T], debug_id: str | None = None) -> None:
        self._count = 0
        self._id = uuid1().int
        self._debug_id = debug_id or str(self._id)
        self._current: T | None = None
        self._manager = manager
        self._on_start_actions: list[SyncAction | AsyncAction] = []
        self._per_value_actions: list[SyncAction | AsyncAction] = []
        self._manager.add_flow(self)
        self._take_count: int | None = None
        # TODO handle cleanup
        # TODO there is certainly a better way to do this using the unimplemented dunders below
        self._should_close = False

    def __hash__(self) -> int:
        return self._id

    def _mux_action(self, action: SyncAction | AsyncAction | None, value: T, tg: asyncio.TaskGroup) -> None:
        if action:
            if iscoroutinefunction(action):
                tg.create_task(action(value))
            else:
                action(value)

    async def _mux_filter_blocking(self, action: SyncFilter | AsyncFilter, value: T) -> bool:
        if iscoroutinefunction(action):
            return await action(value)
        else:
            return action(value)

    @property
    def current(self) -> T | None:
        """Get the most recently collected value of the flow.

        Note that this does not indicate the value in real-time. It is the most recent value that was collected
        from a receiver.

        Returns:
            T | None: Most recently collected value, or None if no values were collected yet
        """
        return self._current

    # TODO should this be treated the same as take?
    async def drop(self: C, num: int) -> C:
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

    def take(self: C, num: int) -> C:
        self._take_count = self._count + num + 1
        return self

    def on_start(self: C, action: SyncAction | AsyncAction) -> C:
        """Register a callback action to be called when the flow starts collecting

        Args:
            action (SyncAction | AsyncAction): Callback action

        Returns:
            Flow[T]: modified flow
        """
        self._on_start_actions.append(action)
        return self

    async def first(self, filter: SyncFilter) -> T:
        """Terminal receiver to collect only the first received value that matches a given filter

        Args:
            filter (SyncFilter): Filter to apply

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

    async def collect(self, action: SyncAction | AsyncAction | None) -> T | None:
        """Terminal receiver to indefinitely collect received values

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            action (SyncAction | AsyncAction | None): Action to call on each received value
        """
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            try:
                # TODO do we want / need should_close. It's not currently being handled
                while not self._should_close:
                    return_value = await self.single()
                    self._mux_action(action, return_value, tg)
            except StopAsyncIteration:
                return_value = self.current
        return return_value

    async def collect_until(self, filter: SyncFilter, action: SyncAction | AsyncAction) -> T | None:
        """Terminal receiver to collected received values until a filter is matched

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            filter (SyncFilter): Filter to apply
            action (SyncAction | AsyncAction): Action called on each received value

        Returns:
            T: Last value that was received when the filter matched
        """
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            try:
                if self.current and filter(self.current):
                    return_value = self.current
                else:
                    while not self._should_close:
                        if filter(return_value := await self.single()):
                            break
                        self._mux_action(action, return_value, tg)
            except StopAsyncIteration:
                return_value = self.current
        return return_value

    async def collect_while(self, action: SyncFilter | AsyncFilter) -> T | None:
        """Terminal receiver to collect received value while a filter is matched

        Note that this will block / await until the filter action is complete.

        Args:
            action (SyncFilter | AsyncFilter ): Action / filter that is called one ach received value.
                It also functions as the filter and should thus return whether or not the filter matches.

        Returns:
            T: Last value that was received while the filter matched.
        """
        try:
            if self.current and not self._mux_filter_blocking(action, self.current):
                return self.current
            else:
                while not self._should_close:
                    if not await self._mux_filter_blocking(action, value := await self.single()):
                        return value
        except StopAsyncIteration:
            return self.current

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
            if self._take_count and self._count == self._take_count:
                break
            return value
        raise StopAsyncIteration
