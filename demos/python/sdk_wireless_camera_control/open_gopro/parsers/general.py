"""Monolithic Parser implementations"""

from dataclasses import asdict

from construct import (
    BitsInteger,
    BitStruct,
    Construct,
    Flag,
    Padding,
)

from open_gopro.models import ScheduledCapture
from open_gopro.parser_interface import BytesParserBuilder
from open_gopro.util import to_dict


class ScheduledCaptureParser(BytesParserBuilder[ScheduledCapture]):
    """Build / parser scheduled capture setting value to / from bytes"""

    scheduled_capture_struct: Construct = BitStruct(
        Padding(3),
        "hour" / BitsInteger(5),
        "minute" / BitsInteger(6),
        "is_24_hour" / Flag,
        "is_enabled" / Flag,
    )

    def parse(self, data: bytes) -> ScheduledCapture:
        return ScheduledCapture(**to_dict(self.scheduled_capture_struct.parse(data)))

    def build(self, obj: ScheduledCapture) -> bytes:
        return self.scheduled_capture_struct.build(asdict(obj))
