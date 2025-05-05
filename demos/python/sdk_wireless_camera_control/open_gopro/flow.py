"""Async generators to process asynchronous data flows.

TODO!!! This is fairly untested and has known issues for multiple transformations. Also chained transformations are
order-dependent: different orders will result in different behavior :(
"""

from __future__ import annotations

import asyncio
import logging
from copy import copy
from dataclasses import dataclass, field
from inspect import iscoroutinefunction
from typing import Any, Callable, Coroutine, Final, Generic, Self, TypeAlias, TypeVar
from uuid import UUID, uuid1

O = TypeVar("O")
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


T_I = TypeVar("T_I")


class Flow(Generic[T]):
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
        self._debug_id = debug_id or str(Flow.FLOW_IDX)
        Flow.FLOW_IDX += 1
        self._on_start_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._on_subscribe_actions: list[Callable[[], None] | Callable[[], Coroutine[Any, Any, None]]] = []
        self._per_value_actions: list[SyncAction[T] | AsyncAction[T]] = []
        self._take_count: int | None = None
        self._drop_count: int = 0
        self._shared_data = Flow.SharedData[T]()
        self._mappers: list[Callable[[Any], T]] = []
        self._filters: list[SyncFilter] = []
        # TODO handle cleanup

    def __copy__(self) -> Flow[T]:
        flow = Flow[T](capacity=self._capacity, debug_id=self._debug_id)
        # TODO do we actually want to copy all of these?
        flow._on_start_actions = self._on_start_actions
        flow._on_subscribe_actions = self._on_subscribe_actions
        flow._per_value_actions = self._per_value_actions
        flow._mappers = self._mappers
        flow._filters = self._filters
        flow._take_count = self._take_count
        flow._drop_count = self._drop_count
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
                if replay == Flow.REPLAY_ALL:
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
                logger.trace(f"Flow manager {self._debug_id} emitting {value} to flow {uuid}")  # type: ignore
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
        return self._shared_data.current

    ####################################################################################################################
    ##### Flow Manipulators
    ####################################################################################################################

    # TODO we need to add a pipeline for this to be used at the same time as take
    def drop(self: C, num: int) -> C:
        """Collect the first num values and ignore them

        Args:
            num (int): number of values to ignore

        Returns:
            C: modified flow
        """
        flow = copy(self)
        flow._drop_count = num
        return flow

    def take(self: C, num: int) -> C:
        """Configure the flow collection to stop after receiving a certain amount of values

        Args:
            num (int): number of values to take

        Returns:
            C: modified flow
        """
        flow = copy(self)
        flow._take_count = flow._count + num
        return flow

    # TODO we lost C. Is this going to work with subclasses? Maybe we need an interface / protocol
    def map(self, mapper: Callable[[T], O]) -> Flow[O]:
        """Apply the map transform on data elements

        Args:
            mapper (Callable[[T], O]): map transform to apply

        Returns:
            Flow[O]: Mapped flow
        """
        flow = copy(self)
        flow._mappers.append(mapper)  # type: ignore
        return flow  # type: ignore

    def filter(self: C, filter: SyncFilter) -> C:
        """Filter out elements using the provided boolean check

        Args:
            filter (SyncFilter): filter to apply

        Returns:
            C: modified flow
        """
        flow = copy(self)
        flow._filters.append(filter)
        return flow

    # TODO should this be done per collector?
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

    # TODO should this be done per collector?
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
    ############

    async def first(self, filter: SyncFilter, replay: int = 1) -> T:
        """Terminal receiver to collect only the first received value that matches a given filter

        Args:
            filter (SyncFilter): Filter to apply
            replay (int): how many values to replay from cache. Defaults to 1.

        Returns:
            T: first value matching filter
        """
        uuid = uuid1()
        await self._add_collector(uuid, replay)
        while True:
            match await self._get_next(uuid):
                case Continue(value):
                    if filter(value):
                        await self._remove_collector(uuid)
                        return value
                case Complete(value):
                    await self._remove_collector(uuid)
                    return value

    async def single(self, replay: int = 1) -> T:
        """Terminal receiver to collect the first received value.

        Args:
            replay (int): how many values to replay from cache. Defaults to 1.

        Returns:
            T: First received value
        """
        uuid = uuid1()
        await self._add_collector(uuid, replay)
        flow_value = await self._get_next(uuid)
        assert flow_value is not None
        await self._remove_collector(uuid)
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
        await self._add_collector(uuid, replay)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            while True:
                match await self._get_next(uuid):
                    case Continue(value):
                        return_value = value
                        if action:
                            self._mux_action(action, value, tg)
                    case Complete(value):
                        break
        await self._remove_collector(uuid)
        if return_value is None:
            raise RuntimeError("Failed to collect any values")
        return return_value

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
        await self._add_collector(uuid, replay)
        return_value: T | None = None
        async with asyncio.TaskGroup() as tg:
            if self.current and filter(self.current):
                return_value = self.current
            else:
                while True:
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
        await self._remove_collector(uuid)
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
        await self._add_collector(uuid, replay)
        if self.current and not self._mux_filter_blocking(action, self.current):
            await self._remove_collector(uuid)
            return self.current
        while True:
            return_value: T | None = None
            match await self._get_next(uuid):
                case Continue(value):
                    return_value = value
                    if not await self._mux_filter_blocking(action, value):
                        await self._remove_collector(uuid)
                        assert return_value is not None
                        return return_value
                case Complete(value):
                    await self._remove_collector(uuid)
                    if return_value is None:
                        raise RuntimeError("Failed to collect any values")
                    return return_value

    # TODO we have no way of ordering manipulators. I.e. a take always comes before a filter. We need a pipeline

    # TODO should we be using an async generator?
    async def _get_next(self, uuid: UUID) -> FlowValue[T]:
        """Get the next flow value from the manager

        Args:
            uuid (UUID): Flow identifier

        Raises:
            RuntimeError: Flow ended without receiving any values

        Returns:
            FlowValue[T]: Latest flow value
        """
        while True:
            # If we've reached our take limit, return (or raise if no value)
            # We do this first so that the previous iteration returns a valid value
            if self._take_count and self._count == self._take_count:
                if self.current is None:
                    raise RuntimeError("Failed to collect any values")
                return Complete(self.current)

            # If this is the first time entering, notify all on-subscribe listeners
            if self._count == 0:
                for action in self._on_subscribe_actions:
                    if iscoroutinefunction(action):
                        await action()
                    action()

            # Acquire the condition and read the per-collector value
            async with self._shared_data:
                if uuid not in self._shared_data.q_dict:
                    logger.error("Attempted to get value from a non-registered flow.")
                    raise RuntimeError("Flow has not been added!")
                q = self._shared_data.q_dict[uuid]
            # Note! This can't be called inside shared data context as it will cause a deadlock. We've already retrieved
            # the q here which is itself coroutine-safe so just await it.
            value = await q.get()
            self._count += 1

            # Find a non-dropped, non-filtered value.
            # First map it...
            for mapper in self._mappers:
                value = mapper(value)
            # See if its filtered
            should_continue = False
            for filter in self._filters:
                if not filter(value):
                    should_continue = True
                    break
            # It was filtered so advance the top level while loop
            if should_continue:
                continue
            # It wasn't filtered. See if we're dropping values.
            if self._drop_count > 0:
                self._drop_count -= 1
                continue
            # At this point, the value will be returned
            # If this is the first value, notify on start listeners
            if self._count == 1:
                for action in self._on_start_actions:  # type: ignore
                    self._mux_action(action, value)  # type: ignore
            # Notify per-value actions
            for action in self._per_value_actions:  # type: ignore
                action(value)  # type: ignore
            # We've made it! Return the continuing value
            return Continue(value)
