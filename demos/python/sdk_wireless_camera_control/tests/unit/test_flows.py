import asyncio

import pytest

from open_gopro.api.gopro_flow import (
    GoproRegisterFlow,
    GoproRegisterFlowDistinctInitial,
)
from open_gopro.constants.statuses import StatusId
from open_gopro.domain.flow import Flow
from tests.mocks import MockWirelessGoPro


@pytest.mark.asyncio
async def test_flow_single():
    # GIVEN
    complete = asyncio.Event()
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    async def single_get_values():
        assert await flow.single() == 0
        assert flow.current == 0
        complete.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(single_get_values())

    await asyncio.wait_for(complete.wait(), 2)


@pytest.mark.asyncio
async def test_flow_single_with_replay():
    # GIVEN
    flow = Flow()

    # WHEN
    await flow.emit(0)
    result = await flow.single(replay=Flow.REPLAY_ALL)

    # THEN
    assert result == 0


@pytest.mark.asyncio
async def test_flow_get_2_values_via_replay():
    # GIVEN
    complete = asyncio.Event()
    started = asyncio.Event()
    flow = Flow()

    # WHEN
    async def emit_values():
        await flow.emit(0)
        await flow.emit(1)
        started.set()

    async def single_get_values():
        await started.wait()
        assert await flow.single(replay=Flow.REPLAY_ALL) == 0
        assert flow.current == 1
        assert await flow.single(replay=Flow.REPLAY_ALL) == 0
        assert flow.current == 1
        complete.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(single_get_values())

    await asyncio.wait_for(complete.wait(), 2)


@pytest.mark.asyncio
async def test_flow_on_start_sync_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(flow.on_start(lambda _: on_start.set()).single())

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0


@pytest.mark.asyncio
async def test_flow_on_start_async_action():
    # GIVEN
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)

    async def set_event_on_start(value: int) -> None:
        on_start.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(flow.on_start(set_event_on_start).single())

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0


@pytest.mark.asyncio
async def test_flow_collect_until_async_collector():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)

    async def collector(value: int) -> None:
        received.append(value)

    async with asyncio.TaskGroup() as tg:
        collect = tg.create_task(flow.collect_until(filter=lambda x: x == 2, action=collector))
        tg.create_task(emit_values())
    final = collect.result()

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_collect_until_sync_collector():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)

    def collector(value: int) -> None:
        received.append(value)

    async with asyncio.TaskGroup() as tg:
        collect = tg.create_task(flow.collect_until(filter=lambda x: x == 2, action=collector))
        tg.create_task(emit_values())
    final = collect.result()

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_collect_while_async_collector():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async def collector(value: int) -> bool:
        if value != 2:
            received.append(value)
            return True
        return False

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collect = tg.create_task(flow.collect_while(action=collector))

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert collect.result() == 2


@pytest.mark.asyncio
async def test_flow_collect_while_sync_collector():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    def collector(value: int) -> bool:
        if value != 2:
            received.append(value)
            return True
        return False

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collect = tg.create_task(flow.collect_while(action=collector))

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert collect.result() == 2


@pytest.mark.asyncio
async def test_flow_first():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        matched = tg.create_task(flow.first(lambda x: x == 1))

    # THEN
    assert matched.result() == 1


@pytest.mark.asyncio
async def test_flow_drop_2():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(
            flow.drop(2).collect_until(
                filter=lambda x: x == 3,
                action=lambda x: collected.append(x),
            )
        )

    # THEN
    assert collected == [2]
    assert collector.result() == 3


@pytest.mark.asyncio
async def test_flow_take_2():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(2).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 1]
    assert collector.result() == 1


@pytest.mark.asyncio
async def test_flow_map():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(2).map(lambda x: str(x)).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == ["0", "1"]
    assert collector.result() == "1"


@pytest.mark.asyncio
async def test_flow_filter():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(4).filter(lambda x: x % 2 == 0).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 2]
    assert collector.result() == 2


@pytest.mark.asyncio
async def test_flow_filter_then_take():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.filter(lambda x: x % 2 == 0).take(2).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 2]
    assert collector.result() == 2


@pytest.mark.asyncio
async def test_flow_map_then_filter():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(
            flow.take(4)
            .map(mapper=lambda x: x + 2)
            .filter(filter=lambda x: x % 2 == 0)
            .collect(action=lambda x: collected.append(x))
        )

    # THEN
    assert collected == [2, 4]
    assert collector.result() == 4


@pytest.mark.asyncio
async def test_flow_filter_then_map():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(
            flow.take(4)
            .filter(filter=lambda x: x >= 2)
            .map(mapper=lambda x: x + 2)
            .collect(action=lambda x: collected.append(x))
        )

    # THEN
    assert collected == [4, 5]
    assert collector.result() == 5


@pytest.mark.asyncio
async def test_take_then_take_only_takes_second():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(4).take(2).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 1]
    assert collector.result() == 1


# TODO this should fail with a timeout. Or maybe kill the first flow (take 2) and throw some type of error.
@pytest.mark.xfail
@pytest.mark.asyncio
async def test_take_then_take_too_many_hangs():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(2).take(4).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 1]
    assert collector.result() == 1


@pytest.mark.asyncio
async def test_take_then_drop():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(3).drop(1).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [1, 2]
    assert collector.result() == 2


@pytest.mark.asyncio
async def test_drop_then_take():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.drop(1).take(3).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [1, 2, 3]
    assert collector.result() == 3


@pytest.mark.asyncio
async def test_complex_flow():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[str] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)  # drop
        await flow.emit(1)  # drop
        await flow.emit(2)  # take 1, filtered out by second filter
        await flow.emit(3)  # filtered out
        await flow.emit(4)  # take 2
        await flow.emit(5)  # filtered out
        await flow.emit(6)  # take 3
        await flow.emit(7)  # ignored
        await flow.emit(8)  # ignored

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(
            flow.drop(2)
            .filter(lambda x: x % 2 == 0)
            .map(lambda x: x * 100)
            .take(3)
            .filter(lambda x: x > 200)
            .collect(lambda x: collected.append(x))
        )

    # THEN
    assert collected == [400, 600]
    assert collector.result() == 600


@pytest.mark.asyncio
async def test_simultaneous_collect_first():
    # GIVEN
    started = asyncio.Event()
    flow = Flow().on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await flow.emit(0)
        await flow.emit(1)
        await flow.emit(2)
        await flow.emit(3)
        await flow.emit(4)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        first_2 = tg.create_task(flow.first(lambda x: x == 2))
        collector = tg.create_task(
            flow.collect_until(
                filter=lambda x: x == 4,
                action=lambda x: collected.append(x),
            )
        )

    # THEN
    assert collected == [0, 1, 2, 3]
    assert first_2.result() == 2
    assert collector.result() == 4


@pytest.mark.asyncio
async def test_status_flow_basic(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    flow = (
        await GoproRegisterFlow(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=mock_wireless_gopro_basic.mock_gopro_resp(True),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )
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

    async def collect(status):
        values.append(status)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_statuses())
        collector = tg.create_task(flow.take(4).collect(collect))

    # THEN
    assert values == [True, False, True, False]
    assert collector.result() == False


@pytest.mark.asyncio
async def test_status_flow_different_initial_response(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    started = asyncio.Event()
    flow = (
        await GoproRegisterFlowDistinctInitial(
            gopro=mock_wireless_gopro_basic,
            update=StatusId.ENCODING,
            register_command=mock_wireless_gopro_basic.ble_command.get_open_gopro_api_version(),
        )
        .on_subscribe(lambda: started.set())
        .start()
    )

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
            await flow.take(4).collect(lambda status: values.append(status))

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(receive_values())

    # THEN
    assert values == ["2.0", True, False, True, False]
