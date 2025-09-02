# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

# pylint: disable=redefined-outer-name

import logging
import os
import re
from pathlib import Path
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio

from open_gopro import WirelessGoPro
from open_gopro.gopro_base import GoProBase
from open_gopro.gopro_wired import WiredGoPro
from open_gopro.models.constants import settings
from open_gopro.network.ble import (
    BleClient,
    Characteristic,
    Descriptor,
    GattDB,
    Service,
    UUIDs,
)
from open_gopro.network.ble.adapters.bleak_wrapper import BleakWrapperController
from open_gopro.network.ble.services import CharProps
from open_gopro.network.wifi import WifiClient
from open_gopro.util.logger import set_logging_level, setup_logging
from tests.mocks import (
    MockBleCommunicator,
    MockBleController,
    MockFeature,
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
    if top_dir_stripped == Path("."):
        top_dir_stripped = Path(request.node.name)
    extension_changed = Path(str(top_dir_stripped).strip(".py") + ".log")
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(
        Path(".reports") / "logs" / extension_changed
    )


@pytest.fixture(scope="function", autouse=True)
def test_log(request):
    logging.debug("################################################################################")
    logging.debug("Test '{}' STARTED".format(request.node.nodeid))
    logging.debug("################################################################################")


# TODO. I think this is a bug in pytest-cov.
@pytest.fixture(scope="function", autouse=True)
def ignore_coroutine_never_awaited_warning():
    import warnings

    warnings.filterwarnings("ignore", message="coroutine 'enforce_message_rules' was never awaited")
    yield


##############################################################################################################
#                                             Bleak Unit Testing
##############################################################################################################


@pytest_asyncio.fixture(scope="function")
async def mock_bleak_wrapper():
    ble = BleakWrapperController()
    yield ble


@pytest_asyncio.fixture(scope="function")
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


def notification_handler(handle: int, data: bytearray) -> None:
    print("Entered test notification callback")


@pytest_asyncio.fixture(scope="function")
async def mock_ble_client():
    test_client = BleClient(
        controller=MockBleController(),
        disconnected_cb=disconnection_handler,
        notification_cb=notification_handler,  # type: ignore
        target=("device", []),
    )
    yield test_client


@pytest_asyncio.fixture(scope="function")
async def mock_ble_communicator(request):
    test_client = MockBleCommunicator("2.0")
    yield test_client


##############################################################################################################
#                                             WiFi Unit Testing
##############################################################################################################


@pytest_asyncio.fixture(scope="function")
async def mock_wifi_client():
    test_client = WifiClient(controller=MockWifiController())
    yield test_client


@pytest_asyncio.fixture(scope="function")
async def mock_wifi_communicator(request):
    test_client = MockWifiCommunicator("2.0")
    yield test_client


##############################################################################################################
#                                             GoPro Unit Testing
##############################################################################################################


@pytest_asyncio.fixture(scope="function")
async def mock_wired_gopro():
    test_client = MockWiredGoPro("2.0")
    yield test_client


def mock_features(monkeypatch):
    monkeypatch.setattr("open_gopro.features.AccessPointFeature", MockFeature)
    monkeypatch.setattr("open_gopro.features.CohnFeature", MockFeature)
    monkeypatch.setattr("open_gopro.features.StreamFeature", MockFeature)


@pytest_asyncio.fixture(scope="function")
async def mock_wireless_gopro_basic(monkeypatch):
    mock_features(monkeypatch)
    test_client = MockWirelessGoPro("2.0")
    GoProBase.HTTP_GET_RETRIES = 1  # type: ignore
    try:
        yield test_client
        await test_client.close()
    except Exception as e:
        logger.error(f"PYTEST Error closing GoPro: {e}")


@pytest_asyncio.fixture(scope="function")
async def mock_wireless_gopro(monkeypatch):
    mock_features(monkeypatch)
    test_client = MockGoProMaintainBle()
    try:
        yield test_client
        await test_client.close()
    except Exception as e:
        logger.error(f"PYTEST Error closing GoPro: {e}")


##############################################################################################################
#                                             E2E fixtures
##############################################################################################################


@pytest_asyncio.fixture(loop_scope="function")
async def wireless_gopro_ble():
    set_logging_level(logging.DEBUG)

    os.environ["LANG"] = "en_US"
    async with WirelessGoPro(interfaces={WirelessGoPro.Interface.BLE}) as gopro:
        logger.critical("==================================================================")
        logger.critical("Yielding gopro under test.")
        logger.critical("==================================================================")
        yield gopro


@pytest.fixture(scope="function")
async def wired_gopro() -> AsyncGenerator[WiredGoPro, None]:
    async with WiredGoPro() as gopro:
        logger.critical("==================================================================")
        logger.critical("Yielding gopro under test.")
        logger.critical("==================================================================")
        yield gopro
