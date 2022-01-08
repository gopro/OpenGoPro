# services.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:50 PM

"""Objects to nicely interact with BLE services, characteristics, and attributes."""

from __future__ import annotations
import csv
import json
import logging
import uuid
from pathlib import Path
from enum import IntFlag, IntEnum
from dataclasses import dataclass, field, asdict
from typing import Dict, Iterator, Generator, Mapping, Optional, Tuple, Type, no_type_check, Union

logger = logging.getLogger(__name__)


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


class UuidLength(IntEnum):
    """Used to specify 8-bit or 128-bit UUIDs"""

    BIT_8 = 2
    BIT_128 = 16


class BleUUID(uuid.UUID):
    """Used to identify BLE BleUUID's

    A extension of the standard UUID to associate a string name with the UUID and allow 8-bit UUID input
    """

    BASE_UUID = "0000{}-0000-1000-8000-00805F9B34FB"

    # pylint: disable=redefined-builtin
    def __init__(
        self,
        name: str,
        uuid_format: UuidLength = UuidLength.BIT_128,
        hex: Optional[str] = None,
        bytes: Optional[bytes] = None,
        bytes_le: Optional[bytes] = None,
        int: Optional[int] = None,
    ) -> None:
        self.name: str
        if uuid_format is UuidLength.BIT_8:
            if [hex, bytes, bytes_le, int].count(None) != 3:
                raise ValueError("Only one of [hex, bytes, bytes_le, int] can be set.")
            if hex:
                if len(hex) != 4:
                    raise ValueError("badly formed 8-bit hexadecimal UUID string")
                hex = BleUUID.BASE_UUID.format(hex)
            elif bytes:
                if len(bytes) != 2:
                    raise ValueError("badly formed 8-bit byte input")
                bytes = uuid.UUID(hex=BleUUID.BASE_UUID.format(bytes.hex())).bytes
            elif bytes_le:
                raise ValueError("byte_le not possible with 8-bit UUID")
            elif int:
                int = uuid.UUID(hex=BleUUID.BASE_UUID.format(int.to_bytes(2, "big").hex())).int

        object.__setattr__(self, "name", name)  # needed to work around immutability in base class
        super().__init__(hex=hex, bytes=bytes, bytes_le=bytes_le, int=int)

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return self.hex if self.name == "" else self.name

    def __repr__(self) -> str:  # pylint: disable=missing-return-doc
        return self.__str__()


@dataclass
class Descriptor:
    """A charactersistic descriptor.
    Args:
        handle (int) : the handle of the attribute table that the descriptor resides at
        uuid (BleUUID): BleUUID of this descriptor
        value (bytes) : the byte stream value of the descriptor
    """

    handle: int
    uuid: BleUUID
    value: Optional[bytes] = None

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return json.dumps(asdict(self), indent=4, default=str)


@dataclass
class Characteristic:
    """A BLE charactersistic.
    Args:
        handle (int) : the handle of the attribute table that the characteristic resides at
        descriptor_handle (int) : TODO
        uuid (BleUUID) : the BleUUID of the characteristic
        props (CharProps) : the characteristic's properties (READ, WRITE, NOTIFY, etc)
        name (str) : the characteristic's name
        value (bytes) : the current byte stream value of the characteristic value
        descriptors (List[Descriptor], optional) : Any relevant descriptors if they exist
    """

    handle: int
    descriptor_handle: int
    uuid: BleUUID
    props: CharProps
    name: str = ""
    value: Optional[bytes] = None
    descriptors: Dict[BleUUID, Descriptor] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.props = CharProps(int(self.props))
        if self.uuid.name == "":
            self.uuid.name = self.name

    def __str__(self) -> str:  # pylint: disable=missing-return-doc
        return f"BleUUID {str(self.uuid)} @ handle {self.handle}: {self.props}"

    @property
    def is_readable(self) -> bool:
        """Does this characteric have readable property?

        Returns:
            bool: True if readable, False if not
        """
        return CharProps.NOTIFY in self.props

    @property
    def is_writeable_with_response(self) -> bool:
        """Does this characteric have writeable-with-response property?

        Returns:
            bool: True if writeable-with-response, False if not
        """
        return CharProps.WRITE_YES_RSP in self.props

    @property
    def is_writeable_without_response(self) -> bool:
        """Does this characteric have writeable-without-response property?

        Returns:
            bool: True if writeable-without-response, False if not
        """
        return CharProps.WRITE_NO_RSP in self.props

    @property
    def is_writeable(self) -> bool:
        """Does this characteric have writeable property?

        That is, does it have writeable-with-response or writeable-without-response property

        Returns:
            bool: True if writeable, False if not
        """
        return self.is_writeable_with_response or self.is_writeable_without_response

    @property
    def is_notifiable(self) -> bool:
        """Does this characteric have notifiable property?

        Returns:
            bool: True if notifiable, False if not
        """
        return CharProps.NOTIFY in self.props

    @property
    def is_indicatable(self) -> bool:
        """Does this characteric have indicatable property?

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
        return self.descriptors[UUIDs.CLIENT_CHAR_CONFIG].handle


@dataclass
class Service:
    """A BLE service or grouping of Characteristics.
    Args:
        uuid (BleUUID) : the service's BleUUID
        start_handle(int): the attribute handle where the service begins
        end_handle(int): the attribute handle where the service ends
        name (str) : the service's name
        chars (Dict[str, Characteristic]) : the dictionary of characteristics, indexed by name
    """

    uuid: BleUUID
    start_handle: int
    name: str
    end_handle: int = 0xFFFF
    chars: Dict[BleUUID, Characteristic] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.uuid.name == "":
            self.uuid.name = self.name


class GattDB:
    """The attribute table to store / look up BLE services, characteristics, and attributes.
    Args:
        services (Dict[BleUUID, Service]): A dictionary of Services indexed by BleUUID.
        characteristics (Dict[BleUUID, Characteristic]): A dictionary of Characteristics indexed by BleUUID.
    """

    # TODO fix typing here
    class CharacteristicView(Mapping):
        """Represent the GattDB mapping as characteristics indexed by BleUUID"""

        def __init__(self, db: "GattDB") -> None:
            self._db = db

        def __getitem__(self, key: BleUUID) -> Characteristic:  # pylint: disable=missing-return-doc
            for service in self._db.services.values():
                for char in service.chars.values():
                    if char.uuid == key:
                        return char
            raise KeyError

        def __contains__(self, key: object) -> bool:  # pylint: disable=missing-return-doc
            for service in self._db.services.values():
                for char in service.chars.values():
                    if char.uuid == key:
                        return True
            return False

        @no_type_check
        def __iter__(self) -> Iterator[BleUUID]:  # pylint: disable=missing-return-doc
            return iter(self.keys())

        def __len__(self) -> int:  # pylint: disable=missing-return-doc
            return sum(len(service.chars) for service in self._db.services.values())

        @no_type_check
        def keys(self) -> Generator[BleUUID, None, None]:  # pylint: disable=missing-return-doc
            def iter_keys():
                for service in self._db.services.values():
                    for ble_uuid in service.chars.keys():
                        yield ble_uuid

            return iter_keys()

        @no_type_check
        def values(self) -> Generator[Characteristic, None, None]:  # pylint: disable=missing-return-doc
            def iter_values():
                for service in self._db.services.values():
                    for char in service.chars.values():
                        yield char

            return iter_values()

        @no_type_check
        def items(  # pylint: disable=missing-return-doc
            self,
        ) -> Generator[Tuple[BleUUID, Characteristic], None, None]:
            def iter_items():
                for service in self._db.services.values():
                    for ble_uuid, char in service.chars.items():
                        yield (ble_uuid, char)

            return iter_items()

    def __init__(self, services: Dict[BleUUID, Service]) -> None:
        self.services: Dict[BleUUID, Service] = services
        self.characteristics = self.CharacteristicView(self)

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
            for c in s.chars.values():
                if c.handle == handle:
                    return c.uuid
        raise KeyError(f"Matching BleUUID not found for handle {handle}")

    def uuid2handle(self, ble_uuid: BleUUID) -> int:
        """Convert a handle to a BleUUID

        Args:
            ble_uuid (BleUUID): BleUUID to translate

        Returns:
            int: the handle in the Gatt Database where this BleUUID resides

        Raises:
            KeyError: This BleUUID does not exist in the Gatt database
        """
        return self.characteristics[ble_uuid].handle

    def dump_to_csv(self, file: Path = Path("attributes.csv")) -> None:
        """Dump discovered services to a csv file.
        Args:
            file (Path, optional): File to write to. Defaults to "./attributes.csv".
        """
        with open(file, mode="w") as f:
            logger.debug(f"Dumping discovered BLE characteristics to {file}")

            w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow(["handle", "description", BleUUID, "properties", "value"])

            # For each service in table
            for service in self.services.values():
                desc = "unknown" if service.name == "" else service.name
                w.writerow(
                    [
                        service.start_handle,
                        SpecUuidNumber.PRIMARY_SERVICE,
                        service.uuid.hex,
                        desc,
                        "SERVICE",
                    ]
                )
                # For each characteristic in service
                for char in service.chars.values():
                    w.writerow(
                        [char.descriptor_handle, SpecUuidNumber.CHAR_DECLARATION, "28:03", str(char.props), ""]
                    )
                    description = "unknown" if char.name == "" else char.name
                    w.writerow([char.handle, description, char.uuid.hex, "", char.value])
                    # For each descriptor in characteristic
                    for descriptor in char.descriptors.values():
                        description = SpecUuidNumber(descriptor.uuid.int).name
                        w.writerow([descriptor.handle, description, descriptor.uuid.hex, "", descriptor.value])


class UUIDsMeta(type):
    """The metaclass used to build a UUIDs container

    Upon creation of a new UUIDs class, this will store the BleUUID names in an internal mapping indexed by UUID as int
    """

    @no_type_check
    def __new__(cls, name, bases, dct) -> UUIDsMeta:  # pylint: disable=missing-return-doc
        x = super().__new__(cls, name, bases, dct)
        x._int2uuid = {}
        for _, ble_uuid in [(k, v) for k, v in dct.items() if not k.startswith("__")]:
            if not isinstance(ble_uuid, BleUUID):
                raise TypeError("This class can only be composed of BleUUID attributes")
            x._int2uuid[ble_uuid.int] = ble_uuid
        return x

    @no_type_check
    def __getitem__(cls, key: Union[BleUUID, int, str]) -> BleUUID:  # pylint: disable=missing-return-doc
        if isinstance(key, BleUUID):
            return cls._int2uuid[key.int]
        if isinstance(key, int):
            return cls._int2uuid[key]
        if isinstance(key, str):
            return cls._int2uuid[uuid.UUID(hex=key).int]
        raise TypeError("Key must be of type  Union[BleUUID, int, str]")

    @no_type_check
    def __contains__(cls, key: Union[BleUUID, int, str]) -> bool:  # pylint: disable=missing-return-doc
        if isinstance(key, BleUUID):
            return key.int in cls._int2uuid
        if isinstance(key, int):
            return key in cls._int2uuid
        if isinstance(key, str):
            return uuid.UUID(hex=key).int in cls._int2uuid
        raise TypeError("Key must be of type  Union[BleUUID, int, str]")

    @no_type_check
    def __iter__(cls):  # pylint: disable=missing-return-doc
        for item in cls._uuids.items():
            yield item


@dataclass(frozen=True)
class UUIDs(metaclass=UUIDsMeta):
    """BLE Spec-defined UUIDs that are common across all applications.

    Also functions as a dict to look up UUID's by str, int, or BleUUID

    """

    @no_type_check
    def __new__(cls: Type[UUIDs]) -> Type[UUIDs]:
        raise Exception("This class shall not be instantiated")

    # GATT Identifiers
    PRIMARY_SERVICE = BleUUID(
        "Primary Service",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.PRIMARY_SERVICE,
    )
    SECONDARY_SERVICE = BleUUID(
        "Secondary Service",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.SECONDARY_SERVICE,
    )
    INCLUDE = BleUUID(
        "Characteristic Include Descriptor",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.INCLUDE,
    )
    CHAR_DECLARATION = BleUUID(
        "Characteristic Declaration",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CHAR_DECLARATION,
    )
    CHAR_EXTENDED_PROPS = BleUUID(
        "Characteristic Extended Properties",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CHAR_EXTENDED_PROPS,
    )
    CHAR_USER_DESCR = BleUUID(
        "Characteristic User Description",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CHAR_USER_DESCR,
    )
    CLIENT_CHAR_CONFIG = BleUUID(
        "Client Characteristic Configuration",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CLIENT_CHAR_CONFIG,
    )
    SERVER_CHAR_CONFIG = BleUUID(
        "Server Characteristic Configuration",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.SERVER_CHAR_CONFIG,
    )
    CHAR_FORMAT = BleUUID(
        "Characteristic Format",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CHAR_FORMAT,
    )
    CHAR_AGGREGATE_FORMAT = BleUUID(
        "Characteristic Aggregate Format",
        uuid_format=UuidLength.BIT_8,
        int=SpecUuidNumber.CHAR_AGGREGATE_FORMAT,
    )

    # Generic Attribute Service
    S_GENERIC_ATT = BleUUID("Generic Attribute Service", hex="00001801-0000-1000-8000-00805f9b34fb")

    # Generic Access Service
    S_GENERIC_ACCESS = BleUUID("Generic Access Service", hex="00001800-0000-1000-8000-00805f9b34fb")
    ACC_DEVICE_NAME = BleUUID("Device Name", hex="00002a00-0000-1000-8000-00805f9b34fb")
    ACC_APPEARANCE = BleUUID("Appearance", hex="00002a01-0000-1000-8000-00805f9b34fb")
    ACC_PREF_CONN_PARAMS = BleUUID(
        "Peripheral Preferred Connection Parameters", hex="00002a04-0000-1000-8000-00805f9b34fb"
    )
    ACC_CENTRAL_ADDR_RES = BleUUID("Central Address Resolution", hex="00002aa6-0000-1000-8000-00805f9b34fb")

    # Tx Power
    S_TX_POWER = BleUUID("Tx Power Service", hex="00001804-0000-1000-8000-00805f9b34fb")
    TX_POWER_LEVEL = BleUUID("Tx Power Level", hex="00002a07-0000-1000-8000-00805f9b34fb")

    # Battery Service
    S_BATTERY = BleUUID("Battery Service", hex="0000180f-0000-1000-8000-00805f9b34fb")
    BATT_LEVEL = BleUUID("Battery Level", hex="00002a19-0000-1000-8000-00805f9b34fb")

    # Device Information Service
    S_DEV_INFO = BleUUID("Device Information Service", hex="0000180a-0000-1000-8000-00805f9b34fb")
    INF_MAN_NAME = BleUUID("Manufacturer Name", hex="00002a29-0000-1000-8000-00805f9b34fb")
    INF_MODEL_NUM = BleUUID("Model Number", hex="00002a24-0000-1000-8000-00805f9b34fb")
    INF_SERIAL_NUM = BleUUID("Serial Number", hex="00002a25-0000-1000-8000-00805f9b34fb")
    INF_FW_REV = BleUUID("Firmware Revision", hex="00002a26-0000-1000-8000-00805f9b34fb")
    INF_HW_REV = BleUUID("Hardware Revision", hex="00002a27-0000-1000-8000-00805f9b34fb")
    INF_SW_REV = BleUUID("Software Revision", hex="00002a28-0000-1000-8000-00805f9b34fb")
    INF_SYS_ID = BleUUID("System ID", hex="00002a23-0000-1000-8000-00805f9b34fb")
    INF_CERT_DATA = BleUUID("Certification Data", hex="00002a2a-0000-1000-8000-00805f9b34fb")
    INF_PNP_ID = BleUUID("PNP ID", hex="00002a50-0000-1000-8000-00805f9b34fb")
