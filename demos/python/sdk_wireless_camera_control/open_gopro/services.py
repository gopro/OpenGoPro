# services.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Objects to nicely interact with BLE services, characteristics, and attributes.

TODO There needs to be significant future work to make this more useful. It would most likely
be possible to just use the bleak model of this directly but we need to account for other BLE adapters.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Union

from open_gopro.constants import UUID


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
