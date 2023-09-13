# services.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Objects to nicely interact with BLE services, characteristics, and attributes."""

from __future__ import annotations

import csv
import json
import logging
import uuid
from dataclasses import InitVar, asdict, dataclass
from enum import IntEnum, IntFlag
from pathlib import Path
from typing import (
    Any,
    Final,
    Generator,
    Iterator,
    Mapping,
    Optional,
    Union,
    no_type_check,
)

logger = logging.getLogger(__name__)

BLE_BASE_UUID: Final = "0000{}-0000-1000-8000-00805F9B34FB"


class CharProps(IntFlag):
    """BLE Spec-Defined Characteristic Property bitmask values"""

    NONE = 0x00
    BROADCAST = 0x01
    READ = 0x02
    WRITE_NO_RSP = 0x04
    WRITE_YES_RSP = 0x08
    NOTIFY = 0x10
    INDICATE = 0x20
    AUTH_SIGN_WRITE = 0x40
    EXTENDED = 0x80
    NOTIFY_ENCRYPTION_REQ = 0x100
    INDICATE_ENCRYPTION_REQ = 0x200


class SpecUuidNumber(IntEnum):
    """BLE Spec-Defined BleUUID Number values as ints"""

    PRIMARY_SERVICE = 0x2800
    SECONDARY_SERVICE = 0x2801
    INCLUDE = 0x2802
    CHAR_DECLARATION = 0x2803
    CHAR_EXTENDED_PROPS = 0x2900
    CHAR_USER_DESCR = 0x2901
    CLIENT_CHAR_CONFIG = 0x2902
    SERVER_CHAR_CONFIG = 0x2903
    CHAR_FORMAT = 0x2904
    CHAR_AGGREGATE_FORMAT = 0x2905


class BleUUID(uuid.UUID):
    """An extension of the standard UUID to associate a string name with the UUID and allow 8-bit UUID input

    Can only be initialized with one of [hex, bytes, bytes_le, int]
    """

    class Format(IntEnum):
        """Used to specify 8-bit or 128-bit UUIDs"""

        BIT_16 = 2
        BIT_128 = 16

    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        format: BleUUID.Format = Format.BIT_128,
        hex: Optional[str] = None,
        bytes: Optional[bytes] = None,
        bytes_le: Optional[bytes] = None,
        int: Optional[int] = None,
    ) -> None:
        """Constructor

        Args:
            name (str): human readable name
            format (BleUUID.Format, Optional): 16 or 128 bit format. Defaults to BleUUID.Format.BIT_128.
            hex (str, Optional): build from hex string. Defaults to None.
            bytes (bytes, Optional): build from big-endian bytes. Defaults to None.
            bytes_le (bytes, Optional): build from little-endian bytes. Defaults to None.
            int (int, Optional): build from int. Defaults to None.

        Raises:
            ValueError: Attempt to initialize with more than one option
            ValueError: Badly formed input
        """
        self.name: str
        if format is BleUUID.Format.BIT_16:
            if [hex, bytes, bytes_le, int].count(None) != 3:
                raise ValueError("Only one of [hex, bytes, bytes_le, int] can be set.")
            if hex:
                if len(hex) != 4:
                    raise ValueError("badly formed 8-bit hexadecimal UUID string")
                hex = BLE_BASE_UUID.format(hex)
            elif bytes:
                if len(bytes) != 2:
                    raise ValueError("badly formed 8-bit byte input")
                bytes = uuid.UUID(hex=BLE_BASE_UUID.format(bytes.hex())).bytes
            elif bytes_le:
                raise ValueError("byte_le not possible with 8-bit UUID")
            elif int:
                int = uuid.UUID(hex=BLE_BASE_UUID.format(int.to_bytes(2, "big").hex())).int

        object.__setattr__(self, "name", name)  # needed to work around immutability in base class
        super().__init__(hex=hex, bytes=bytes, bytes_le=bytes_le, int=int)

    @property
    def format(self) -> BleUUID.Format:
        """Is this a 16 bit or 128 bit UUID?

        Returns:
            BleUUID.Format: format of UUID
        """
        return BleUUID.Format.BIT_16 if len(self.hex) == BleUUID.Format.BIT_16 else BleUUID.Format.BIT_128

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return self.name if self.name else self.hex

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Descriptor:
    """A characteristic descriptor.

    Args:
        handle (int) : the handle of the attribute table that the descriptor resides at
        uuid (BleUUID): BleUUID of this descriptor
        value (bytes) : the byte stream value of the descriptor
    """

    handle: int
    uuid: BleUUID
    value: Optional[bytes] = None

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=4, default=str)

    @property
    def name(self) -> str:
        """What is the human-readable name of this characteristic?

        Returns:
            str: characteristic's name
        """
        return self.uuid.name


@dataclass
class Characteristic:
    """A BLE characteristic.

    Args:
        handle (int) : the handle of the attribute table that the characteristic resides at
        uuid (BleUUID) : the BleUUID of the characteristic
        props (CharProps) : the characteristic's properties (READ, WRITE, NOTIFY, etc)
        value (bytes) : the current byte stream value of the characteristic value
        init_descriptors (Optional[list[Descriptor]]) : Descriptors known at initialization (can also be
            set later using the descriptors property)
        descriptor_handle (Optional[int]) : handle of this characteristic's declaration descriptor. If not
            passed, defaults to handle + 1
    """

    handle: int
    uuid: BleUUID
    props: CharProps
    value: Optional[bytes] = None
    init_descriptors: InitVar[Optional[list[Descriptor]]] = None
    descriptor_handle: Optional[int] = None

    def __post_init__(self, init_descriptors: Optional[list[Descriptor]]) -> None:
        self._descriptors: dict[BleUUID, Descriptor] = {}
        # Mypy should eventually support this: see https://github.com/python/mypy/issues/3004
        self.descriptors = init_descriptors or []  # type: ignore
        if self.descriptor_handle is None:
            self.descriptor_handle = self.handle + 1

    def __str__(self) -> str:
        return f"{self.name} @ handle {self.handle}: {self.props.name}"

    @property
    def descriptors(self) -> dict[BleUUID, Descriptor]:
        """Return uuid-to-descriptor mapping

        Returns:
            dict[BleUUID, Descriptor]: dictionary of descriptors indexed by BleUUID
        """
        return self._descriptors

    @descriptors.setter
    def descriptors(self, descriptors: list[Descriptor]) -> None:
        for descriptor in descriptors:
            self._descriptors[descriptor.uuid] = descriptor

    @property
    def name(self) -> str:
        """What is the human-readable name of this characteristic?

        Returns:
            str: characteristic's name
        """
        return self.uuid.name

    @property
    def is_readable(self) -> bool:
        """Does this characteristic have readable property?

        Returns:
            bool: True if readable, False if not
        """
        return CharProps.READ in self.props

    @property
    def is_writeable_with_response(self) -> bool:
        """Does this characteristic have writeable-with-response property?

        Returns:
            bool: True if writeable-with-response, False if not
        """
        return CharProps.WRITE_YES_RSP in self.props

    @property
    def is_writeable_without_response(self) -> bool:
        """Does this characteristic have writeable-without-response property?

        Returns:
            bool: True if writeable-without-response, False if not
        """
        return CharProps.WRITE_NO_RSP in self.props

    @property
    def is_writeable(self) -> bool:
        """Does this characteristic have writeable property?

        That is, does it have writeable-with-response or writeable-without-response property

        Returns:
            bool: True if writeable, False if not
        """
        return self.is_writeable_with_response or self.is_writeable_without_response

    @property
    def is_notifiable(self) -> bool:
        """Does this characteristic have notifiable property?

        Returns:
            bool: True if notifiable, False if not
        """
        return CharProps.NOTIFY in self.props

    @property
    def is_indicatable(self) -> bool:
        """Does this characteristic have indicatable property?

        Returns:
            bool: True if indicatable, False if not
        """
        return CharProps.INDICATE in self.props

    @property
    def cccd_handle(self) -> int:
        """What is this characteristics CCCD (client characteristic configuration descriptor) handle

        Returns:
            int: the CCCD handle
        """
        return self._descriptors[UUIDs.CLIENT_CHAR_CONFIG].handle


@dataclass
class Service:
    """A BLE service or grouping of Characteristics.

    Args:
        uuid (BleUUID) : the service's BleUUID
        start_handle(int): the attribute handle where the service begins
        end_handle(int): the attribute handle where the service ends. Defaults to 0xFFFF.
        init_chars (list[Characteristic]) : list of characteristics known at service instantiation. Can be set
            later with the characteristics property
    """

    uuid: BleUUID
    start_handle: int
    end_handle: int = 0xFFFF
    init_chars: InitVar[Optional[list[Characteristic]]] = None

    def __post_init__(self, init_characteristics: Optional[list[Characteristic]]) -> None:
        self._characteristics: dict[BleUUID, Characteristic] = {}
        # Mypy should eventually support this: see https://github.com/python/mypy/issues/3004
        self.characteristics = init_characteristics or []  # type: ignore

    def __str__(self) -> str:
        return self.name

    @property
    def characteristics(self) -> dict[BleUUID, Characteristic]:
        """Return uuid-to-characteristic mapping

        Returns:
            dict[BleUUID, Characteristic]: Dict of characteristics indexed by uuid
        """
        return self._characteristics

    @characteristics.setter
    def characteristics(self, characteristics: list[Characteristic]) -> None:
        for characteristic in characteristics:
            self._characteristics[characteristic.uuid] = characteristic

    @property
    def name(self) -> str:
        """What is the human-readable name of this characteristic?

        Returns:
            str: characteristic's name
        """
        return self.uuid.name


class GattDB:
    """The attribute table to store / look up BLE services, characteristics, and attributes.

    Args:
        init_services (list[Service]): A list of services known at instantiation time. Can be updated later
            with the services property
    """

    class CharacteristicView(Mapping[BleUUID, Characteristic]):
        """Represent the GattDB mapping as characteristics indexed by BleUUID"""

        def __init__(self, db: "GattDB") -> None:
            self._db = db

        def __getitem__(self, key: BleUUID) -> Characteristic:
            for service in self._db.services.values():
                for char in service.characteristics.values():
                    if char.uuid == key:
                        return char
            raise KeyError

        def __contains__(self, key: object) -> bool:
            for service in self._db.services.values():
                for char in service.characteristics.values():
                    if char.uuid == key:
                        return True
            return False

        @no_type_check
        def __iter__(self) -> Iterator[Characteristic]:
            return iter(self.values())

        def __len__(self) -> int:
            return sum(len(service.characteristics) for service in self._db.services.values())

        @no_type_check
        def keys(self) -> Generator[BleUUID, None, None]:  # noqa: D102
            """Generate dict-like keys view

            Returns:
                Generator[BleUUID, None, None]: keys generator
            """

            def iter_keys():
                for service in self._db.services.values():
                    for ble_uuid in service.characteristics.keys():
                        yield ble_uuid

            return iter_keys()

        @no_type_check
        def values(self) -> Generator[Characteristic, None, None]:  # noqa: D102
            """Generate dict-like values view

            Returns:
                Generator[Characteristic, None, None]: values generator
            """

            def iter_values():
                for service in self._db.services.values():
                    for char in service.characteristics.values():
                        yield char

            return iter_values()

        @no_type_check
        def items(
            self,
        ) -> Generator[tuple[BleUUID, Characteristic], None, None]:  # noqa: D102
            """Generate dict-like items view

            Returns:
                Generator[tuple[BleUUID, Characteristic], None, None]: items generator
            """

            def iter_items():
                for service in self._db.services.values():
                    for ble_uuid, char in service.characteristics.items():
                        yield (ble_uuid, char)

            return iter_items()

    def __init__(self, init_services: list[Service]) -> None:
        self._services: dict[BleUUID, Service] = {}
        # Mypy should eventually support this: see https://github.com/python/mypy/issues/3004
        self.services = init_services  # type: ignore
        self.characteristics = self.CharacteristicView(self)

    @property
    def services(self) -> dict[BleUUID, Service]:
        """Return uuid-to-service mapping

        Returns:
            dict[BleUUID, Service]: Dict of services indexed by uuid
        """
        return self._services

    @services.setter
    def services(self, services: list[Service]) -> None:
        for service in services:
            self._services[service.uuid] = service

    def handle2uuid(self, handle: int) -> BleUUID:
        """Get a BleUUID from a handle.

        Args:
            handle (int): the handle to search for

        Raises:
            KeyError: No characteristic was found at this handle

        Returns:
            BleUUID: The found BleUUID
        """
        for s in self.services.values():
            for c in s.characteristics.values():
                if c.handle == handle:
                    return c.uuid
        raise KeyError(f"Matching BleUUID not found for handle {handle}")

    def uuid2handle(self, ble_uuid: BleUUID) -> int:
        """Convert a handle to a BleUUID

        Args:
            ble_uuid (BleUUID): BleUUID to translate

        Returns:
            int: the handle in the Gatt Database where this BleUUID resides
        """
        return self.characteristics[ble_uuid].handle

    def dump_to_csv(self, file: Path = Path("attributes.csv")) -> None:
        """Dump discovered services to a csv file.

        Args:
            file (Path): File to write to. Defaults to "./attributes.csv".
        """
        with open(file, mode="w") as f:
            logger.debug(f"Dumping discovered BLE characteristics to {file}")

            w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["handle", "description", BleUUID, "properties", "value"])

            # For each service in table
            for service in self.services.values():
                w.writerow(
                    [
                        service.start_handle,
                        SpecUuidNumber.PRIMARY_SERVICE,
                        service.uuid.hex,
                        service.name,
                        "SERVICE",
                    ]
                )
                # For each characteristic in service
                for char in service.characteristics.values():
                    w.writerow([char.descriptor_handle, SpecUuidNumber.CHAR_DECLARATION, "28:03", str(char.props), ""])
                    w.writerow([char.handle, char.name, char.uuid.hex, "", char.value])
                    # For each descriptor in characteristic
                    for descriptor in char.descriptors.values():
                        w.writerow([descriptor.handle, descriptor.name, descriptor.uuid.hex, "", descriptor.value])


class UUIDsMeta(type):
    """The metaclass used to build a UUIDs container

    Upon creation of a new UUIDs class, this will store the BleUUID names in an internal mapping indexed by UUID as int
    """

    @no_type_check
    def __new__(mcs, name, bases, dct) -> UUIDsMeta:  # noqa
        x = super().__new__(mcs, name, bases, dct)
        x._int2uuid = {}
        for db in [*[base.__dict__ for base in bases], dct]:
            for _, ble_uuid in [(k, v) for k, v in db.items() if not k.startswith("_")]:
                if not isinstance(ble_uuid, BleUUID):
                    raise TypeError("This class can only be composed of BleUUID attributes")
                x._int2uuid[ble_uuid.int] = ble_uuid
        return x

    @no_type_check
    def __getitem__(cls, key: Union[uuid.UUID, int, str]) -> BleUUID:
        if isinstance(key, uuid.UUID):
            return cls._int2uuid[key.int]
        if isinstance(key, int):
            return cls._int2uuid[key]
        if isinstance(key, str):
            return cls._int2uuid[uuid.UUID(hex=key).int]
        raise TypeError("Key must be of type Union[uuid.UUID, int, str]")

    @no_type_check
    def __contains__(cls, key: Union[uuid.UUID, int, str]) -> bool:
        if isinstance(key, uuid.UUID):
            return key.int in cls._int2uuid
        if isinstance(key, int):
            return key in cls._int2uuid
        if isinstance(key, str):
            # Built uuid.UUID to use it's normalizing
            return uuid.UUID(hex=key).int in cls._int2uuid
        raise TypeError("Key must be of type Union[uuid.UUID, int, str]")

    @no_type_check
    def __iter__(cls):
        for item in cls._int2uuid.items():
            yield item


@dataclass(frozen=True)
class UUIDs(metaclass=UUIDsMeta):
    """BLE Spec-defined UUIDs that are common across all applications.

    Also functions as a dict to look up UUID's by str, int, or BleUUID
    """

    # pylint: disable=no-method-argument
    def __new__(cls, *_: Any) -> UUIDs:  # noqa
        raise RuntimeError("This class shall not be instantiated")

    # GATT Identifiers
    PRIMARY_SERVICE = BleUUID(
        "Primary Service",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.PRIMARY_SERVICE,
    )
    SECONDARY_SERVICE = BleUUID(
        "Secondary Service",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.SECONDARY_SERVICE,
    )
    INCLUDE = BleUUID(
        "Characteristic Include Descriptor",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.INCLUDE,
    )
    CHAR_DECLARATION = BleUUID(
        "Characteristic Declaration",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CHAR_DECLARATION,
    )
    CHAR_EXTENDED_PROPS = BleUUID(
        "Characteristic Extended Properties",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CHAR_EXTENDED_PROPS,
    )
    CHAR_USER_DESCR = BleUUID(
        "Characteristic User Description",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CHAR_USER_DESCR,
    )
    CLIENT_CHAR_CONFIG = BleUUID(
        "Client Characteristic Configuration",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CLIENT_CHAR_CONFIG,
    )
    SERVER_CHAR_CONFIG = BleUUID(
        "Server Characteristic Configuration",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.SERVER_CHAR_CONFIG,
    )
    CHAR_FORMAT = BleUUID(
        "Characteristic Format",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CHAR_FORMAT,
    )
    CHAR_AGGREGATE_FORMAT = BleUUID(
        "Characteristic Aggregate Format",
        format=BleUUID.Format.BIT_16,
        int=SpecUuidNumber.CHAR_AGGREGATE_FORMAT,
    )

    # Generic Attribute Service
    S_GENERIC_ATT = BleUUID("Generic Attribute Service", hex=BLE_BASE_UUID.format("1801"))

    # Generic Access Service
    S_GENERIC_ACCESS = BleUUID("Generic Access Service", hex=BLE_BASE_UUID.format("1800"))
    ACC_DEVICE_NAME = BleUUID("Device Name", hex=BLE_BASE_UUID.format("2a00"))
    ACC_APPEARANCE = BleUUID("Appearance", hex=BLE_BASE_UUID.format("2a01"))
    ACC_PREF_CONN_PARAMS = BleUUID("Preferred Connection Parameters", hex=BLE_BASE_UUID.format("2a04"))
    ACC_CENTRAL_ADDR_RES = BleUUID("Central Address Resolution", hex=BLE_BASE_UUID.format("2aa6"))

    # Tx Power
    S_TX_POWER = BleUUID("Tx Power Service", hex=BLE_BASE_UUID.format("1804"))
    TX_POWER_LEVEL = BleUUID("Tx Power Level", hex=BLE_BASE_UUID.format("2a07"))

    # Battery Service
    S_BATTERY = BleUUID("Battery Service", hex=BLE_BASE_UUID.format("180f"))
    BATT_LEVEL = BleUUID("Battery Level", hex=BLE_BASE_UUID.format("2a19"))

    # Device Information Service
    S_DEV_INFO = BleUUID("Device Information Service", hex=BLE_BASE_UUID.format("180a"))
    INF_MAN_NAME = BleUUID("Manufacturer Name", hex=BLE_BASE_UUID.format("2a29"))
    INF_MODEL_NUM = BleUUID("Model Number", hex=BLE_BASE_UUID.format("2a24"))
    INF_SERIAL_NUM = BleUUID("Serial Number", hex=BLE_BASE_UUID.format("2a25"))
    INF_FW_REV = BleUUID("Firmware Revision", hex=BLE_BASE_UUID.format("2a26"))
    INF_HW_REV = BleUUID("Hardware Revision", hex=BLE_BASE_UUID.format("2a27"))
    INF_SW_REV = BleUUID("Software Revision", hex=BLE_BASE_UUID.format("2a28"))
    INF_SYS_ID = BleUUID("System ID", hex=BLE_BASE_UUID.format("2a23"))
    INF_CERT_DATA = BleUUID("Certification Data", hex=BLE_BASE_UUID.format("2a2a"))
    INF_PNP_ID = BleUUID("PNP ID", hex=BLE_BASE_UUID.format("2a50"))
