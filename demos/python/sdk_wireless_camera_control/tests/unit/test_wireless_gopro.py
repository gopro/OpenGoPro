# test_Wirelessgopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://Wirelessgopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Client"""

import asyncio
import test
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
from open_gopro.models.constants.constants import FeatureId
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

    results = await asyncio.gather(
        mock_wireless_gopro.ble_command.enable_wifi_ap(enable=False),
        mock_wireless_gopro._sync_resp_ready_q.put(mock_good_response),
    )

    assert results[0].ok
    assert await mock_wireless_gopro.ble_command.get_open_gopro_api_version()

    # Ensure keep alive was received and is correct
    assert (await mock_wireless_gopro.generic_spy.get())[0] == 66

    # Mock closing
    await asyncio.gather(mock_wireless_gopro.close(), set_disconnect_event())
    assert mock_wireless_gopro._keep_alive_task.cancelled


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


async def test_http_file(mock_wireless_gopro_basic: MockWirelessGoPro):
    message = HttpMessage("videos/DCIM/100GOPRO/dummy.MP4", None)
    out_file = Path("test.mp4")
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
        identifier=ProtobufId(FeatureId.COMMAND, None),
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
    # Make it appear to be the synchronous response
    await mock_wireless_gopro_basic._sync_resp_wait_q.put(mock_response)
    # Route the mock response
    await mock_wireless_gopro_basic._route_response(mock_response)
    # Get the routed response
    routed_response = await mock_wireless_gopro_basic._sync_resp_ready_q.get()

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
    # Make it appear to be the synchronous response
    await mock_wireless_gopro_basic._sync_resp_wait_q.put(mock_response)
    # Route the mock response
    await mock_wireless_gopro_basic._route_response(mock_response)
    # Get the routed response
    routed_response = await mock_wireless_gopro_basic._sync_resp_ready_q.get()

    # THEN
    assert routed_response.data == 1


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
