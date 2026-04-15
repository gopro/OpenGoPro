# test_Wirelessgopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://Wirelessgopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Client"""

import asyncio
from pathlib import Path

import pytest
import requests
import requests_mock

from open_gopro.domain.communicator_interface import HttpMessage
from open_gopro.domain.exceptions import GoProNotOpened, ResponseTimeout
from open_gopro.domain.parser_interface import GlobalParsers
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models import GoProResp
from open_gopro.models.constants import (
    ErrorCode,
    QueryCmdId,
    SettingId,
    StatusId,
    settings,
)
from open_gopro.models.constants.constants import ActionId, FeatureId
from open_gopro.models.constants.statuses import InternalBatteryBars
from open_gopro.models.proto.cohn_pb2 import NotifyCOHNStatus, ResponseCOHNCert
from open_gopro.models.types import ProtobufId, UpdateType
from tests import mock_good_response
from tests.mocks import (
    MockBleCommunicator,
    MockGoProMaintainBle,
    MockGoproResp,
    MockWirelessGoPro,
)


async def test_gopro_open(mock_wireless_gopro_basic: WirelessGoPro):
    await mock_wireless_gopro_basic.open()
    assert mock_wireless_gopro_basic.is_ble_connected
    assert mock_wireless_gopro_basic.is_http_connected
    assert mock_wireless_gopro_basic.identifier == "vice"


async def test_http_get(mock_wireless_gopro_basic: MockWirelessGoPro):
    message = HttpMessage("gopro/camera/stream/start", None)
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri("GET", mock_wireless_gopro_basic._base_url + message._endpoint, json="{}")
    mock_wireless_gopro_basic.set_requests_session(session)
    response = await mock_wireless_gopro_basic._get_json(message)
    assert response.ok


async def test_http_file(mock_wireless_gopro_basic: MockWirelessGoPro, tmp_path: Path):
    message = HttpMessage("videos/DCIM/100GOPRO/dummy.MP4", None)
    out_file = tmp_path / "test.mp4"
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri("GET", mock_wireless_gopro_basic._base_url + message._endpoint, text="BINARY DATA")
    mock_wireless_gopro_basic.set_requests_session(session)
    await mock_wireless_gopro_basic._get_stream(message, camera_file=out_file, local_file=out_file)
    assert out_file.exists()


async def test_http_response_timeout(mock_wireless_gopro_basic: MockWirelessGoPro):
    with pytest.raises(ResponseTimeout):
        message = HttpMessage("gopro/camera/stream/start", None)
        session = requests.Session()
        adapter = requests_mock.Adapter()
        session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
        adapter.register_uri(
            "GET", mock_wireless_gopro_basic._base_url + message._endpoint, exc=requests.exceptions.ConnectTimeout
        )
        mock_wireless_gopro_basic.set_requests_session(session)
        await mock_wireless_gopro_basic._get_json(message, timeout=1)


async def test_http_response_error(mock_wireless_gopro_basic: MockWirelessGoPro):
    message = HttpMessage("gopro/camera/stream/start", None)
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount(mock_wireless_gopro_basic._base_url + message._endpoint, adapter)
    adapter.register_uri(
        "GET",
        mock_wireless_gopro_basic._base_url + message._endpoint,
        status_code=403,
        reason="something bad happened",
        json="{}",
    )
    mock_wireless_gopro_basic.set_requests_session(session)
    response = await mock_wireless_gopro_basic._get_json(message)
    assert not response.ok


async def test_get_update(mock_wireless_gopro_basic: WirelessGoPro):
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()
    event = asyncio.Event()

    async def receive_encoding_status(id: UpdateType, value: bool):
        event.set()

    mock_wireless_gopro_basic.register_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    await event.wait()

    # Now ensure unregistering works
    event.clear()
    mock_wireless_gopro_basic.unregister_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x13, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(event.wait(), 1)


async def test_unsupported_protobuf_operation(mock_wireless_gopro_basic: WirelessGoPro):
    # GIVEN
    test_ready = asyncio.Event()
    mock_response = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.INVALID_PARAM,
        identifier=ProtobufId(FeatureId.COMMAND, ActionId.RESPONSE_CLEAR_COHN_CERT),
        data=None,
    )
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    # WHEN
    async def get_cohn_status() -> GoProResp[None]:
        test_ready.set()
        return await mock_wireless_gopro_basic.ble_command.cohn_clear_certificate()

    async def route_response():
        await test_ready.wait()
        await asyncio.sleep(1)  # TODO remove this
        await mock_wireless_gopro_basic._route_response(mock_response)

    async with asyncio.TaskGroup() as tg:
        cohn_task = tg.create_task(get_cohn_status())
        tg.create_task(route_response())
    response = cohn_task.result()

    # THEN
    assert cohn_task.done()
    assert response.status == ErrorCode.INVALID_PARAM


async def test_route_all_data(mock_wireless_gopro_basic: WirelessGoPro):
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    # GIVEN
    mock_data = {"one": 1, "two": 2}
    mock_response = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.SUCCESS,
        data=mock_data,
        identifier=QueryCmdId.GET_SETTING_VAL,
    )

    # WHEN
    # Create a Future and register it as pending
    future: asyncio.Future[GoProResp] = asyncio.Future()
    mock_wireless_gopro_basic._pending_responses.append((QueryCmdId.GET_SETTING_VAL, future))
    # Route the mock response - this should resolve the Future
    await mock_wireless_gopro_basic._route_response(mock_response)
    # Get the routed response from the resolved Future
    routed_response = await future

    # THEN
    assert routed_response.data == mock_data


async def test_route_individual_data(mock_wireless_gopro_basic: WirelessGoPro):
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    # GIVEN
    mock_data = {"one": 1}
    mock_response = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.SUCCESS,
        data=mock_data,
        identifier=QueryCmdId.GET_SETTING_VAL,
    )

    # WHEN
    # Create a Future and register it as pending
    future: asyncio.Future[GoProResp] = asyncio.Future()
    mock_wireless_gopro_basic._pending_responses.append((QueryCmdId.GET_SETTING_VAL, future))
    # Route the mock response - this should resolve the Future
    await mock_wireless_gopro_basic._route_response(mock_response)
    # Get the routed response from the resolved Future
    routed_response = await future

    # THEN
    assert routed_response.data == 1


async def test_concurrent_ble_messages_receive_correct_responses(mock_wireless_gopro_basic: WirelessGoPro):
    """Test that concurrent BLE message senders receive their own responses, not each other's.

    With the Future-based approach, each sender creates and awaits its own Future.
    When _route_response resolves a Future, only the sender waiting on that specific
    Future receives the response - eliminating the race condition.
    """
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    # GIVEN two different request identifiers
    request_1_id = QueryCmdId.GET_SETTING_VAL  # Sender 1's request
    request_2_id = QueryCmdId.GET_STATUS_VAL  # Sender 2's request

    response_for_sender_1 = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.SUCCESS,
        data={"setting": "value"},
        identifier=request_1_id,
    )
    response_for_sender_2 = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.SUCCESS,
        data={"status": "value"},
        identifier=request_2_id,
    )

    # Track which response each simulated sender receives
    received_responses: dict[str, GoProResp] = {}

    # Coordination events to precisely control timing
    sender1_registered = asyncio.Event()
    sender2_registered = asyncio.Event()

    # Create Futures for each sender
    future_1: asyncio.Future[GoProResp] = asyncio.Future()
    future_2: asyncio.Future[GoProResp] = asyncio.Future()

    async def simulate_sender_1():
        """Sender 1: registers first, awaits its own Future"""
        # Register our Future in the pending list FIRST
        mock_wireless_gopro_basic._pending_responses.append((request_1_id, future_1))
        sender1_registered.set()
        # Wait for sender 2 to also register
        await sender2_registered.wait()
        # Await our own Future - only we will receive this response
        response = await asyncio.wait_for(future_1, timeout=2)
        received_responses["sender1"] = response

    async def simulate_sender_2():
        """Sender 2: registers second, awaits its own Future"""
        # Wait for sender 1 to register
        await sender1_registered.wait()
        # Register our Future in the pending list SECOND
        mock_wireless_gopro_basic._pending_responses.append((request_2_id, future_2))
        sender2_registered.set()
        # Await our own Future - only we will receive this response
        response = await asyncio.wait_for(future_2, timeout=2)
        received_responses["sender2"] = response

    # Start both senders
    task1 = asyncio.create_task(simulate_sender_1())
    task2 = asyncio.create_task(simulate_sender_2())

    # Wait for both to be registered and waiting
    await sender2_registered.wait()
    await asyncio.sleep(0.01)  # Ensure both are blocked awaiting their Futures

    # WHEN: Route response for sender 1 (matches head of pending list: request_1_id)
    # This resolves future_1 directly - only sender 1 will wake up
    await mock_wireless_gopro_basic._route_response(response_for_sender_1)

    # Then route response for sender 2 (now matches new head: request_2_id)
    # This resolves future_2 directly - only sender 2 will wake up
    await mock_wireless_gopro_basic._route_response(response_for_sender_2)

    # Wait for both senders to complete
    await asyncio.gather(task1, task2)

    # THEN: Each sender receives ITS OWN response
    # With Direct Future resolution, this PASSES because:
    # - Each sender awaits its own Future
    # - _route_response resolves the specific Future for the matching identifier
    # - No race condition - responses go directly to the correct sender
    assert (
        received_responses["sender1"].identifier == request_1_id
    ), f"Sender 1 (expecting {request_1_id}) received wrong response: {received_responses['sender1'].identifier}"
    assert (
        received_responses["sender2"].identifier == request_2_id
    ), f"Sender 2 (expecting {request_2_id}) received wrong response: {received_responses['sender2'].identifier}"


async def test_out_of_order_ble_responses_routed_correctly(mock_wireless_gopro_basic: WirelessGoPro):
    """Test that responses arriving out of order are still routed to the correct sender.

    Scenario: A slow command (e.g., COHN) is pending at the head, then a fast command's
    response arrives. The fast response should match its sender, not be treated as async.

    Current bug: _route_response only checks the head, so the fast response gets
    misrouted as async because it doesn't match the slow command at the head.
    """
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    # GIVEN: Two requests registered - slow command first, fast command second
    slow_request_id = QueryCmdId.GET_SETTING_VAL  # Simulates slow COHN-like command
    fast_request_id = QueryCmdId.GET_STATUS_VAL  # Simulates fast LED-like command

    future_slow: asyncio.Future[GoProResp] = asyncio.Future()
    future_fast: asyncio.Future[GoProResp] = asyncio.Future()

    # Register slow command first (at head of queue)
    mock_wireless_gopro_basic._pending_responses.append((slow_request_id, future_slow))
    # Register fast command second (behind slow command)
    mock_wireless_gopro_basic._pending_responses.append((fast_request_id, future_fast))

    # Response for fast command (arrives first, out of order)
    fast_response = GoProResp(
        protocol=GoProResp.Protocol.BLE,
        status=ErrorCode.SUCCESS,
        data={"status": "fast_value"},
        identifier=fast_request_id,
    )

    # WHEN: Fast response arrives while slow command is still at head
    await mock_wireless_gopro_basic._route_response(fast_response)

    # THEN: Fast response should resolve the fast Future (not be treated as async)
    assert future_fast.done(), "Fast response should have resolved the fast Future"
    assert future_fast.result().identifier == fast_request_id
    # Note: _route_response unwraps single-value dicts for query responses
    assert future_fast.result().data == "fast_value"

    # AND: Slow Future should still be pending
    assert not future_slow.done(), "Slow Future should still be pending"

    # AND: Pending responses should only have the slow request left
    assert len(mock_wireless_gopro_basic._pending_responses) == 1
    assert mock_wireless_gopro_basic._pending_responses[0][0] == slow_request_id


async def test_get_update_unregister(mock_wireless_gopro_basic: WirelessGoPro):
    event = asyncio.Event()
    mock_wireless_gopro_basic._loop = asyncio.get_running_loop()

    async def receive_encoding_status(id: UpdateType, value: bool):
        event.set()

    mock_wireless_gopro_basic.register_update(receive_encoding_status, StatusId.ENCODING)
    not_encoding = bytearray([0x05, 0x93, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    await event.wait()

    # Now ensure unregistering works
    event.clear()
    mock_wireless_gopro_basic.unregister_update(receive_encoding_status)
    not_encoding = bytearray([0x05, 0x13, 0x00, StatusId.ENCODING.value, 0x01, 0x00])
    mock_wireless_gopro_basic._notification_handler(0xFF, not_encoding)
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(event.wait(), 1)


def test_get_param_values_by_id():
    vector = list(settings.VideoResolution)[0]
    assert GlobalParsers.get_query_container(SettingId.VIDEO_RESOLUTION)(vector.value) == vector


@pytest.mark.timeout(30)
async def test_lifecycle(mock_wireless_gopro: MockGoProMaintainBle):
    async def set_disconnect_event():
        mock_wireless_gopro._disconnect_handler(None)

    # We're not yet open so can't send commands
    assert not mock_wireless_gopro.is_open
    with pytest.raises(GoProNotOpened):
        await mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False)

    # Mock ble / wifi open
    await mock_wireless_gopro.open()
    assert mock_wireless_gopro.is_open

    # Ensure we can't send commands because not ready
    assert not await mock_wireless_gopro.is_ready
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False), 1)

    # Mock receiving initial not-encoding and not-busy statuses
    await mock_wireless_gopro._update_internal_state(update=StatusId.ENCODING, value=False)
    await mock_wireless_gopro._update_internal_state(update=StatusId.BUSY, value=False)
    assert await mock_wireless_gopro.is_ready

    async def provide_response():
        """Simulate the response being routed by resolving the pending Future"""
        # Wait a bit for the BLE command to register its Future
        await asyncio.sleep(0.1)
        # Get the pending Future and resolve it with a mock response
        if mock_wireless_gopro._pending_responses:
            _, future = mock_wireless_gopro._pending_responses[0]
            mock_wireless_gopro._pending_responses.pop(0)
            future.set_result(mock_good_response)

    results = await asyncio.gather(
        mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False),
        provide_response(),
    )

    assert results[0].ok
    assert await mock_wireless_gopro.ble_command.get_open_gopro_api_version()

    # Ensure keep alive was received and is correct
    assert (await mock_wireless_gopro.generic_spy.get())[0] == 66

    # Mock closing
    await asyncio.gather(mock_wireless_gopro.close(), set_disconnect_event())
    assert mock_wireless_gopro._keep_alive_task.cancelled
