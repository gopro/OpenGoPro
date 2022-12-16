# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

# pylint: disable=redefined-outer-name

import re
import asyncio
import logging
from pathlib import Path
from typing import Pattern, Generic, Optional, Any
from dataclasses import dataclass, field

import pytest
from open_gopro.ble.services import CharProps

from tests import versions
from open_gopro import WirelessGoPro
from open_gopro.ble import (
    BleClient,
    BLEController,
    BleDevice,
    BleHandle,
    DisconnectHandlerType,
    NotiHandlerType,
    GattDB,
    BleUUID,
    UUIDs,
    Descriptor,
    Characteristic,
    Service,
)
from open_gopro.wifi import WifiClient, WifiController, SsidState
from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.responses import GoProResp
from open_gopro.constants import ErrorCode, ProducerType, CmdId, GoProUUIDs, ResponseType
from open_gopro.interface import GoProBle, GoProWifi
from open_gopro.api import (
    WirelessApi,
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    Params,
)
from open_gopro.exceptions import ConnectFailed, FailedToFindDevice
from open_gopro.util import setup_logging, set_logging_level

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
async def bleak_wrapper():
    ble = BleakWrapperController()
    yield ble


@pytest.fixture(scope="module")
async def bleak_client():
    def disconnected_cb(_) -> None:
        print("Entered test disconnect callback")

    def notification_cb(handle: int, data: bytearray) -> None:
        print("Entered test notification callback")

    ble = BleClient(
        BleakWrapperController(), disconnected_cb, notification_cb, target=re.compile("###invalid_device###")
    )
    ble.open(timeout=30)
    print("GoPro Bleak opened!")
    yield ble
    ble.close()


##############################################################################################################
#                                             GATT Database Unit Testing
##############################################################################################################


@pytest.fixture()
def descriptor():
    yield Descriptor(0xABCD, UUIDs.CLIENT_CHAR_CONFIG)


@pytest.fixture()
def characteristic(descriptor: Descriptor):
    yield Characteristic(2, UUIDs.ACC_APPEARANCE, CharProps.READ, init_descriptors=[descriptor])


@pytest.fixture()
def service(characteristic: Characteristic):
    yield Service(UUIDs.S_GENERIC_ACCESS, 3, init_chars=[characteristic])


@pytest.fixture()
def gatt_db(service: Service):
    yield GattDB([service])


##############################################################################################################
#                                             BLE Unit Testing
##############################################################################################################


@dataclass
class GattTable:
    def handle2uuid(self):
        ...


class BleControllerTest(BLEController, Generic[BleHandle, BleDevice]):
    # pylint: disable=signature-differs

    def __init__(self, *args, **kwargs) -> None:
        pass

    def scan(self, token: Pattern, timeout: int, service_uuids: list[BleUUID] = None) -> str:
        if token == re.compile("device"):
            return "scanned_device"
        raise FailedToFindDevice

    def read(self, handle: BleHandle, uuid: str) -> bytearray:
        return bytearray()

    def write(self, handle: BleHandle, uuid: str, data: bytearray) -> None:
        return

    def connect(self, disconnect_cb: DisconnectHandlerType, device: BleDevice, timeout: int) -> str:
        if disconnect_cb is None:
            raise ConnectFailed("forced connect fail from test", timeout, 1)
        return "connected_device"

    def pair(self, handle: BleHandle) -> None:
        return

    def enable_notifications(self, handle: BleHandle, handler: NotiHandlerType) -> None:
        return

    def discover_chars(self, handle: BleHandle, service_uuids: list[BleUUID] = None) -> GattTable:
        return GattTable()

    def disconnect(self, handle: BleHandle) -> None:
        return


def disconnection_handler(_) -> None:
    print("Entered test disconnect callback")


def notification_handler(handle: int, data: bytearray) -> None:
    print("Entered test notification callback")


@pytest.fixture(scope="module")
async def ble_client():
    test_client = BleClient(
        controller=BleControllerTest(),
        disconnected_cb=disconnection_handler,
        notification_cb=notification_handler,
        target=(re.compile("device"), []),
    )
    yield test_client


class BleCommunicatorTest(GoProBle):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str) -> None:
        super().__init__(
            BleControllerTest(), disconnection_handler, notification_handler, re.compile("target")
        )
        self._api = api_versions[test_version](self)

    def _register_listener(self, _) -> None:
        return True

    def _unregister_listener(self, _) -> None:
        return True

    def get_notification(self, timeout: float) -> int:
        return 1

    def _send_ble_message(
        self, uuid: BleUUID, data: bytearray, response_id: ResponseType, **kwargs
    ) -> GoProResp:
        response = good_response
        response._meta = [uuid]
        response._raw_packet = data
        return response

    def _read_characteristic(self, uuid: BleUUID) -> GoProResp:
        response = good_response
        response._meta = [uuid]
        return response

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
async def ble_communicator(request):
    test_client = BleCommunicatorTest(request.param)
    yield test_client


##############################################################################################################
#                                             WiFi Unit Testing
##############################################################################################################


class WifiControllerTest(WifiController):
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
async def wifi_client():
    test_client = WifiClient(controller=WifiControllerTest())
    yield test_client


@dataclass
class DummyWifiResponse:
    url: str
    _meta: list = field(default_factory=list)


class WifiCommunicatorTest(GoProWifi):
    # pylint: disable=signature-differs

    def __init__(self, test_version: str):
        super().__init__(WifiControllerTest())
        self._api = api_versions[test_version](self)

    def _get(self, url: str, _=None, **kwargs):
        return DummyWifiResponse(url)

    def _stream_to_file(self, url: str, file: Path):
        return url, file

    @property
    def http_command(self) -> HttpCommands:
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        return self._api.http_setting


@pytest.fixture(scope="module", params=versions)
async def wifi_communicator(request):
    test_client = WifiCommunicatorTest(request.param)
    yield test_client


##############################################################################################################
#                                             GoPro Unit Testing
##############################################################################################################


@dataclass
class Version:
    major: int
    minor: int


class FlattenPatch:
    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def flatten(self) -> Any:
        return self.value


good_response = GoProResp(meta=["test_response"], status=ErrorCode.SUCCESS)

_test_response_id = CmdId.SET_SHUTTER


def _test_parse(self: GoProResp) -> None:
    self._state = GoProResp._State.PARSED
    self._meta = [_test_response_id]


class GoProTest(WirelessGoPro):
    def __init__(self, test_version: str) -> None:
        super().__init__(
            target=re.compile("device"),
            ble_adapter=BleControllerTest,
            wifi_adapter=WifiControllerTest,
            enable_wifi=True,
            maintain_state=False,
        )
        self._test_version = test_version
        self._api.ble_command.get_open_gopro_api_version = self._test_return_version
        self._ble.write = self._test_write
        self._ble._controller.disconnect = self._disconnect_handler
        self._test_response_uuid = GoProUUIDs.CQ_COMMAND
        self._test_response_data = bytearray()

    def _open_wifi(self, timeout: int = 15, retries: int = 5) -> None:
        self._api.ble_command.get_wifi_password = self._test_return_password
        super()._open_wifi(timeout, retries)

    def _open_ble(self, timeout: int, retries: int) -> None:
        super()._open_ble(timeout=timeout, retries=retries)
        self._ble._gatt_table.handle2uuid = self._test_return_uuid

    def _send_ble_message(
        self,
        uuid: BleUUID,
        data: bytearray,
        response_id: ResponseType,
        response_data: list[bytearray] = None,
        response_uuid: BleUUID = None,
        **kwargs
    ) -> GoProResp:
        if response_uuid is None:
            return good_response
        else:
            self._test_response_data = response_data
            self._test_response_uuid = response_uuid
            global _test_response_id
            _test_response_id = response_id
            self._ble.write = self._test_write
            return super()._send_ble_message(uuid, data, response_id)

    def _test_return_version(self) -> FlattenPatch:
        return FlattenPatch(Version(*[int(x) for x in self._test_version.split(".")]))

    def _test_return_password(self) -> FlattenPatch:
        return FlattenPatch("password")

    def _test_return_uuid(self, _) -> BleUUID:
        return self._test_response_uuid

    def _test_write(self, uuid: str, data: bytearray) -> None:
        assert self._test_response_data is not None
        for packet in self._test_response_data:
            self._notification_handler(0, packet)

    @property
    def is_ble_connected(self) -> bool:
        return True

    @property
    def is_http_connected(self) -> bool:
        return True


@pytest.fixture(scope="module", params=versions)
async def gopro_client(request):
    original_parse = GoProResp._parse
    GoProResp._parse = _test_parse
    test_client = GoProTest(request.param)
    yield test_client
    GoProResp._parse = original_parse


class GoProTestMaintainBle(WirelessGoPro):
    def __init__(self) -> None:
        super().__init__(
            target=re.compile("device"),
            ble_adapter=BleControllerTest,
            wifi_adapter=WifiControllerTest,
            enable_wifi=True,
            maintain_ble=True,
        )
        self._test_version = "2.0"
        self._api.ble_command.get_open_gopro_api_version = self._test_return_version
        self.ble_status.encoding_active.register_value_update = lambda *args: None
        self.ble_status.system_ready.register_value_update = lambda *args: None
        self.keep_alive = lambda *args: True
        self._open_wifi = lambda *args: None
        self._sync_resp_ready_q.get = lambda *args, **kwargs: good_response

    def _open_ble(self, timeout: int, retries: int) -> None:
        super()._open_ble(timeout=timeout, retries=retries)
        self._ble._gatt_table.handle2uuid = lambda *args: GoProUUIDs.CQ_QUERY_RESP

    def _test_return_version(self) -> FlattenPatch:
        return FlattenPatch(Version(*[int(x) for x in self._test_version.split(".")]))


@pytest.fixture(scope="function")
async def gopro_client_maintain_ble():
    test_client = GoProTestMaintainBle()
    yield test_client
