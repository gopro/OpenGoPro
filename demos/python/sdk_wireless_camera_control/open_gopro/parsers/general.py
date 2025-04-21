# general.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Apr 21 22:24:00 UTC 2025

"""Monolithic Parser implementations"""

from construct import BitsInteger, BitStruct, Flag, Int32ub, Padding

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
