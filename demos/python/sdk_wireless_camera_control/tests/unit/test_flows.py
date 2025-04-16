import pytest

from open_gopro.flow import Flow, FlowManager


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
async def test_flow_collect_until():
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
async def test_flow_collect_while():
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
