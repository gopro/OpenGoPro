"""Async generators to process asynchronous data flows."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from inspect import iscoroutinefunction
from typing import Any, Callable, Coroutine, Final, Generic, TypeAlias, TypeVar
from uuid import UUID, uuid1

T = TypeVar("T")
C = TypeVar("C", bound="Flow")


SyncAction: TypeAlias = Callable[[T], None]
AsyncAction: TypeAlias = Callable[[T], Coroutine[Any, Any, None]]
SyncFilter: TypeAlias = Callable[[T], bool]
AsyncFilter: TypeAlias = Callable[[T], Coroutine[Any, Any, bool]]


# pylint: disable=redefined-builtin

logger = logging.getLogger(__name__)


@dataclass
class FlowValue(Generic[T]):
    """Base class for value returned from flow "generator"""

    value: T


@dataclass
class Continue(FlowValue[T]):
    """A flow value from a successful read that indicates reads can continue"""


@dataclass
class Complete(FlowValue[T]):
    """A flow value from a read that indicates the read is complete either via success or error"""


class FlowManager(Generic[T]):
    """Flow manager to manage sending values from one data stream to one or more flows

    Args:
        capacity (int): cache size. Defaults to 1000.
        debug_id (str): Identifier for debug logging. Defaults to "".
    """

    def __init__(self, capacity: int = 1000, debug_id: str = "") -> None:
        self._debug_id = debug_id
        self._capacity = capacity
        # TODO do these need concurrency protection? yes.
        self._cache: list[T] = []
        self._q_dict: dict[UUID, asyncio.Queue[T]] = {}
        self._current: T | None = None
        # TODO handle cleanup

    def add_flow(self, uuid: UUID, replay: int) -> None:
        """Add a flow to receive collected values

        Args:
            uuid (UUID): flow identifier
            replay (int): how many values to replay from cache
        """
        if uuid not in self._q_dict:
            self._q_dict[uuid] = asyncio.Queue()
            if replay == Flow.REPLAY_ALL:
                replay = len(self._cache)
            head = max(len(self._cache) - replay, 0)
            for value in self._cache[head:]:
                self._q_dict[uuid].put_nowait(value)

    def remove_flow(self, uuid: UUID) -> None:
        """Remove a flow from receiving collected values

        Args:
            uuid (UUID): flow identifier
        """
        if uuid in self._q_dict:
            del self._q_dict[uuid]

    async def get_value(self, uuid: UUID) -> T:
        """Get the next value per-flow

        Args:
            uuid (UUID):: flow identifier to access value for

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
        self._current = value
        self._cache.append(value)
        if len(self._cache) > self._capacity:
            self._cache.pop(0)
        for uuid, q in self._q_dict.items():
            logger.trace(f"Flow manager {self._debug_id} emitting {value} to flow {uuid}")  # type: ignore
            await q.put(value)


# https://gist.github.com/jspahrsummers/32a8096667cf9f17d5e8fddeb081b202


class Flow(Generic[T]):
    """The asynchronous data flow

    Attributes:
        REPLAY_ALL (Final[int]): Special integer value to indicate all values should be replayed

    Args:
        manager (FlowManager[T]): manager to send data to the flow
        debug_id (str | None): Identifier to log for debugging. Defaults to None (will use generated UUID).
    """

    REPLAY_ALL: Final[int] = -1

    def __init__(self, manager: FlowManager[T], debug_id: str | None = None) -> None:
        self._count = 0
        self._debug_id = debug_id or ""
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
        return self._manager._current

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
        self._take_count = self._count + num
        return self

    # TODO should this be moved to add_flow in the manager?
    def on_subscribe(
        self: C,
        action: Callable[[], None] | Callable[[], Coroutine[Any, Any, None]],
    ) -> C:
        """Register to receive a callback when the a terminal operator starts collecting

        Args:
            action (Callable[[], None] | Callable[[], Coroutine[Any, Any, None]]): Callback

        Returns:
            C: modified flow
        """
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

    async def first(self, filter: SyncFilter, replay: int = 1) -> T:
        """Terminal receiver to collect only the first received value that matches a given filter

        Args:
            filter (SyncFilter): Filter to apply
            replay (int): how many values to replay from cache. Defaults to 1.

        Raises:
            NotImplementedError: TODO Need to handle what happens if flow ends before filter is triggered

        Returns:
            T: first value matching filter
        """
        uuid = uuid1()
        self._manager.add_flow(uuid, replay)
        while not self._should_close:
            match await self._get_next(uuid):
                case Continue(value):
                    if filter(value):
                        self._manager.remove_flow(uuid)
                        return value
                case Complete(value):
                    self._manager.remove_flow(uuid)
                    return value
        raise NotImplementedError

    async def single(self, replay: int = 1) -> T:
        """Terminal receiver to collect the first received value.

        Args:
            replay (int): how many values to replay from cache. Defaults to 1.

        Returns:
            T: First received value
        """
        uuid = uuid1()
        self._manager.add_flow(uuid, replay)
        flow_value = await self._get_next(uuid)
        assert flow_value is not None
        self._manager.remove_flow(uuid)
        return flow_value.value

    async def collect(
        self,
        action: SyncAction[T] | AsyncAction[T] | None = None,
        replay: int = 1,
    ) -> T:
        """Terminal receiver to indefinitely collect received values

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            action (SyncAction[T] | AsyncAction[T] | None): Action to call on each received value
            replay (int): how many values to replay from cache. Defaults to 1.

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: last received value
        """
        uuid = uuid1()
        self._manager.add_flow(uuid, replay)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            # TODO do we want / need should_close. It's not currently being handled
            while not self._should_close:
                match await self._get_next(uuid):
                    case Continue(value):
                        return_value = value
                        if action:
                            self._mux_action(action, value, tg)
                    case Complete(value):
                        break
        self._manager.remove_flow(uuid)
        if return_value is not None:
            return return_value
        raise RuntimeError("Failed to collect any values")

    async def collect_until(
        self,
        filter: SyncFilter[T],
        action: SyncAction[T] | AsyncAction[T],
        replay: int = 1,
    ) -> T:
        """Terminal receiver to collected received values until a filter is matched

        Note! If the action is synchronous, collecting will block on it
        Note! This will not return until all actions have completed

        Args:
            filter (SyncFilter[T]): Filter to apply
            action (SyncAction[T] | AsyncAction[T]): Action called on each received value
            replay (int): how many values to replay from cache. Defaults to 1.

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: Last value that was received when the filter matched
        """
        uuid = uuid1()
        self._manager.add_flow(uuid, replay)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            if self.current and filter(self.current):
                return_value = self.current
            else:
                while not self._should_close:
                    match await self._get_next(uuid):
                        case Continue(value):
                            return_value = value
                            assert return_value is not None
                            if filter(value):
                                break
                            self._mux_action(action, return_value, tg)
                        case Complete(value):
                            return_value = value
                            break
        self._manager.remove_flow(uuid)
        if return_value is not None:
            return return_value
        raise RuntimeError("Failed to collect any values")

    async def collect_while(
        self,
        action: SyncFilter[T] | AsyncFilter[T],
        replay: int = 1,
    ) -> T:
        """Terminal receiver to collect received value while a filter is matched

        Note that this will block / await until the filter action is complete.

        Args:
            action (SyncFilter[T] | AsyncFilter[T]): Action / filter that is called one ach received value.
                It also functions as the filter and should thus return whether or not the filter matches.
            replay (int): how many values to replay from cache. Defaults to 1.

        Raises:
            RuntimeError: Failed to collect any values

        Returns:
            T: Last value that was received while the filter matched.
        """
        uuid = uuid1()
        self._manager.add_flow(uuid, replay)
        if self.current and not self._mux_filter_blocking(action, self.current):
            self._manager.remove_flow(uuid)
            return self.current
        while not self._should_close:
            return_value: T | None = None
            match await self._get_next(uuid):
                case Continue(value):
                    return_value = value
                    if not await self._mux_filter_blocking(action, value):
                        self._manager.remove_flow(uuid)
                        assert return_value is not None
                        return return_value
                case Complete(value):
                    self._manager.remove_flow(uuid)
                    if return_value is None:
                        raise RuntimeError("Failed to collect any values")
                    return return_value
        self._manager.remove_flow(uuid)
        if self.current:
            return self.current
        raise RuntimeError("Failed to collect any values")

    async def _get_next(self, uuid: UUID) -> FlowValue[T]:
        """Get the next flow value from the manager

        Args:
            uuid (UUID): Flow identifier

        Raises:
            RuntimeError: Flow ended without receiving any values

        Returns:
            FlowValue[T]: Latest flow value
        """
        if self._count == 0:
            for action in self._on_subscribe_actions:
                if iscoroutinefunction(action):
                    await action()
                action()
        if self._take_count and self._count == self._take_count:
            if self.current is None:
                raise RuntimeError("Failed to collect any values")
            return Complete(self.current)
        if self._drop_count:
            for _ in range(self._drop_count):
                await self._manager.get_value(uuid)
            self._drop_count = 0
        value = await self._manager.get_value(uuid)
        for action in self._per_value_actions:  # type: ignore
            action(value)  # type: ignore
        self._count += 1
        if self._count == 1:
            for action in self._on_start_actions:  # type: ignore
                self._mux_action(action, value)  # type: ignore
        return Continue(value)
