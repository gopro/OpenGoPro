# uuids.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 20 23:24:52 UTC 2025

"""UUID-related constants"""

from dataclasses import dataclass
from typing import Final

from open_gopro.network.ble import BleUUID, UUIDs

GOPRO_BASE_UUID: Final = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"


@dataclass(frozen=True)
class GoProUUID(UUIDs):
    """GoPro Proprietary BleUUID's."""

    # GoPro Wifi Access Point Service
    S_WIFI_ACCESS_POINT = BleUUID("Wifi Access Point Service", hex=GOPRO_BASE_UUID.format("0001"))
    WAP_SSID = BleUUID("Wifi AP SSID", hex=GOPRO_BASE_UUID.format("0002"))
    WAP_PASSWORD = BleUUID("Wifi AP Password", hex=GOPRO_BASE_UUID.format("0003"))
    WAP_POWER = BleUUID("Wifi Power", hex=GOPRO_BASE_UUID.format("0004"))
    WAP_STATE = BleUUID("Wifi State", hex=GOPRO_BASE_UUID.format("0005"))
    WAP_CSI_PASSWORD = BleUUID("CSI Password", hex=GOPRO_BASE_UUID.format("0006"))

    # GoPro Control & Query Service
    S_CONTROL_QUERY = BleUUID("Control and Query Service", hex="0000fea6-0000-1000-8000-00805f9b34fb")
    CQ_COMMAND = BleUUID("Command", hex=GOPRO_BASE_UUID.format("0072"))
    CQ_COMMAND_RESP = BleUUID("Command Response", hex=GOPRO_BASE_UUID.format("0073"))
    CQ_SETTINGS = BleUUID("Settings", hex=GOPRO_BASE_UUID.format("0074"))
    CQ_SETTINGS_RESP = BleUUID("Settings Response", hex=GOPRO_BASE_UUID.format("0075"))
    CQ_QUERY = BleUUID("Query", hex=GOPRO_BASE_UUID.format("0076"))
    CQ_QUERY_RESP = BleUUID("Query Response", hex=GOPRO_BASE_UUID.format("0077"))
    CQ_SENSOR = BleUUID("Sensor", hex=GOPRO_BASE_UUID.format("0078"))
    CQ_SENSOR_RESP = BleUUID("Sensor Response", hex=GOPRO_BASE_UUID.format("0079"))

    # GoPro Camera Management Service
    S_CAMERA_MANAGEMENT = BleUUID("Camera Management Service", hex=GOPRO_BASE_UUID.format("0090"))
    CM_NET_MGMT_COMM = BleUUID("Camera Management", hex=GOPRO_BASE_UUID.format("0091"))
    CN_NET_MGMT_RESP = BleUUID("Camera Management Response", hex=GOPRO_BASE_UUID.format("0092"))

    # Unknown
    S_INTERNAL = BleUUID("Unknown Service", hex=GOPRO_BASE_UUID.format("0080"))
    INTERNAL_81 = BleUUID("Internal 81", hex=GOPRO_BASE_UUID.format("0081"))
    INTERNAL_82 = BleUUID("Internal 82", hex=GOPRO_BASE_UUID.format("0082"))
    INTERNAL_83 = BleUUID("Internal 83", hex=GOPRO_BASE_UUID.format("0083"))
    INTERNAL_84 = BleUUID("Internal 84", hex=GOPRO_BASE_UUID.format("0084"))
