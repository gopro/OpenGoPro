# general.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Apr 21 22:24:00 UTC 2025

"""Monolithic Parser implementations"""

from typing import Any

from construct import BitsInteger, BitStruct, Flag, Int8ub, Int32ub, Padding

from open_gopro.domain.parser_interface import BytesParserBuilder
from open_gopro.models import ScheduledCapture
from open_gopro.parsers.bytes import ConstructDataclassByteParserBuilder

ScheduledCaptureParser = ConstructDataclassByteParserBuilder(
    construct=BitStruct(
        Padding(19),
        "hour" / BitsInteger(5),
        "minute" / BitsInteger(6),
        "is_24_hour" / Flag,
        "is_enabled" / Flag,
    ),
    data_class=ScheduledCapture,
    int_builder=Int32ub,
)


class IntByteParserBuilder(BytesParserBuilder[int]):
    """Built / parse integers to / from bytes

    Args:
        length (int): length of byte array to store integer

    Raises:
        ValueError: _description_
    """

    def __init__(self, length: int) -> None:
        match length:
            case 1:
                self._container = Int8ub
            case 4:
                self._container = Int32ub
            case _:
                raise ValueError(f"Length {length} is not handled")

    def parse(self, data: bytes) -> int:  # noqa: D102
        return self._container.parse(data)

    def build(self, obj: Any) -> bytes:  # noqa: D102
        match obj:
            case int():
                return self._container.build(obj)
            case str():
                return self._container.build(int(obj))
            case _:
                raise TypeError(f"Can not build bytes from object of type {type(obj)}")
