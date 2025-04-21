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
