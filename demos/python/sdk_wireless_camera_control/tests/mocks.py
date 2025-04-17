# mocks.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Mar 20 21:57:17 UTC 2025

import asyncio
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generic, Optional, Pattern

from open_gopro import WiredGoPro, WirelessGoPro
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WirelessApi,
)
from open_gopro.ble import (
    BLEController,
    BleDevice,
    BleHandle,
    BleUUID,
    DisconnectHandlerType,
    NotiHandlerType,
)
from open_gopro.communicator_interface import (
    BleMessage,
    GoProBle,
    GoProWifi,
    HttpMessage,
    MessageRules,
)
from open_gopro.constants import CmdId, GoProUUID, StatusId
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice
from open_gopro.features.access_point import AccessPointFeature
from open_gopro.features.base_feature import BaseFeature
from open_gopro.gopro_base import GoProBase
from open_gopro.models.response import GoProResp
from open_gopro.types import CameraState, UpdateCb, UpdateType
from open_gopro.wifi import SsidState, WifiController
from tests import mock_good_response, versions

api_versions = {"2.0": WirelessApi}


@dataclass
class MockGattTable:
    def handle2uuid(self, *args):
        return GoProUUID.CQ_QUERY_RESP


class MockBleController(BLEController, Generic[BleHandle, BleDevice]):
    # pylint: disable=signature-differs

    def __init__(self, *args, **kwargs) -> None:
        self.gatt_db = MockGattTable()

    async def scan(self, token: Pattern, timeout: int, service_uuids: list[BleUUID] = None) -> str:
        if token == re.compile(".*device") or token == "device":
            return "scanned_device"
        raise FailedToFindDevice

    async def read(self, handle: BleHandle, uuid: str) -> bytearray:
        return bytearray()

    async def write(self, handle: BleHandle, uuid: str, data: bytearray) -> None:
        return

    async def connect(self, disconnect_cb: DisconnectHandlerType, device: BleDevice, timeout: int) -> str:
        if disconnect_cb is None:
            raise ConnectFailed("forced connect fail from test", timeout, 1)
        return "connected_device"

    async def pair(self, handle: BleHandle) -> None:
        return

    async def enable_notifications(self, handle: BleHandle, handler: NotiHandlerType) -> None:
        return

    async def discover_chars(self, handle: BleHandle, service_uuids: list[BleUUID] = None) -> MockGattTable:
        return self.gatt_db

    async def disconnect(self, handle: BleHandle) -> None:
        return


def disconnection_handler(_) -> None:
    print("Entered test disconnect callback")


def notification_handler(handle: int, data: bytearray) -> None:
    print("Entered test notification callback")


class MockBleCommunicator(GoProBle):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str) -> None:
        super().__init__(
            MockBleController(),
            disconnection_handler,
            notification_handler,
            "target",
        )
        self._api = api_versions[test_version](self)

    def identifier(self) -> str:
        return "identifier"

    def _register_update(self, callback: UpdateCb, update: GoProBle._CompositeRegisterType | UpdateType) -> None:
        return

    def _unregister_update(
        self, callback: UpdateCb, update: GoProBle._CompositeRegisterType | UpdateType | None = None
    ) -> None:
        return

    def register_update(self, callback: UpdateCb, update: UpdateType) -> None:
        return

    def unregister_update(self, callback: UpdateCb, update: UpdateType | None = None) -> None:
        return

    async def _send_ble_message(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        return dict(uuid=message._uuid, packet=message._build_data(**kwargs))

    async def _read_ble_characteristic(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        return dict(uuid=message._uuid)

    @property
    def ble_command(self) -> BleCommands:
        return self._api.ble_command

    @property
    def ble_setting(self) -> BleSettings:
        return self._api.ble_setting

    @property
    def ble_status(self) -> BleStatuses:
        return self._api.ble_status


class MockWifiController(WifiController):
    # pylint: disable=signature-differs

    def __init__(self, interface: Optional[str] = None, password: Optional[str] = None) -> None: ...

    async def connect(self, ssid: str, password: str, timeout: float) -> bool:
        return True if password == "password" else False

    async def disconnect(self) -> bool:
        return True

    def current(self) -> tuple[Optional[str], SsidState]:
        return "current_ssid", SsidState.CONNECTED

    def available_interfaces(self) -> list[str]:
        return ["interface1", "interface2"]

    def power(self, power: bool) -> None:
        return

    def is_on(self) -> bool:
        return True


@dataclass
class MockWifiResponse:
    url: str
    body: dict[str, Any] = field(default_factory=dict)


class MockWifiCommunicator(GoProWifi):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str):
        super().__init__(MockWifiController())
        self._api = api_versions[test_version](self)

    @property
    def identifier(self) -> str:
        return "identifier"

    async def _get_json(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules = MessageRules(), **kwargs
    ) -> GoProResp:
        return MockWifiResponse(message.build_url(**kwargs), message.build_body(**kwargs))

    async def _get_stream(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules = MessageRules(), **kwargs
    ) -> GoProResp:
        return MockWifiResponse(message.build_url(path=kwargs["camera_file"])), kwargs["local_file"]

    async def _put_json(
        self, message: HttpMessage, *, timeout: int = 0, rules: MessageRules = MessageRules(), **kwargs
    ) -> GoProResp:
        return MockWifiResponse(message.build_url(**kwargs), message.build_body(**kwargs))

    async def _stream_to_file(self, url: str, file: Path):
        return url, file

    def register_update(self, callback: UpdateCb, update: UpdateType) -> None:
        return

    def unregister_update(self, callback: UpdateCb, update: UpdateType = None) -> None:
        return

    @property
    def http_command(self) -> HttpCommands:
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        return self._api.http_setting


class DataPatch:
    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def data(self) -> Any:
        return self.value

    @property
    def ok(self) -> bool:
        return True


class MockWiredGoPro(WiredGoPro):
    def __init__(self, test_version: str) -> None:
        super().__init__(serial=None, poll_period=0.5)
        self.http_command.wired_usb_control = self._mock_empty_return
        self.http_command.get_open_gopro_api_version = self._mock_get_version
        self.http_command.get_camera_state = self._mock_get_state
        self.http_command.set_third_party_client_info = self._mock_empty_return
        self.state_response: CameraState = {}

    async def _mock_get_state(self, *args, **kwargs):
        return DataPatch(self.state_response)

    def set_state_response(self, response: CameraState):
        self.state_response = response

    async def _mock_empty_return(self, *args, **kwargs):
        return

    async def _mock_get_version(self, *args, **kwargs):
        return DataPatch("2.0")


class MockFeature(BaseFeature):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(None, None)

    async def wait_for_ready(self) -> None:
        return

    @property
    def is_ready(self) -> bool:
        return True

    def close(self) -> None:
        return


class MockFeatures:
    CohnFeature = MockFeature
    AccessPointFeature = MockFeature


class MockWirelessGoPro(WirelessGoPro):
    def __init__(self, test_version: str) -> None:
        super().__init__(
            target="device",
            ble_adapter=MockBleController,
            wifi_adapter=MockWifiController,
            enable_wifi=True,
            maintain_state=False,
        )
        self._test_version = test_version
        # TODO we need to find a way to inject these from individual tests
        self._api.ble_command.get_open_gopro_api_version = self._mock_version
        self._api.http_command.get_open_gopro_api_version = self._mock_version
        self._api.ble_command.cohn_get_certificate = self._mock_get_cohn_cohn_cert
        self._api.ble_command.get_ap_entries = self._mock_get_ap_entries
        self.http_command.set_third_party_client_info = self._mock_empty_return
        self._ble.write = self._mock_write
        self._ble._gatt_table = MockGattTable()
        self._ble._controller.disconnect = self._disconnect_handler
        self._test_response_uuid = GoProUUID.CQ_COMMAND
        self._test_response_data = bytearray()
        self.ble_status.ap_mode.get_value = self._mock_wifi_check

    async def _open_wifi(self, timeout: int = 15, retries: int = 5) -> None:
        self._api.ble_command.get_wifi_password = self._mock_password
        self._api.ble_command.get_wifi_ssid = self._mock_ssid
        await super()._open_wifi(timeout, retries)

    async def _open_ble(self, timeout: int, retries: int) -> None:
        await super()._open_ble(timeout=timeout, retries=retries)
        self._ble._gatt_table.handle2uuid = self._mock_uuid

    async def _send_ble_message(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        if response_data := kwargs.get("response_data"):
            self._test_response_data = response_data
            self._test_response_uuid = message._uuid
            global _test_response_id
            _test_response_id = message._identifier
            self._ble.write = self._mock_write
            return await super()._send_ble_message(message, **kwargs)
        else:
            return mock_good_response

    async def _read_ble_characteristic(
        self, message: BleMessage, rules: MessageRules = MessageRules(), **kwargs: Any
    ) -> GoProResp:
        raise NotImplementedError

    async def _mock_version(self) -> DataPatch:
        return DataPatch("2.0")

    async def _mock_password(self) -> DataPatch:
        return DataPatch("password")

    async def _mock_wifi_check(self) -> DataPatch:
        return DataPatch(True)

    async def _mock_ssid(self) -> DataPatch:
        return DataPatch("ssid")

    async def _mock_empty_return(self, *args, **kwargs) -> None:
        return None

    def _mock_uuid(self, _) -> BleUUID:
        return self._test_response_uuid

    async def _mock_write(self, uuid: str, data: bytearray) -> None:
        assert self._test_response_data is not None
        self._notification_handler(0, self._test_response_data)
        # for packet in self._test_response_data:
        #     self._notification_handler(0, packet)

    async def _mock_get_cohn_cohn_cert(self) -> DataPatch:
        @dataclass
        class MockCert:
            cert: str

        return DataPatch(MockCert("cert"))

    async def _mock_get_ap_entries(self) -> DataPatch:
        return DataPatch("ap_entries")

    @property
    def is_ble_connected(self) -> bool:
        return True

    @property
    def is_http_connected(self) -> bool:
        return True

    def close(self) -> None:
        pass


_test_response_id = CmdId.SET_SHUTTER


class MockGoProMaintainBle(WirelessGoPro):
    def __init__(self) -> None:
        super().__init__(
            target="device",
            ble_adapter=MockBleController,
            wifi_adapter=MockWifiController,
            enable_wifi=True,
            maintain_ble=True,
            keep_alive_interval=1,
        )
        self._test_version = "2.0"
        self._api.ble_command.get_open_gopro_api_version = self._mock_get_version
        self.ble_status.encoding.register_value_update = self._mock_register_encoding
        self.ble_status.busy.register_value_update = self._mock_register_busy
        self.ble_setting.led.set = self._mock_led_set
        self._open_wifi = self._mock_open_wifi
        self._sync_resp_ready_q.get = self._mock_q_get
        self.generic_spy: asyncio.Queue[Any] = asyncio.Queue()

    async def _mock_q_get(self, *args, **kwargs):
        return mock_good_response

    async def _mock_led_set(self, *args):
        await self.generic_spy.put(args)
        return mock_good_response

    async def _mock_open_wifi(self, *args):
        return None

    async def _mock_register_encoding(self, *args):
        return DataPatch({StatusId.ENCODING: 1})

    async def _mock_register_busy(self, *args):
        return DataPatch({StatusId.BUSY: 1})

    async def mock_handle2uuid(self, *args):
        return GoProUUID.CQ_QUERY_RESP

    async def _open_ble(self, timeout: int, retries: int) -> None:
        await super()._open_ble(timeout=timeout, retries=retries)

    async def _mock_get_version(self) -> DataPatch:
        return DataPatch("2.0")
