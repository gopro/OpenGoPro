# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

# pylint: disable=redefined-outer-name

import asyncio
import logging
import re
from pathlib import Path
from typing import Any, Generator

import pytest

from open_gopro.api import WirelessApi
from open_gopro.ble import BleClient, Characteristic, Descriptor, GattDB, Service, UUIDs
from open_gopro.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.ble.services import CharProps
from open_gopro.gopro_base import GoProBase
from open_gopro.logger import set_logging_level, setup_logging
from open_gopro.wifi import WifiClient
from tests import versions
from tests.mocks import (
    MockBleCommunicator,
    MockBleController,
    MockGoProMaintainBle,
    MockWifiCommunicator,
    MockWifiController,
    MockWiredGoPro,
    MockWirelessGoPro,
)

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
        BleakWrapperController(),
        disconnected_cb,
        notification_cb,
        target=re.compile("###invalid_device###"),  # type: ignore
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
def mock_characteristic(mock_descriptor: Descriptor) -> Generator[Characteristic, Any, None]:
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


def disconnection_handler(_) -> None:
    print("Entered test disconnect callback")


async def notification_handler(handle: int, data: bytearray) -> None:
    print("Entered test notification callback")


@pytest.fixture(scope="module")
async def mock_ble_client():
    test_client = BleClient(
        controller=MockBleController(),
        disconnected_cb=disconnection_handler,
        notification_cb=notification_handler,  # type: ignore
        target=(re.compile("device"), []),
    )
    yield test_client


@pytest.fixture(scope="module", params=versions)
async def mock_ble_communicator(request):
    test_client = MockBleCommunicator(request.param)
    yield test_client


##############################################################################################################
#                                             WiFi Unit Testing
##############################################################################################################


@pytest.fixture(scope="module")
async def mock_wifi_client():
    test_client = WifiClient(controller=MockWifiController())
    yield test_client


@pytest.fixture(scope="module", params=versions)
async def mock_wifi_communicator(request):
    test_client = MockWifiCommunicator(request.param)
    yield test_client


##############################################################################################################
#                                             GoPro Unit Testing
##############################################################################################################


@pytest.fixture(scope="function")
async def mock_wired_gopro():
    test_client = MockWiredGoPro("2.0")
    yield test_client


@pytest.fixture(params=versions)
async def mock_wireless_gopro_basic(request):
    test_client = MockWirelessGoPro(request.param)
    GoProBase.HTTP_GET_RETRIES = 1  # type: ignore
    yield test_client
    test_client.close()


@pytest.fixture(scope="function")
async def mock_wireless_gopro():
    test_client = MockGoProMaintainBle()
    yield test_client
