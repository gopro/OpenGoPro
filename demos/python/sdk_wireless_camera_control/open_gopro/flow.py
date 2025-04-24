"""Async generators to process asynchronous data flows."""

from __future__ import annotations

import asyncio
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
from uuid import UUID, uuid1

T = TypeVar("T")
C = TypeVar("C", bound="Flow")


SyncAction: TypeAlias = Callable[[T], None]
AsyncAction: TypeAlias = Callable[[T], Coroutine[Any, Any, None]]
SyncFilter: TypeAlias = Callable[[T], bool]
AsyncFilter: TypeAlias = Callable[[T], Coroutine[Any, Any, bool]]


# pylint: disable=redefined-builtin

logger = logging.getLogger(__name__)


class FlowManager(Generic[T]):
    """Flow manager to manage sending values from one data stream to one or more flows"""

    def __init__(self, debug_id: str = "") -> None:
        self._debug_id = debug_id
        self._replay: T | None = None
        self._q_dict: dict[UUID, asyncio.Queue[T]] = {}
        # TODO handle cleanup

    def add_flow(self, uuid: UUID) -> None:
        """Add a flow to receive collected values

        Args:
            flow (Flow[T]): Flow to add
        """
        if uuid not in self._q_dict:
            self._q_dict[uuid] = asyncio.Queue()
            # Replay the current value if we have it
            if self._replay:
                self._q_dict[uuid].put_nowait(self._replay)

    def remove_flow(self, uuid: UUID) -> None:
        """Remove a flow from receiving collected values

        Args:
            flow (Flow[T]): Flow to remove
        """
        if uuid in self._q_dict:
            del self._q_dict[uuid]

    async def get_value(self, uuid: UUID) -> T:
        """Get the next value per-flow

        Args:
            flow (Flow[T]): flow to access value for

        Raises:
            RuntimeError: Flow has not yet been added

        Returns:
            T: Received value
        """
        if uuid not in self._q_dict:
            logger.error("Attempted to get value from a non-registered flow.")
            raise RuntimeError("Flow has not been added!")
            # TODO exception is not propagating
        value = await self._q_dict[uuid].get()
        return value

    async def emit(self, value: T) -> None:
        """Receive a value and queue it for per-flow retrieval

        Args:
            value (T): Value to queue
        """
        self._replay = value
        for uuid, q in self._q_dict.items():
            logger.trace(f"Flow manager {self._debug_id} emitting {value} to flow {uuid}")  # type: ignore
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202


class Flow(Generic[T]):
    """The asynchronous data flow

    Args:
        manager (FlowManager[T]): manager to send data to the flow
        debug_id (str | None): Identifier to log for debugging. Defaults to None (will use generated UUID).
    """

    def __init__(self, manager: FlowManager[T], debug_id: str | None = None) -> None:
        self._count = 0
        self._debug_id = debug_id or ""
        self._current: T | None = None
        self._manager = manager
        self._on_start_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._on_subscribe_actions: list[Callable[[], None] | Callable[[], Coroutine[Any, Any, None]]] = []
        self._per_value_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._take_count: int | None = None
        self._drop_count: int = 0
        # TODO handle cleanup
        # TODO there is certainly a better way to do this using the unimplemented dunders below
        self._should_close = False

    def _mux_action(
        self,
        action: SyncAction[T] | AsyncAction[T],
        value: T,
        tg: asyncio.TaskGroup | None = None,
    ) -> None:
        """Execute an action that is either synchronous or asynchronous

        If tg is passed, the async action will be added to the task group. Otherwise an anonymous async task will be
        created. In both cases, this function will return without awaiting the created task.

        Note! If action is synchronous, this will block until the action returns.

        Args:
            action (SyncAction[T] | AsyncAction[T]): action to execute
            value (T): value to pass to action
            tg (asyncio.TaskGroup | None, optional): Task group to add async action. Defaults to None (don't add to any
                task group).
        """
        if iscoroutinefunction(action):
            if tg:
                tg.create_task(action(value))
            else:
                asyncio.create_task(action(value))
        else:
            action(value)

    async def _mux_filter_blocking(self, filter: SyncFilter | AsyncFilter, value: T) -> bool:
        """Execute a filter that is either synchronous or asynchronous

        Note! This will await / block until the action completes.

        Args:
            filter (SyncFilter | AsyncFilter): Filter to execute
            value (T): value to analyze with filter

        Returns:
            bool: _description_
        """
        if iscoroutinefunction(filter):
            return await filter(value)
        return filter(value)  # type: ignore

    @property
    def current(self) -> T | None:
        """Get the most recently collected value of the flow.

        Note that this does not indicate the value in real-time. It is the most recent value that was collected
        from a receiver.

        Returns:
            T | None: Most recently collected value, or None if no values were collected yet
        """
        return self._current

    # TODO we need to add a pipeline for this to be used at the same time as take
    def drop(self: C, num: int) -> C:
        """Collect the first num values and ignore them

        Args:
            num (int): number of values to ignore

        Returns:
            C: modified flow
        """
        self._drop_count = num
        return self

    def take(self: C, num: int) -> C:
        """Configure the flow collection to stop after receiving a certain amount of values

        Args:
            num (int): number of values to take

        Returns:
            C: modified flow
        """
        self._take_count = self._count + num + 1
        return self

    def on_subscribe(self: C, action: Callable[[], None] | Callable[[], Coroutine[Any, Any, None]]) -> C:
        self._on_subscribe_actions.append(action)
        return self

    def on_start(self: C, action: SyncAction[T] | AsyncAction[T]) -> C:
        """Register a callback action to be called when the flow starts collecting

        Args:
            action (SyncAction[T] | AsyncAction[T]): Callback action

        Returns:
            C: modified flow
        """
        self._on_start_actions.append(action)
        return self

    # TODO add on_subscribed

    async def first(self, filter: SyncFilter) -> T:
        """Terminal receiver to collect only the first received value that matches a given filter

        Args:
            filter (SyncFilter): Filter to apply

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered

        Returns:
            T: first value matching filter
        """
        uuid = uuid1()
        self._manager.add_flow(uuid)
        while (value := await self._get_next(uuid)) is not None:
            if filter(value):
                self._manager.remove_flow(uuid)
                return value
        raise NotImplementedError

    async def single(self) -> T:
        """Terminal receiver to collect the first received value.

        Returns:
            T: First received value
        """
        uuid = uuid1()
        self._manager.add_flow(uuid)
        value = await self._get_next(uuid)
        assert value is not None
        self._manager.remove_flow(uuid)
        return value

    async def collect(self, action: SyncAction[T] | AsyncAction[T] | None = None) -> T:
        """Terminal receiver to indefinitely collect received values

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            action (SyncAction[T] | AsyncAction[T] | None): Action to call on each received value

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: last received value
        """
        uuid = uuid1()
        self._manager.add_flow(uuid)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            try:
                # TODO do we want / need should_close. It's not currently being handled
                while not self._should_close:
                    return_value = await self._get_next(uuid)
                    if action:
                        self._mux_action(action, return_value, tg)
                return_value = self.current
            except StopAsyncIteration:
                pass
        self._manager.remove_flow(uuid)
        if return_value is not None:
            return return_value
        raise RuntimeError("Failed to collect any values")

    async def collect_until(self, filter: SyncFilter[T], action: SyncAction[T] | AsyncAction[T]) -> T:
        """Terminal receiver to collected received values until a filter is matched

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            filter (SyncFilter[T]): Filter to apply
            action (SyncAction[T] | AsyncAction[T]): Action called on each received value

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: Last value that was received when the filter matched
        """
        uuid = uuid1()
        self._manager.add_flow(uuid)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            try:
                if self.current and filter(self.current):
                    return_value = self.current
                else:
                    while not self._should_close:
                        if filter(return_value := await self._get_next(uuid)):
                            break
                        self._mux_action(action, return_value, tg)
            except StopAsyncIteration:
                return_value = self.current
        self._manager.remove_flow(uuid)
        if return_value is not None:
            return return_value
        raise RuntimeError("Failed to collect any values")

    async def collect_while(self, action: SyncFilter[T] | AsyncFilter[T]) -> T:
        """Terminal receiver to collect received value while a filter is matched

        Note that this will block / await until the filter action is complete.

        Args:
            action (SyncFilter[T] | AsyncFilter[T] ): Action / filter that is called one ach received value.
                It also functions as the filter and should thus return whether or not the filter matches.

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: Last value that was received while the filter matched.
        """
        try:
            uuid = uuid1()
            self._manager.add_flow(uuid)
            if self.current and not self._mux_filter_blocking(action, self.current):
                self._manager.remove_flow(uuid)
                return self.current
            while not self._should_close:
                if not await self._mux_filter_blocking(action, value := await self._get_next(uuid)):
                    self._manager.remove_flow(uuid)
                    return value
            self._manager.remove_flow(uuid)
            if self.current:
                return self.current
            raise RuntimeError("Failed to collect any values")
        except StopAsyncIteration as exc:
            self._manager.remove_flow(uuid)
            if self.current:
                return self.current
            raise RuntimeError("Failed to collect any values") from exc

    async def _get_next(self, uuid: UUID) -> T:
        if self._count == 0:
            for action in self._on_subscribe_actions:
                if iscoroutinefunction(action):
                    await action()
                action()
        if self._drop_count:
            for _ in range(self._drop_count):
                await self._manager.get_value(uuid)
            self._drop_count = 0
        value = await self._manager.get_value(uuid)
        self._current = value
        for action in self._per_value_actions:
            action(value)
        self._count += 1
        if self._count == 1:
            for action in self._on_start_actions:
                self._mux_action(action, value)
        if self._take_count and self._count == self._take_count:
            raise StopAsyncIteration
        return value
