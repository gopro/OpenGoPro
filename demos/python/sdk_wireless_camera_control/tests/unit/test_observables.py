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


@pytest.mark.asyncio
async def test_base_flow():
    # GIVEN
    complete = asyncio.Event()
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    async def single_get_values():
        flow_gen = flow.observe()
        assert await anext(flow_gen) == 0
        assert flow.current == 0
        complete.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(single_get_values())

    await asyncio.wait_for(complete.wait(), 2)


@pytest.mark.asyncio
async def test_flow_with_default_replay():
    # GIVEN
    flow = Observable[int]()

    # WHEN
    await flow.emit(0)
    await flow.emit(1)
    result = await anext(flow.observe())

    # THEN
    assert result == 1


@pytest.mark.asyncio
async def test_flow_with_max_replay():
    # GIVEN
    flow = Observable[int]()
    results: list[int] = []
    flow_gen = flow.observe(replay=Observable.REPLAY_ALL)

    # WHEN
    await flow.emit(0)
    await flow.emit(1)
    await flow.emit(2)
    results.append(await anext(flow_gen))
    results.append(await anext(flow_gen))
    results.append(await anext(flow_gen))

    # THEN
    assert results == [0, 1, 2]


@pytest.mark.asyncio
async def test_flow_with_no_replay_times_out():
    # GIVEN
    flow = Observable[int]()
    results: list[int] = []
    flow_gen = flow.observe(replay=0)

    # WHEN
    await flow.emit(0)
    await flow.emit(1)
    await flow.emit(2)

    # THEN
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(anext(flow_gen), timeout=0.5)


@pytest.mark.asyncio
async def test_flow_on_start_sync_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Observable().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    flow = flow.on_start(lambda _: on_start.set())
    flow_gen = flow.observe()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(anext(flow_gen))

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0


@pytest.mark.asyncio
async def test_flow_on_start_async_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Observable().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    async def set_event_on_start(value: int) -> None:
        on_start.set()

    flow = flow.on_start(set_event_on_start)
    flow_gen = flow.observe()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(anext(flow_gen))

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0


@pytest.mark.asyncio
async def test_flow_take_while():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)

    async def collector() -> None:
        async for value in takewhile(lambda x: x != 2, flow_gen):
            received.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(collector())
        tg.create_task(emit_values())

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1


@pytest.mark.asyncio
async def test_flow_drop_while():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async def collector() -> None:
        async for value in dropwhile(lambda x: x < 2, flow_gen):
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


@pytest.mark.asyncio
async def test_flow_first_matching():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        matched = tg.create_task(flow_gen.first(lambda x: x == 1))

    # THEN
    assert matched.result() == 1


@pytest.mark.asyncio
async def test_flow_slice():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)
        await flow.emit(4)

    async def collect():
        async for value in islice(flow_gen, 1, 3):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [1, 2]


@pytest.mark.asyncio
async def test_flow_map():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)

    async def collect():
        async for idx, value in enumerate(map(lambda x: str(x), flow_gen)):
            collected.append(value)
            if idx == 1:
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == ["0", "1"]


@pytest.mark.asyncio
async def test_flow_filter():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)
        await flow.emit(4)
        await flow.emit(5)

    async def collect():
        async for idx, value in enumerate(filter(lambda x: x % 2 == 0, flow_gen)):
            collected.append(value)
            if idx == 2:
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 2, 4]


@pytest.mark.asyncio
async def test_flow_filter_then_take_2():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)
        await flow.emit(4)
        await flow.emit(5)

    async def collect():
        async for value in islice(filter(lambda x: x % 2 == 0, flow_gen), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 2]


@pytest.mark.asyncio
async def test_flow_map_then_filter():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async def collect():
        async for value in islice(filter(lambda x: x % 2 == 0, map(lambda x: x + 2, flow_gen)), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [2, 4]


@pytest.mark.asyncio
async def test_flow_filter_then_map():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async def collect():
        async for value in islice(map(lambda x: x * 100, filter(lambda x: x >= 2, flow_gen)), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [200, 300]


@pytest.mark.asyncio
async def test_take_then_take_only_takes_second():
    # GIVEN
    started = asyncio.Event()
    flow = Observable[int]().on_subscribe(lambda: started.set())
    flow_gen = flow.observe()
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async def collect():
        async for value in islice(islice(flow_gen, 4), 2):
            collected.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect())

    # THEN
    assert collected == [0, 1]


@pytest.mark.asyncio
async def test_simultaneous_collect():
    # GIVEN
    started = asyncio.Event()
    flow = Observable().on_subscribe(lambda: started.set())
    flow_gen1 = flow.observe(replay=Observable.REPLAY_ALL)
    flow_gen2 = flow.observe(replay=Observable.REPLAY_ALL)
    collected1: list[int] = []
    collected2: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)
        await flow.emit(4)

    async def collect_flow_gen1():
        async for value in islice(flow_gen1, 5):
            collected1.append(value)

    async def collect_flow_gen2():
        async for value in islice(flow_gen2, 5):
            collected2.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(collect_flow_gen1())
        tg.create_task(collect_flow_gen2())

    # THEN
    assert collected1 == [0, 1, 2, 3, 4]
    assert collected2 == [0, 1, 2, 3, 4]


@pytest.mark.asyncio
async def test_status_flow_basic(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    flow = (
        await GoProObservable(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=mock_wireless_gopro_basic.mock_gopro_resp(True),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )
    flow_gen = flow.observe()
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
        async for value in islice(flow_gen, 4):
            values.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_statuses())
        tg.create_task(collect())

    # THEN
    assert values == [True, False, True, False]


@pytest.mark.asyncio
async def test_status_flow_different_initial_response(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    flow = (
        await GoproObserverDistinctInitial(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=mock_wireless_gopro_basic.ble_command.get_open_gopro_api_version(),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )
    flow_gen = flow.observe()

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
        async with flow:
            values.append(flow.initial_response)
            async for value in islice(flow_gen, 4):
                values.append(value)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(receive_values())

    # THEN
    assert values == ["2.0", True, False, True, False]
