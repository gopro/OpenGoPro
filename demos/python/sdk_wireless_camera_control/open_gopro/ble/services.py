# services.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Objects to nicely interact with BLE services, characteristics, and attributes."""

import json
import enum
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Union


GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"

# TODO this is temporary. Really UUID should be a data structure and we pass in the values
# of these UUID's from the application
class UUID(enum.Enum):
    """BLE UUID."""

    # Generic Attribute Service
    S_GENERIC_ATT = "00001801-0000-1000-8000-00805f9b34fb"

    # Generic Access Service
    S_GENERIC_ACCESS = "00001800-0000-1000-8000-00805f9b34fb"
    ACC_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
    ACC_APPEARANCE = "00002a01-0000-1000-8000-00805f9b34fb"
    ACC_PREF_CONN_PARAMS = "00002a04-0000-1000-8000-00805f9b34fb"
    ACC_CENTRAL_ADDR_RES = "00002aa6-0000-1000-8000-00805f9b34fb"

    # Tx Power
    S_TX_POWER = "00001804-0000-1000-8000-00805f9b34fb"
    TX_POWER_LEVEL = "00002a07-0000-1000-8000-00805f9b34fb"

    # Battery Service
    S_BATTERY = "0000180f-0000-1000-8000-00805f9b34fb"
    BATT_LEVEL = "00002a19-0000-1000-8000-00805f9b34fb"

    # Device Information Service
    S_DEV_INFO = "0000180a-0000-1000-8000-00805f9b34fb"
    INF_MAN_NAME = "00002a29-0000-1000-8000-00805f9b34fb"
    INF_MODEL_NUM = "00002a24-0000-1000-8000-00805f9b34fb"
    INF_SERIAL_NUM = "00002a25-0000-1000-8000-00805f9b34fb"
    INF_FW_REV = "00002a26-0000-1000-8000-00805f9b34fb"
    INF_HW_REV = "00002a27-0000-1000-8000-00805f9b34fb"
    INF_SW_REV = "00002a28-0000-1000-8000-00805f9b34fb"
    INF_SYS_ID = "00002a23-0000-1000-8000-00805f9b34fb"
    INF_CERT_DATA = "00002a2a-0000-1000-8000-00805f9b34fb"
    INF_PNP_ID = "00002a50-0000-1000-8000-00805f9b34fb"

    # GoPro Wifi Access Point Service
    S_WIFI_ACCESS_POINT = GOPRO_BASE_UUID.format("0001")
    WAP_SSID = GOPRO_BASE_UUID.format("0002")
    WAP_PASSWORD = GOPRO_BASE_UUID.format("0003")
    WAP_POWER = GOPRO_BASE_UUID.format("0004")
    WAP_STATE = GOPRO_BASE_UUID.format("0005")
    WAP_CSI_PASSWORD = GOPRO_BASE_UUID.format("0006")

    # GoPro Control & Query Service
    S_CONTROL_QUERY = "0000fea6-0000-1000-8000-00805f9b34fb"
    CQ_COMMAND = GOPRO_BASE_UUID.format("0072")
    CQ_COMMAND_RESP = GOPRO_BASE_UUID.format("0073")
    CQ_SETTINGS = GOPRO_BASE_UUID.format("0074")
    CQ_SETTINGS_RESP = GOPRO_BASE_UUID.format("0075")
    CQ_QUERY = GOPRO_BASE_UUID.format("0076")
    CQ_QUERY_RESP = GOPRO_BASE_UUID.format("0077")
    CQ_SENSOR = GOPRO_BASE_UUID.format("0078")
    CQ_SENSOR_RESP = GOPRO_BASE_UUID.format("0079")

    # GoPro Camera Management Service
    S_CAMERA_MANAGEMENT = GOPRO_BASE_UUID.format("0090")
    CM_NET_MGMT_COMM = GOPRO_BASE_UUID.format("0091")
    CN_NET_MGMT_RESP = GOPRO_BASE_UUID.format("0092")

    # Unknown
    S_UNKNOWN = GOPRO_BASE_UUID.format("0080")
    INTERNAL_81 = GOPRO_BASE_UUID.format("0081")
    INTERNAL_82 = GOPRO_BASE_UUID.format("0082")
    INTERNAL_83 = GOPRO_BASE_UUID.format("0083")
    INTERNAL_84 = GOPRO_BASE_UUID.format("0084")


def get_gopro_desc(uuid: str) -> Union[UUID, str]:
    """Attempt to retrieve a the name of a UUID from it's value.

    Args:
        uuid (str): string representation of UUID

    Returns:
        Union[UUID, str]: a UUID object if success, otherwise just the input string
    """
    try:
        return UUID(uuid.lower()).name
    except ValueError:
        return uuid


@dataclass
class Descriptor:
    """A charactersistic descriptor.

    Args:
        handle (int) : the handle of the attribute table that the descriptor resides at
        value (bytes) : the byte stream value of the descriptor
    """

    handle: int
    value: bytes

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return json.dumps(asdict(self), indent=4, default=str)


@dataclass
class Characteristic:
    """A BLE charactersistic.

    Args:
        handle (int) : the handle of the attribute table that the characteristic resides at
        uuid (UUID) : the UUID of the characteristic
        props (List[str]) : the characteristic's properties (READ, WRITE, NOTIFY, etc)
        name (str) : the characteristic's name
        value (bytes) : the byte stream value of the characteristic value
        descriptors (List[Descriptor], optional) : Any relevant descriptors if they exist
    """

    handle: int
    uuid: UUID
    props: List[str]
    name: str
    value: bytes
    descriptors: List[Descriptor] = field(default_factory=list)

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return json.dumps(asdict(self), indent=4, default=str)


@dataclass
class Service:
    """A BLE service or grouping of Characteristics.

    Args:
        uuid (UUID) : the service's UUID
        name (str) : the service's name
        chars (Dict[str, Characteristic]) : the dictionary of characteristics, indexed by name
    """

    uuid: UUID
    name: str
    chars: Dict[UUID, Characteristic] = field(default_factory=dict)


class AttributeTable:
    """The attribute table to store / look up BLE services, characteristics, and attributes.

    Args:
        services (Dict[UUID, Service]): A dictionary of Services indexed by UUID..
    """

    def __init__(self, services: Dict[UUID, Service]) -> None:
        self.services = services

    def handle2uuid(self, handle: int) -> UUID:
        """Get a UUID from a handle.

        Args:
            handle (int): the handle to search for

        Raises:
            Exception: No characteristic was found at this handle

        Returns:
            UUID: The found UUID
        """
        for s in self.services.values():
            for c in s.chars.values():
                if c.handle == handle:
                    return c.uuid
        raise Exception(f"Matching UUID not found for handle {handle}")
