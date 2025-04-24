import asyncio

import pytest

from open_gopro.api.gopro_flow import (
    GoproRegisterFlow,
    GoproRegisterFlowDistinctInitial,
)
from open_gopro.constants.statuses import StatusId
from open_gopro.flow import Flow, FlowManager
from tests.mocks import MockWirelessGoPro


@pytest.mark.asyncio
async def test_flow_get_2_values():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    complete = asyncio.Event()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)

    async def single_get_values():
        assert await flow.single() == 0
        assert flow.current == 0
        assert await flow.single() == 1
        assert flow.current == 1
        complete.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        tg.create_task(single_get_values())

    await asyncio.wait_for(complete.wait(), 2)


@pytest.mark.asyncio
async def test_flow_on_start_sync_action():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(flow.on_start(lambda _: on_start.set()).single())

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0
    assert await flow.single() == 1
    assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_on_start_async_action():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    on_start = asyncio.Event()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)

    async def set_event_on_start(value: int) -> None:
        on_start.set()

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        single = tg.create_task(flow.on_start(set_event_on_start).single())

    # THEN
    assert single.result() == 0
    assert await asyncio.wait_for(on_start.wait(), 1)
    assert flow.current == 0
    assert await flow.single() == 1
    assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_collect_until_async_collector():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)

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
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)

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
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)
        await manager.emit(3)

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
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    received: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)
        await manager.emit(3)

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


# TODO figure out how / if we want to handle replay
# @pytest.mark.asyncio
# async def test_flow_replays_current_value_for_new_subscriber():
#     # GIVEN
#     manager: FlowManager[int] = FlowManager()

#     # WHEN
#     await manager.emit(0)
#     await manager.emit(1)
#     flow = Flow(manager)

#     # THEN
#     assert await anext(flow) == 1
#     assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_first():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        matched = tg.create_task(flow.first(lambda x: x == 1))

    # THEN
    assert matched.result() == 1


@pytest.mark.asyncio
async def test_flow_drop_2():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)
        await manager.emit(3)

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
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)
        await manager.emit(3)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_values())
        collector = tg.create_task(flow.take(2).collect(lambda x: collected.append(x)))

    # THEN
    assert collected == [0, 1]
    assert collector.result() == 1


@pytest.mark.asyncio
async def test_simultaneous_collect_first():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    started = asyncio.Event()
    flow = Flow(manager).on_subscribe(lambda: started.set())
    collected: list[int] = []

    # WHEN
    async def emit_values():
        await started.wait()
        await manager.emit(0)
        await manager.emit(1)
        await manager.emit(2)
        await manager.emit(3)
        await manager.emit(4)

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
        emit_status(False)
        emit_status(True)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(emit_statuses())
        collector = tg.create_task(flow.take(3).collect(lambda x: values.append(x)))

    # THEN
    assert values == [True, False, False, True]
    assert collector.result() == True


@pytest.mark.asyncio
async def test_status_flow_different_initial_response(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    flow = await GoproRegisterFlowDistinctInitial(
        gopro=mock_wireless_gopro_basic,
        update=StatusId.ENCODING,
        register_command=mock_wireless_gopro_basic.ble_command.get_open_gopro_api_version(),
    ).start()

    def emit_status(encoding: bool):
        if encoding:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x01])
        else:
            payload = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
        mock_wireless_gopro_basic._notification_handler(0xFF, payload)

    # WHEN
    emit_status(False)
    emit_status(False)
    values: list[str | bool] = []
    async with flow:
        values.append(flow.initial_response)
        emit_status(True)
        emit_status(True)
        emit_status(True)
        emit_status(True)

        await flow.take(2).collect(lambda status: values.append(status))

    # THEN
    assert values == ["2.0", False, False]
