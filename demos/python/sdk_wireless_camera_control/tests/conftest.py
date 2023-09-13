# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

# pylint: disable=redefined-outer-name

import asyncio
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, Optional, Pattern

import pytest

from open_gopro import WiredGoPro, WirelessGoPro, types
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WirelessApi,
)
from open_gopro.ble import (
    BleClient,
    BLEController,
    BleDevice,
    BleHandle,
    BleUUID,
    Characteristic,
    Descriptor,
    DisconnectHandlerType,
    GattDB,
    NotiHandlerType,
    Service,
    UUIDs,
)
from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.ble.services import CharProps
from open_gopro.communicator_interface import GoProBle, GoProWifi
from open_gopro.constants import CmdId, ErrorCode, GoProUUIDs, StatusId
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice
from open_gopro.logger import set_logging_level, setup_logging
from open_gopro.models.response import GoProResp
from open_gopro.wifi import SsidState, WifiClient, WifiController
from tests import mock_good_response, versions

api_versions = {"2.0": WirelessApi}

##############################################################################################################
#                                             Log Management
##############################################################################################################

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    global logger
    logger = setup_logging(logger)
    set_logging_level(logging.ERROR)


@pytest.fixture(scope="module", autouse=True)
def manage_logs(request):
    top_dir_stripped = Path(*Path(request.node.name).parts[1:])
    extension_changed = Path(str(top_dir_stripped).strip(".py") + ".log")
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(
        Path(".reports") / "logs" / extension_changed
    )


@pytest.fixture(scope="function", autouse=True)
def test_log(request):
    logging.debug("################################################################################")
    logging.debug("Test '{}' STARTED".format(request.node.nodeid))
    logging.debug("################################################################################")


##############################################################################################################
#                                             General
##############################################################################################################


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


##############################################################################################################
#                                             Bleak Unit Testing
##############################################################################################################


@pytest.fixture(scope="module")
async def mock_bleak_wrapper():
    ble = BleakWrapperController()
    yield ble


@pytest.fixture(scope="module")
async def mock_bleak_client():
    def disconnected_cb(_) -> None:
        print("Entered test disconnect callback")

    def notification_cb(handle: int, data: bytearray) -> None:
        print("Entered test notification callback")

    ble = BleClient(
        BleakWrapperController(), disconnected_cb, notification_cb, target=re.compile("###invalid_device###")
    )
    await ble.open(timeout=30)
    print("GoPro Bleak opened!")
    yield ble
    await ble.close()


##############################################################################################################
#                                             GATT Database Unit Testing
##############################################################################################################


@pytest.fixture()
def mock_descriptor():
    yield Descriptor(0xABCD, UUIDs.CLIENT_CHAR_CONFIG)


@pytest.fixture()
def mock_characteristic(mock_descriptor: Descriptor):
    yield Characteristic(2, UUIDs.ACC_APPEARANCE, CharProps.READ, init_descriptors=[mock_descriptor])


@pytest.fixture()
def mock_service(mock_characteristic: Characteristic):
    yield Service(UUIDs.S_GENERIC_ACCESS, 3, init_chars=[mock_characteristic])


@pytest.fixture()
def mock_gatt_db(mock_service: Service):
    yield GattDB([mock_service])


##############################################################################################################
#                                             BLE Unit Testing
##############################################################################################################


@dataclass
class MockGattTable:
    def handle2uuid(self, *args):
        return GoProUUIDs.CQ_QUERY_RESP


class MockBleController(BLEController, Generic[BleHandle, BleDevice]):
    # pylint: disable=signature-differs

    def __init__(self, *args, **kwargs) -> None:
        self.gatt_db = MockGattTable()

    async def scan(self, token: Pattern, timeout: int, service_uuids: list[BleUUID] = None) -> str:
        if token == re.compile("device"):
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


@pytest.fixture(scope="module")
async def mock_ble_client():
    test_client = BleClient(
        controller=MockBleController(),
        disconnected_cb=disconnection_handler,
        notification_cb=notification_handler,
        target=(re.compile("device"), []),
    )
    yield test_client


class MockBleCommunicator(GoProBle):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str) -> None:
        super().__init__(MockBleController(), disconnection_handler, notification_handler, re.compile("target"))
        self._api = api_versions[test_version](self)

    def register_update(self, callback: types.UpdateCb, update: types.UpdateType) -> None:
        return

    def unregister_update(self, callback: types.UpdateCb, update: types.UpdateType = None) -> None:
        return

    async def _send_ble_message(
        self, uuid: BleUUID, data: bytearray, response_id: types.ResponseType, **kwargs
    ) -> dict:
        return dict(uuid=uuid, packet=data)

    async def _read_characteristic(self, uuid: BleUUID) -> dict:
        return dict(uuid=uuid)

    @property
    def ble_command(self) -> BleCommands:
        return self._api.ble_command

    @property
    def ble_setting(self) -> BleSettings:
        return self._api.ble_setting

    @property
    def ble_status(self) -> BleStatuses:
        return self._api.ble_status


@pytest.fixture(scope="module", params=versions)
async def mock_ble_communicator(request):
    test_client = MockBleCommunicator(request.param)
    yield test_client


##############################################################################################################
#                                             WiFi Unit Testing
##############################################################################################################


class MockWifiController(WifiController):
    # pylint: disable=signature-differs

    def __init__(self, interface: Optional[str] = None, password: Optional[str] = None) -> None:
        ...

    def connect(self, ssid: str, password: str, timeout: float) -> bool:
        return True if password == "password" else False

    def disconnect(self) -> bool:
        return True

    def current(self) -> tuple[Optional[str], SsidState]:
        return "current_ssid", SsidState.CONNECTED

    def available_interfaces(self) -> list[str]:
        return ["interface1", "interface2"]

    def power(self, power: bool) -> None:
        return

    def is_on(self) -> bool:
        return True


@pytest.fixture(scope="module")
async def mock_wifi_client():
    test_client = WifiClient(controller=MockWifiController())
    yield test_client


@dataclass
class MockWifiResponse:
    url: str


class MockWifiCommunicator(GoProWifi):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str):
        super().__init__(MockWifiController())
        self._api = api_versions[test_version](self)

    async def _http_get(self, url: str, _=None, **kwargs):
        return MockWifiResponse(url)

    async def _stream_to_file(self, url: str, file: Path):
        return url, file

    def register_update(self, callback: types.UpdateCb, update: types.UpdateType) -> None:
        return

    def unregister_update(self, callback: types.UpdateCb, update: types.UpdateType = None) -> None:
        return

    @property
    def http_command(self) -> HttpCommands:
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        return self._api.http_setting


@pytest.fixture(scope="module", params=versions)
async def mock_wifi_communicator(request):
    test_client = MockWifiCommunicator(request.param)
    yield test_client


##############################################################################################################
#                                             GoPro Unit Testing
##############################################################################################################


class DataPatch:
    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def data(self) -> Any:
        return self.value


class MockWiredGoPro(WiredGoPro):
    def __init__(self, test_version: str) -> None:
        super().__init__(serial=None, poll_period=0.5)
        self.http_command.wired_usb_control = self._mock_wired_usb_control
        self.http_command.get_open_gopro_api_version = self._mock_get_version
        self.http_command.get_camera_state = self._mock_get_state
        self.state_response: types.CameraState = {}

    async def _mock_get_state(self, *args, **kwargs):
        return DataPatch(self.state_response)

    def set_state_response(self, response: types.CameraState):
        self.state_response = response

    async def _mock_wired_usb_control(self, *args, **kwargs):
        return

    async def _mock_get_version(self, *args, **kwargs):
        return DataPatch("2.0")


@pytest.fixture(scope="function")
async def mock_wired_gopro():
    test_client = MockWiredGoPro("2.0")
    yield test_client


class MockWirelessGoPro(WirelessGoPro):
    def __init__(self, test_version: str) -> None:
        super().__init__(
            target=re.compile("device"),
            ble_adapter=MockBleController,
            wifi_adapter=MockWifiController,
            enable_wifi=True,
            maintain_state=False,
        )
        self._test_version = test_version
        self._api.ble_command.get_open_gopro_api_version = self._mock_version
        self._ble.write = self._mock_write
        self._ble._gatt_table = MockGattTable()
        self._ble._controller.disconnect = self._disconnect_handler
        self._test_response_uuid = GoProUUIDs.CQ_COMMAND
        self._test_response_data = bytearray()

    async def _open_wifi(self, timeout: int = 15, retries: int = 5) -> None:
        self._api.ble_command.get_wifi_password = self._mock_password
        self._api.ble_command.get_wifi_ssid = self._mock_ssid
        await super()._open_wifi(timeout, retries)

    async def _open_ble(self, timeout: int, retries: int) -> None:
        await super()._open_ble(timeout=timeout, retries=retries)
        self._ble._gatt_table.handle2uuid = self._mock_uuid

    async def _send_ble_message(
        self,
        uuid: BleUUID,
        data: bytearray,
        response_id: types.ResponseType,
        response_data: list[bytearray] = None,
        response_uuid: BleUUID = None,
        **kwargs
    ) -> GoProResp:
        if response_uuid is None:
            return mock_good_response
        else:
            self._test_response_data = response_data
            self._test_response_uuid = response_uuid
            global _test_response_id
            _test_response_id = response_id
            self._ble.write = self._mock_write
            return await super()._send_ble_message(uuid, data, response_id)

    async def _mock_version(self) -> DataPatch:
        return DataPatch("2.0")

    async def _mock_password(self) -> DataPatch:
        return DataPatch("password")

    async def _mock_ssid(self) -> DataPatch:
        return DataPatch("ssid")

    def _mock_uuid(self, _) -> BleUUID:
        return self._test_response_uuid

    async def _mock_write(self, uuid: str, data: bytearray) -> None:
        assert self._test_response_data is not None
        for packet in self._test_response_data:
            self._notification_handler(0, packet)

    @property
    def is_ble_connected(self) -> bool:
        return True

    @property
    def is_http_connected(self) -> bool:
        return True

    def close(self) -> None:
        pass


_test_response_id = CmdId.SET_SHUTTER


# TODO use mocking library instead of doing this manually?
@pytest.fixture(params=versions)
async def mock_wireless_gopro_basic(request):
    test_client = MockWirelessGoPro(request.param)
    yield test_client
    test_client.close()


class MockGoProMaintainBle(WirelessGoPro):
    def __init__(self) -> None:
        super().__init__(
            target=re.compile("device"),
            ble_adapter=MockBleController,
            wifi_adapter=MockWifiController,
            enable_wifi=True,
            maintain_ble=True,
        )
        self._test_version = "2.0"
        self._api.ble_command.get_open_gopro_api_version = self._mock_get_version
        self.ble_status.encoding_active.register_value_update = self._mock_register_encoding
        self.ble_status.system_busy.register_value_update = self._mock_register_busy
        self.ble_setting.led.set = self._mock_led_set
        self._open_wifi = self._mock_open_wifi
        self._sync_resp_ready_q.get = self._mock_q_get

    async def _mock_q_get(self, *args, **kwargs):
        return mock_good_response

    async def _mock_led_set(self, *args):
        return mock_good_response

    async def _mock_open_wifi(self, *args):
        return None

    async def _mock_register_encoding(self, *args):
        return DataPatch({StatusId.ENCODING: 1})

    async def _mock_register_busy(self, *args):
        return DataPatch({StatusId.SYSTEM_BUSY: 1})

    async def mock_handle2uuid(self, *args):
        return GoProUUIDs.CQ_QUERY_RESP

    async def _open_ble(self, timeout: int, retries: int) -> None:
        await super()._open_ble(timeout=timeout, retries=retries)

    async def _mock_get_version(self) -> DataPatch:
        return DataPatch("2.0")


@pytest.fixture(scope="function")
async def mock_wireless_gopro():
    test_client = MockGoProMaintainBle()
    yield test_client
