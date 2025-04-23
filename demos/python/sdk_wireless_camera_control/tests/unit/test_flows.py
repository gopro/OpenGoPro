from optparse import Values
import pytest
import asyncio

from open_gopro.api.status_flow import StatusFlow, StatusFlowSeparateInitial
from open_gopro.constants.statuses import StatusId
from open_gopro.flow import Flow, FlowManager
from tests.mocks import MockWirelessGoPro


@pytest.mark.asyncio
async def test_flow_get_2_values():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)

    # THEN
    assert await anext(flow) == 0
    assert flow.current == 0
    assert await anext(flow) == 1
    assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_single():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)

    # THEN
    assert await flow.single() == 0
    assert flow.current == 0


@pytest.mark.asyncio
async def test_flow_on_start():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)
    caught_on_start = False

    # WHEN
    await manager.emit(0)
    await manager.emit(1)

    # THEN
    def set_on_start(value: int):
        nonlocal caught_on_start
        caught_on_start = True

    assert await flow.on_start(set_on_start).single() == 0
    assert flow.current == 0
    assert await flow.single() == 1
    assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_collect_until_async_collector():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)
    received: list[int] = []

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)

    async def collector(value: int) -> None:
        received.append(value)

    final = await flow.collect_until(filter=lambda x: x == 2, action=collector)

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_collect_until_sync_collector():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)
    received: list[int] = []

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)

    def collector(value: int) -> None:
        received.append(value)

    final = await flow.collect_until(filter=lambda x: x == 2, action=collector)

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_collect_while_async_collector():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)
    received: list[int] = []

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)
    await manager.emit(3)

    async def collector(value: int) -> bool:
        if value != 2:
            received.append(value)
            return True
        return False

    final = await flow.collect_while(action=collector)

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_collect_while_sync_collector():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)
    received: list[int] = []

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)
    await manager.emit(3)

    def collector(value: int) -> bool:
        if value != 2:
            received.append(value)
            return True
        return False

    final = await flow.collect_while(action=collector)

    # THEN
    assert len(received) == 2
    assert received[0] == 0
    assert received[1] == 1
    assert final == 2


@pytest.mark.asyncio
async def test_flow_replays_current_value_for_new_subscriber():
    # GIVEN
    manager: FlowManager[int] = FlowManager()

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    flow = Flow(manager)

    # THEN
    assert await anext(flow) == 1
    assert flow.current == 1


@pytest.mark.asyncio
async def test_flow_iterator():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)

    # THEN
    idx = 0
    async for value in flow:
        assert value == idx
        assert flow.current == idx
        idx += 1
        if idx == 1:
            break
    assert idx == 1


@pytest.mark.asyncio
async def test_flow_first():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    matched = await flow.first(lambda x: x == 1)

    # THEN
    assert matched == 1


@pytest.mark.asyncio
async def test_flow_drop_2():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)
    await manager.emit(3)
    flow = await flow.drop(2)

    # THEN
    assert flow.current == 1
    assert await anext(flow) == 2
    assert flow.current == 2
    assert await anext(flow) == 3
    assert flow.current == 3


@pytest.mark.asyncio
async def test_flow_take_2():
    # GIVEN
    manager: FlowManager[int] = FlowManager()
    flow = Flow(manager)

    # WHEN
    await manager.emit(0)
    await manager.emit(1)
    await manager.emit(2)
    await manager.emit(3)
    flow = flow.take(2)

    # THEN
    assert flow.current == None
    assert await anext(flow) == 0
    assert flow.current == 0
    assert await anext(flow) == 1
    assert flow.current == 1
    with pytest.raises(StopAsyncIteration):
        await anext(flow)


@pytest.mark.asyncio
async def test_status_flow_basic(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    flow = await StatusFlow(
        gopro=mock_wireless_gopro_basic,
        update=StatusId.ENCODING,
        register_command=mock_wireless_gopro_basic.mock_gopro_resp(True),
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
    emit_status(True)
    values = [await flow.single(), await flow.single(), await flow.single(), await flow.single()]

    # THEN
    assert values == [True, False, False, True]


@pytest.mark.asyncio
async def test_status_flow_different_initial_response(mock_wireless_gopro_basic: MockWirelessGoPro):
    # GIVEN
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    flow = await StatusFlowSeparateInitial(
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
