# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jan  5 23:22:12 UTC 2022

# pylint: disable=wrong-import-position

from typing import Awaitable, Callable, Any
import logging

from bleak.backends.characteristic import BleakGATTCharacteristic

from rich.logging import RichHandler
from rich import traceback

logger: logging.Logger = logging.getLogger("tutorial_logger")
sh = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
sh.setFormatter(stream_formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

bleak_logger = logging.getLogger("bleak")
bleak_logger.setLevel(logging.WARNING)
bleak_logger.addHandler(sh)

traceback.install()  # Enable exception tracebacks in rich logger

GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"
GOPRO_BASE_URL = "http://10.5.5.9:8080"

noti_handler_T = Callable[[BleakGATTCharacteristic, bytearray], Awaitable[None]]

from tutorial_modules.tutorial_1_connect_ble.ble_connect import connect_ble
from tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import GoProUuid
from tutorial_modules.tutorial_3_parse_ble_tlv_responses.ble_command_get_hardware_info import Response, TlvResponse
from tutorial_modules.tutorial_4_ble_queries.ble_query_poll_resolution_value import QueryResponse, Resolution
from tutorial_modules.tutorial_6_connect_wifi.enable_wifi_ap import enable_wifi
from tutorial_modules.tutorial_7_send_wifi_commands.wifi_command_get_media_list import get_media_list
from tutorial_modules.tutorial_5_ble_protobuf import proto
from tutorial_modules.tutorial_5_ble_protobuf.set_turbo_mode import ProtobufResponse
from tutorial_modules.tutorial_5_ble_protobuf.decipher_response import ResponseManager
from tutorial_modules.tutorial_6_connect_wifi.connect_as_sta import connect_to_access_point
