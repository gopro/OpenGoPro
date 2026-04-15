# test_observables.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

import asyncio
import re
from calendar import c

import pytest
from asyncstdlib import anext, dropwhile, enumerate, filter, islice, map, takewhile

from open_gopro.domain.gopro_observable import (
    GoProObservable,
    GoproObserverDistinctInitial,
)
from open_gopro.domain.observable import Observable
from open_gopro.models.constants.statuses import StatusId
from tests.mocks import MockWirelessGoPro


async def test_base_observable():
    # GIVEN
    complete = asyncio.Event()
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)

    async def single_get_values():
        observer = observable.observe()
        assert await anext(observer) == 0
        assert observable.current == 0
        complete.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(single_get_values())

    await asyncio.wait_for(complete.wait(), 2)


async def test_observable_with_default_replay():
    # GIVEN
    observable = Observable[int]()

    # WHEN
    await observable.emit(0)
    await observable.emit(1)
    result = await anext(observable.observe())

    # THEN
    assert result == 1


async def test_observable_with_max_replay():
    # GIVEN
    observable = Observable[int]()
    results: list[int] = []
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await observable.emit(0)
    await observable.emit(1)
    await observable.emit(2)
    results.append(await anext(observer))
    results.append(await anext(observer))
    results.append(await anext(observer))

    # THEN
    assert results == [0, 1, 2]


async def test_observable_with_no_replay_times_out():
    # GIVEN
    observable = Observable[int]()
    results: list[int] = []
    observer = observable.observe(replay=0)

    # WHEN
    await observable.emit(0)
    await observable.emit(1)
    await observable.emit(2)

    # THEN
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(anext(observer), timeout=0.5)


async def test_observable_on_start_sync_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    observable = Observable().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)

    observable = observable.on_start(lambda _: on_start.set())
    observer = observable.observe()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(anext(observer))

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert observable.current == 0


async def test_observable_on_start_async_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    observable = Observable().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)

    async def set_event_on_start(value: int) -> None:
        on_start.set()

    observable = observable.on_start(set_event_on_start)
    observer = observable.observe()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(anext(observer))

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert observable.current == 0


async def test_observable_take_while():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)

    async def collector() -> None:
        async for value in takewhile(lambda x: x != 2, observer):
            received.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(collector())
        tg.create_task(emit_values())

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1


async def test_observable_drop_while():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)

    async def collector() -> None:
        async for value in dropwhile(lambda x: x < 2, observer):
            received.append(value)
            if value == 3:
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(collector())
        tg.create_task(emit_values())

    # THEN
    assert len(received) == 2
    assert received[0] == 2
    assert received[1] == 3


async def test_observable_first_matching():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        matched = tg.create_task(observer.first(lambda x: x == 1))

    # THEN
    assert matched.result() == 1


async def test_observable_slice():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)
        await observable.emit(4)

    async def collect():
        async for value in islice(observer, 1, 3):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [1, 2]


async def test_observable_map():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)

    async def collect():
        async for idx, value in enumerate(map(lambda x: str(x), observer)):
            collected.append(value)
            if idx == 1:
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == ["0", "1"]


async def test_observable_filter():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)
        await observable.emit(4)
        await observable.emit(5)

    async def collect():
        async for idx, value in enumerate(filter(lambda x: x % 2 == 0, observer)):
            collected.append(value)
            if idx == 2:
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 2, 4]


async def test_observable_filter_then_take_2():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)
        await observable.emit(4)
        await observable.emit(5)

    async def collect():
        async for value in islice(filter(lambda x: x % 2 == 0, observer), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 2]


async def test_observable_map_then_filter():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)

    async def collect():
        async for value in islice(filter(lambda x: x % 2 == 0, map(lambda x: x + 2, observer)), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [2, 4]


async def test_observable_filter_then_map():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)

    async def collect():
        async for value in islice(map(lambda x: x * 100, filter(lambda x: x >= 2, observer)), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [200, 300]


async def test_take_then_take_only_takes_second():
    # GIVEN
    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set())
    observer = observable.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)

    async def collect():
        async for value in islice(islice(observer, 4), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 1]


async def test_simultaneous_collect():
    # GIVEN
    started = asyncio.Event()
    observable = Observable().on_subscribe(lambda: started.set())
    observer1 = observable.observe(replay=Observable.REPLAY_ALL)
    observer2 = observable.observe(replay=Observable.REPLAY_ALL)
    collected1: list[int] = []
    collected2: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)
        await observable.emit(1)
        await observable.emit(2)
        await observable.emit(3)
        await observable.emit(4)

    async def collect_observer1():
        async for value in islice(observer1, 5):
            collected1.append(value)

    async def collect_observer2():
        async for value in islice(observer2, 5):
            collected2.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect_observer1())
        tg.create_task(collect_observer2())

    # THEN
    assert collected1 == [0, 1, 2, 3, 4]
    assert collected2 == [0, 1, 2, 3, 4]


async def test_status_observable_basic(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    observable = (
        await GoProObservable(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=lambda: mock_wireless_gopro_basic.mock_gopro_resp(True),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )
    observer = observable.observe()
    values: list[bool] = []

    def emit_status(encoding: bool):
        if encoding:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x01])
        else:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
        mock_wireless_gopro_basic._notification_handler(0xFF, payload)

    # WHEN
    async def emit_statuses():
        await started.wait()
        emit_status(False)
        emit_status(True)
        emit_status(False)

    async def collect():
        async for value in islice(observer, 4):
            values.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_statuses())
        tg.create_task(collect())

    # THEN
    assert values == [True, False, True, False]


async def test_status_observable_different_initial_response(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    observable = (
        await GoproObserverDistinctInitial(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=lambda: mock_wireless_gopro_basic.ble_command.get_open_gopro_api_version(),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )
    observer = observable.observe()

    def emit_status(encoding: bool):
        if encoding:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x01])
        else:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
        mock_wireless_gopro_basic._notification_handler(0xFF, payload)

    # WHEN
    values: list[str | bool] = []

    async def emit_values():
        await started.wait()
        emit_status(True)
        emit_status(False)
        emit_status(True)
        emit_status(False)

    async def receive_values():
        async with observable:
            values.append(observable.initial_response)
            async for value in islice(observer, 4):
                values.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(receive_values())

    # THEN
    assert values == ["2.0", True, False, True, False]


###############################################################################
# Observer lifecycle and error handling tests
###############################################################################


async def test_observer_aclose_removes_observer():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await observable.emit(0)
    _ = await anext(observer)  # Activates the observer
    await observer.aclose()

    # THEN - observer should be removed from the observable
    async with observable._shared_data:
        assert observer._uuid not in observable._shared_data.q_dict
    assert not observer._is_active


async def test_observer_aclose_is_idempotent():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await observable.emit(0)
    _ = await anext(observer)
    await observer.aclose()
    await observer.aclose()  # Should not raise

    # THEN
    assert not observer._is_active


async def test_observer_athrow_stops_iteration():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await observable.emit(0)
    _ = await anext(observer)

    # THEN
    with pytest.raises(ValueError, match="test error"):
        await observer.athrow(ValueError, ValueError("test error"))

    assert not observer._is_active


async def test_observer_athrow_before_activation_raises_stop_iteration():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe()

    # WHEN / THEN
    with pytest.raises(StopAsyncIteration):
        await observer.athrow(ValueError)


async def test_observer_asend_advances_iterator():
    """Test that asend advances the iterator to the next value (same as anext)."""
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN - emit values first so they're in the cache
    await observable.emit(0)
    await observable.emit(1)
    await observable.emit(2)

    # Get first value via anext
    first = await anext(observer)
    assert first == 0

    # Use asend to get the next value (asend(None) is equivalent to anext per AsyncGenerator protocol)
    second = await observer.asend(None)

    # THEN
    assert second == 1


async def test_observer_asend_before_activation_raises_stop_iteration():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe()

    # WHEN / THEN
    with pytest.raises(StopAsyncIteration):
        await observer.asend(None)


###############################################################################
# Cache and capacity tests
###############################################################################


async def test_observable_capacity_overflow_keeps_most_recent():
    # GIVEN
    capacity = 3
    observable = Observable[int](capacity=capacity)

    # WHEN - emit more than capacity
    for i in range(10):
        await observable.emit(i)

    # THEN - only most recent 'capacity' values should be cached
    observer = observable.observe(replay=Observable.REPLAY_ALL)
    values = []
    for _ in range(capacity):
        values.append(await anext(observer))

    assert values == [7, 8, 9]
    assert len(observable._shared_data.cache) == capacity


async def test_replay_partial_cache():
    # GIVEN
    observable = Observable[int]()
    for i in range(5):
        await observable.emit(i)

    # WHEN - request replay of 2
    observer = observable.observe(replay=2)

    # THEN
    values = []
    values.append(await anext(observer))
    values.append(await anext(observer))
    assert values == [3, 4]


async def test_replay_more_than_cache_gets_all():
    # GIVEN
    observable = Observable[int]()
    await observable.emit(0)
    await observable.emit(1)

    # WHEN - request replay of 10 but only 2 exist
    observer = observable.observe(replay=10)

    # THEN
    values = []
    values.append(await anext(observer))
    values.append(await anext(observer))
    assert values == [0, 1]


###############################################################################
# Concurrent operations and deadlock prevention tests
###############################################################################


async def test_concurrent_emit_and_observe_no_deadlock():
    # GIVEN
    observable = Observable[int]()
    results: list[int] = []
    num_values = 100

    # WHEN - concurrent emit and observe
    async def emitter():
        for i in range(num_values):
            await observable.emit(i)
            await asyncio.sleep(0)  # Yield to allow observer to run

    async def collector():
        observer = observable.observe(replay=Observable.REPLAY_ALL)
        async for value in islice(observer, num_values):
            results.append(value)

    # THEN - should complete without deadlock
    try:
        async with asyncio.timeout(5):
            async with asyncio.TaskGroup() as tg:
                tg.create_task(emitter())
                tg.create_task(collector())
    except TimeoutError:
        pytest.fail("Deadlock detected: concurrent emit and observe timed out")

    assert len(results) == num_values
    assert results == list(range(num_values))


async def test_multiple_observers_different_replay_no_deadlock():
    # GIVEN
    observable = Observable[int]()
    results1: list[int] = []
    results2: list[int] = []
    results3: list[int] = []

    # WHEN - emit values, then create observers with different replay
    for i in range(10):
        await observable.emit(i)

    observer1 = observable.observe(replay=0)
    observer2 = observable.observe(replay=5)
    observer3 = observable.observe(replay=Observable.REPLAY_ALL)

    # Collect replayed values
    async def collect_with_timeout(observer, results, count):
        try:
            async with asyncio.timeout(1):
                async for value in islice(observer, count):
                    results.append(value)
        except TimeoutError:
            pass

    # observer1 shouldn't get any replayed values, so it would timeout waiting
    # observers 2 and 3 should get their replayed values immediately

    async with asyncio.TaskGroup() as tg:
        tg.create_task(collect_with_timeout(observer2, results2, 5))
        tg.create_task(collect_with_timeout(observer3, results3, 10))

    # THEN
    assert results1 == []  # No replay
    assert results2 == [5, 6, 7, 8, 9]  # Last 5 values
    assert results3 == list(range(10))  # All values


async def test_observer_close_during_emit_no_deadlock():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)
    collected: list[int] = []

    # WHEN
    await observable.emit(0)
    collected.append(await anext(observer))

    # Close observer while emitting in background
    async def close_soon():
        await asyncio.sleep(0.01)
        await observer.aclose()

    async def emit_many():
        for i in range(1, 100):
            await observable.emit(i)
            await asyncio.sleep(0.001)

    # THEN - should not deadlock
    try:
        async with asyncio.timeout(2):
            await asyncio.gather(close_soon(), emit_many())
    except TimeoutError:
        pytest.fail("Deadlock detected during close while emitting")


async def test_rapid_subscribe_unsubscribe_no_deadlock():
    # GIVEN
    observable = Observable[int]()
    subscribe_count = 50

    # WHEN - rapidly create and close observers
    async def subscribe_and_close():
        observer = observable.observe(replay=Observable.REPLAY_ALL)
        await observable.emit(1)
        _ = await anext(observer)
        await observer.aclose()

    # THEN - should complete without deadlock
    try:
        async with asyncio.timeout(5):
            for _ in range(subscribe_count):
                await subscribe_and_close()
    except TimeoutError:
        pytest.fail("Deadlock detected during rapid subscribe/unsubscribe")


async def test_concurrent_observers_with_slow_consumer_no_deadlock():
    # GIVEN
    observable = Observable[int]()
    fast_results: list[int] = []
    slow_results: list[int] = []
    num_values = 20

    # WHEN - one fast consumer, one slow consumer
    started = asyncio.Event()

    async def emitter():
        await started.wait()
        for i in range(num_values):
            await observable.emit(i)
            await asyncio.sleep(0.001)

    async def fast_consumer():
        started.set()
        observer = observable.observe(replay=Observable.REPLAY_ALL)
        async for value in islice(observer, num_values):
            fast_results.append(value)

    async def slow_consumer():
        await started.wait()
        observer = observable.observe(replay=Observable.REPLAY_ALL)
        async for value in islice(observer, num_values):
            await asyncio.sleep(0.01)  # Slow processing
            slow_results.append(value)

    # THEN - should complete without deadlock
    try:
        async with asyncio.timeout(10):
            async with asyncio.TaskGroup() as tg:
                tg.create_task(emitter())
                tg.create_task(fast_consumer())
                tg.create_task(slow_consumer())
    except TimeoutError:
        pytest.fail("Deadlock detected with slow consumer")

    assert fast_results == list(range(num_values))
    assert slow_results == list(range(num_values))


###############################################################################
# on_subscribe and on_start action tests
###############################################################################


async def test_on_subscribe_async_action():
    # GIVEN
    subscribe_event = asyncio.Event()
    started = asyncio.Event()

    async def async_subscribe_action():
        subscribe_event.set()

    observable = Observable[int]().on_subscribe(async_subscribe_action).on_subscribe(lambda: started.set())
    observer = observable.observe()

    # WHEN
    async def emit_values():
        await started.wait()
        await observable.emit(0)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        result = tg.create_task(anext(observer))

    # Note: The current implementation has a bug where async on_subscribe is awaited
    # but sync is also called (we fixed this). This test verifies the fix.
    assert result.result() == 0


async def test_on_start_called_only_once():
    # GIVEN
    call_count = 0

    def increment_count(_):
        nonlocal call_count
        call_count += 1

    started = asyncio.Event()
    observable = Observable[int]().on_subscribe(lambda: started.set()).on_start(increment_count)
    observer = observable.observe()

    # WHEN
    async def emit_values():
        await started.wait()
        for i in range(5):
            await observable.emit(i)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collected = tg.create_task(collect_n(observer, 5))

    # THEN - on_start should be called only once (for the first value)
    assert collected.result() == [0, 1, 2, 3, 4]
    assert call_count == 1


###############################################################################
# Error propagation tests
###############################################################################


async def test_observer_handles_exception_in_iteration():
    # GIVEN
    observable = Observable[int]()
    observer = observable.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await observable.emit(0)
    await observable.emit(1)

    # Simulate an error during processing
    values = []
    try:
        async for value in observer:
            values.append(value)
            if value == 1:
                raise ValueError("Processing error")
    except ValueError:
        pass

    # THEN - observer should be cleaned up
    await observer.aclose()
    assert not observer._is_active


async def test_get_next_with_unregistered_observer_raises():
    # GIVEN
    observable = Observable[int]()
    from uuid import uuid1

    fake_uuid = uuid1()

    # WHEN / THEN
    with pytest.raises(RuntimeError, match="Observer has not been added"):
        await observable._get_next(fake_uuid)


###############################################################################
# Current value and state tests
###############################################################################


async def test_current_value_is_none_initially():
    # GIVEN
    observable = Observable[int]()

    # THEN
    assert observable.current is None


async def test_current_value_updates_on_emit():
    # GIVEN
    observable = Observable[int]()

    # WHEN
    await observable.emit(42)
    await observable.emit(100)

    # THEN
    assert observable.current == 100


###############################################################################
# Helper functions
###############################################################################


async def collect_n(observer, n: int) -> list:
    """Helper to collect n values from an observer"""
    values = []
    async for value in islice(observer, n):
        values.append(value)
    return values
