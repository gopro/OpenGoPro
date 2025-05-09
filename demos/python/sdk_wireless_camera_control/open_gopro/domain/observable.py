"""Async generators to process asynchronous data flows."""

# pylint: disable=redefined-builtin

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from inspect import iscoroutinefunction
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    Final,
    Generic,
    NoReturn,
    Self,
    TypeAlias,
    TypeVar,
)
from uuid import UUID, uuid1

from asyncstdlib import anext, filter

O = TypeVar("O")
T = TypeVar("T")
C = TypeVar("C", bound="Observable")


SyncAction: TypeAlias = Callable[[T], None]
AsyncAction: TypeAlias = Callable[[T], Coroutine[Any, Any, None]]
SyncFilter: TypeAlias = Callable[[T], bool]
AsyncFilter: TypeAlias = Callable[[T], Coroutine[Any, Any, bool]]

logger = logging.getLogger(__name__)

T_I = TypeVar("T_I")


class Observer(AsyncGenerator[T, None]):
    """Async generator wrapper with added control methods"""

    def __init__(self, flow: Observable[T], uuid: UUID, replay: int, debug_id: str | None = None) -> None:
        self.flow = flow
        self.uuid = uuid
        self.replay = replay
        self._debug_id = debug_id or str(uuid)
        self.is_active = False

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> T:
        if not self.is_active:
            self.is_active = True
            await self.flow._add_collector(self.uuid, replay=self.replay)

        try:
            logger.trace(f"Observer {self._debug_id} waiting for next value")  # type: ignore
            value = await self.flow._get_next(self.uuid)
            logger.trace(f"Observer {self._debug_id} received value: {value}")  # type: ignore
            return value
        except Exception as e:
            logger.error(f"Error in observer {self._debug_id}: {e}")
            await self._cleanup()
            raise e

    async def first(self, predicate: SyncFilter) -> T:
        """Get the first value that matches the predicate

        Args:
            predicate (SyncFilter): Predicate to match

        Returns:
            T: First value that matches the predicate
        """
        return await anext(filter(predicate, self))

    async def _cleanup(self) -> None:
        """Clean up resources when generator is done"""
        if self.is_active:
            self.is_active = False
            await self.flow._remove_collector(self.uuid)

    async def aclose(self) -> None:
        """Properly close the generator and clean up resources"""
        await self._cleanup()

    async def athrow(self, typ: Any, val: Any = None, tb: Any = None) -> NoReturn:
        """Throw an exception into the generator"""
        if not self.is_active:
            raise StopAsyncIteration

        # Cleanup first
        await self._cleanup()
        # Then raise the exception
        if val is None:
            val = typ()
        if tb is not None:
            raise val.with_traceback(tb)
        raise val

    async def asend(self, value: None) -> T:
        """Send a value into the generator (required by protocol)"""
        if not self.is_active:
            raise StopAsyncIteration

        # We don't really use the sent value, so just advance to next item
        return await anext(self)


class Observable(Generic[T]):
    """The asynchronous data flow

    Attributes:
        REPLAY_ALL (Final[int]): Special integer value to indicate all values should be replayed
        FLOW_IDX (int): counter of flow instantiations used for debugging

    Args:
        capacity (int): Maximum values to store for replay. Defaults to 100.
        debug_id (str | None): Identifier to log for debugging. Defaults to None (will use generated UUID).
    """

    REPLAY_ALL: Final[int] = -1
    FLOW_IDX: int = 0

    @dataclass
    class SharedData(Generic[T_I]):
        """Common data used for internal management that should be accessed in critical sections"""

        current: T_I | None = None
        cache: list[T_I] = field(default_factory=list)
        q_dict: dict[UUID, asyncio.Queue[T_I]] = field(default_factory=dict)

        def __post_init__(self) -> None:  # noqa
            self._condition = asyncio.Condition()

        async def __aenter__(self) -> Self:  # noqa
            await self._condition.acquire()
            return self

        async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:  # noqa
            self._condition.release()

    def __init__(self, capacity: int = 100, debug_id: str | None = None) -> None:
        self._lock = asyncio.Condition()
        self._count = 0
        self._capacity = capacity
        self._debug_id = debug_id or str(Observable.FLOW_IDX)
        Observable.FLOW_IDX += 1
        self._on_start_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._on_subscribe_actions: list[Callable[[], None] | Callable[[], Coroutine[Any, Any, None]]] = []
        self._per_value_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._shared_data = Observable.SharedData[T]()
        # TODO handle cleanup

    def __copy__(self) -> Observable[T]:
        flow = Observable[T](capacity=self._capacity, debug_id=self._debug_id)
        # TODO do we actually want to copy all of these?
        flow._on_start_actions = self._on_start_actions
        flow._on_subscribe_actions = self._on_subscribe_actions
        flow._per_value_actions = self._per_value_actions
        flow._shared_data = self._shared_data
        return flow

    async def _add_collector(self, uuid: UUID, replay: int) -> None:
        """Add a flow to receive collected values

        Args:
            uuid (UUID): flow identifier
            replay (int): how many values to replay from cache
        """
        async with self._shared_data:
            if uuid not in self._shared_data.q_dict:
                self._shared_data.q_dict[uuid] = asyncio.Queue()
                if replay == Observable.REPLAY_ALL:
                    replay = len(self._shared_data.cache)
                head = max(len(self._shared_data.cache) - replay, 0)
                for value in self._shared_data.cache[head:]:
                    self._shared_data.q_dict[uuid].put_nowait(value)

    async def _remove_collector(self, uuid: UUID) -> None:
        """Remove a flow from receiving collected values

        Args:
            uuid (UUID): flow identifier
        """
        async with self._shared_data:
            if uuid in self._shared_data.q_dict:
                del self._shared_data.q_dict[uuid]

    async def emit(self, value: T) -> None:
        """Receive a value and queue it for per-flow retrieval

        Args:
            value (T): Value to queue
        """
        async with self._shared_data:
            self._shared_data.current = value
            self._shared_data.cache.append(value)
            if len(self._shared_data.cache) > self._capacity:
                self._shared_data.cache.pop(0)
            for uuid, q in self._shared_data.q_dict.items():
                logger.trace(f"Observable {self._debug_id} emitting {value} to observer {uuid}")  # type: ignore
                await q.put(value)

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

    async def _mux_filter_blocking(self, predicate: SyncFilter | AsyncFilter, value: T) -> bool:
        """Execute a filter that is either synchronous or asynchronous

        Note! This will await / block until the action completes.

        Args:
            predicate (SyncFilter | AsyncFilter): Filter to execute
            value (T): value to analyze with predicates

        Returns:
            bool: _description_
        """
        if iscoroutinefunction(predicate):
            return await predicate(value)
        return predicate(value)  # type: ignore

    @property
    def current(self) -> T | None:
        """Get the most recently collected value of the flow.

        Note that this does not indicate the value in real-time. It is the most recent value that was collected
        from a receiver.

        Returns:
            T | None: Most recently collected value, or None if no values were collected yet
        """
        return self._shared_data.current

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

    ####################################################################################################################
    ##### Terminal Operators
    ####################################################################################################################

    def observe(self, replay: int = 1, debug_id: str | None = None) -> Observer[T]:
        """Get an async generator to yield values from the flow

        Args:
            replay (int): how many values to replay from cache. Defaults to 1.
            debug_id (str | None): Identifier for debug logging. Defaults to None (will use generated UUID).

        Returns:
            AsyncGenerator[T, None]: async generator to yield values from the flow
        """

        # Create the enhanced generator with a unique ID
        return Observer(self, uuid1(), replay, debug_id=debug_id)

    async def _get_next(self, uuid: UUID) -> T:
        """Get the next flow value from the manager

        Args:
            uuid (UUID): Flow identifier

        Raises:
            RuntimeError: Flow ended without receiving any values

        Returns:
            FlowValue[T]: Latest flow value
        """
        while True:
            # If this is the first time entering, notify all on-subscribe listeners
            if self._count == 0:
                for action in self._on_subscribe_actions:
                    if iscoroutinefunction(action):
                        await action()
                    action()

            # Acquire the condition and read the per-collector value
            async with self._shared_data:
                if uuid not in self._shared_data.q_dict:
                    logger.error("Attempted to get value from a non-registered observer.")
                    raise RuntimeError("Observer has not been added!")
                q = self._shared_data.q_dict[uuid]
            # Note! This can't be called inside shared data context as it will cause a deadlock. We've already retrieved
            # the q here which is itself coroutine-safe so just await it.
            value = await q.get()
            self._count += 1

            # If this is the first value, notify on start listeners
            if self._count == 1:
                for action in self._on_start_actions:  # type: ignore
                    self._mux_action(action, value)  # type: ignore
            # Notify per-value actions
            for action in self._per_value_actions:  # type: ignore
                action(value)  # type: ignore
            # We've made it! Return the continuing value
            return value
