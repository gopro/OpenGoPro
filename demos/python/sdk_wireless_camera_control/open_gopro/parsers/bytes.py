# bytes.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Apr 21 22:24:00 UTC 2025

"""Bytes parser / builders for data models"""

from __future__ import annotations

import datetime
import logging
from dataclasses import asdict
from typing import Any, Generic, TypeVar

import google.protobuf.json_format
from construct import Construct, Flag, Int16sb, Int16ub
from google.protobuf import descriptor
from google.protobuf.json_format import MessageToDict as ProtobufToDict

from open_gopro.domain.enum import GoProIntEnum, enum_factory
from open_gopro.domain.parser_interface import (
    BytesBuilder,
    BytesParser,
    BytesParserBuilder,
)
from open_gopro.models.types import Protobuf
from open_gopro.util import is_dataclass_instance, pretty_print, to_dict

logger = logging.getLogger(__name__)

ProtobufPrinter = google.protobuf.json_format._Printer  # type: ignore # noqa
original_field_to_json = ProtobufPrinter._FieldToJsonObject


class ProtobufDictProxy(dict):
    """Proxy a dict to appear as an object by giving its keys attribute access"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __str__(self) -> str:
        return pretty_print(self.__dict__)

    @classmethod
    def from_proto(cls, proto_dict: dict) -> ProtobufDictProxy:
        """Build a proxy from a dictionary attr-name to value

        Args:
            proto_dict (dict): dict to build from

        Returns:
            ProtobufDictProxy: built proxy
        """

        def recurse(obj: Any) -> Any:
            # Recursion Cases
            if isinstance(obj, list):
                return [recurse(item) for item in obj]
            if isinstance(obj, dict):
                nested_dict = {}
                for key, value in obj.items():
                    nested_dict[key] = recurse(value)
                return ProtobufDictProxy(nested_dict)
            # Base Case
            return obj

        return ProtobufDictProxy(recurse(proto_dict))


class GoProEnumByteParserBuilder(BytesParserBuilder):
    """Parse into a GoProEnum

    Args:
        target (type[GoProIntEnum]): enum type to parse into
    """

    def __init__(self, target: type[GoProIntEnum]) -> None:
        self._container = target

    def parse(self, data: bytes) -> GoProIntEnum:
        """Parse bytes into GoPro enum

        Args:
            data (bytes): bytes to parse

        Returns:
            GoProIntEnum: parsed enum
        """
        return self._container(data[0])

    def build(self, *args: Any, **_: Any) -> bytes:
        """Build bytes from GoPro Enum

        Args:
            *args (Any): enum to use for building
            **_ (Any): not used

        Returns:
            bytes: built bytes
        """
        return bytes([int(args[0])])


class ProtobufByteParser(BytesParser):
    """Parse into a protobuf object

    The actual returned type is a proxy to a protobuf object but it's attributes can be accessed
    using the protobuf definition

    Args:
        proto (type[Protobuf]): protobuf definition to parse (a proxy) into
    """

    def __init__(self, proto: type[Protobuf]) -> None:
        class Closure(BytesParser[dict]):
            """Parse bytes into a dict using the protobuf"""

            protobuf = proto

            # pylint: disable=not-callable
            def parse(self, data: bytes) -> Any:
                response: Protobuf = self.protobuf().FromString(bytes(data))

                # TODO can wetranslate from Protobuf enums without relying on Protobuf internal implementation?
                # Monkey patch the field-to-json function to use our enum translation
                ProtobufPrinter._FieldToJsonObject = lambda self, field, value: (
                    enum_factory(field.enum_type)(value)
                    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM
                    else original_field_to_json(self, field, value)
                )
                as_dict = ProtobufToDict(response, preserving_proto_field_name=True)
                # For any unset fields, use None
                for key in response.DESCRIPTOR.fields_by_name:
                    if key not in as_dict:
                        as_dict[key] = None
                # Proxy as an object
                return ProtobufDictProxy.from_proto(as_dict)

        self._proto_parser = Closure()

    def parse(self, data: bytes) -> dict:
        """Parse the bytes into a Protobuf Proxy

        Args:
            data (bytes): bytes to parse

        Returns:
            dict: protobuf proxy dict which provides attribute access
        """
        return self._proto_parser.parse(data)


class DateTimeByteParserBuilder(BytesParser, BytesBuilder):
    """Handle local and non-local datetime parsing / building"""

    def build(self, obj: datetime.datetime, tzone: int | None = None, is_dst: bool | None = None) -> bytes:
        """Build bytestream from datetime and optional local arguments

        Args:
            obj (datetime.datetime): date and time
            tzone (int | None): timezone (as UTC offset). Defaults to None.
            is_dst (bool | None): is daylight savings time?. Defaults to None.

        Returns:
            bytes: bytestream built from datetime
        """
        byte_data = [*Int16ub.build(obj.year), obj.month, obj.day, obj.hour, obj.minute, obj.second]
        if tzone is not None and is_dst is not None:
            byte_data.extend([*Int16sb.build(tzone), *Flag.build(is_dst)])
        return bytes(byte_data)

    def parse(self, data: bytes) -> dict:
        """Parse bytestream into dict of datetime and potential timezone / dst

        Args:
            data (bytes): bytestream to parse

        Returns:
            dict: dict containing datetime
        """
        is_dst_tz = len(data) == 9
        buf = data[1:]
        year = Int16ub.parse(buf[0:2])

        dt = datetime.datetime(year, *[int(x) for x in buf[2:7]])  # type: ignore
        return (
            {"datetime": dt} if is_dst_tz else {"datetime": dt, "tzone": Int16sb.parse(buf[7:9]), "dst": bool(buf[9])}
        )


class ConstructByteParserBuilder(BytesParserBuilder):
    """Parse bytes into a construct object

    Args:
        construct (Construct): construct definition
    """

    def __init__(self, construct: Construct) -> None:
        self._construct = self._construct_adapter_factory(construct)

    @classmethod
    def _construct_adapter_factory(cls, target: Construct) -> BytesParserBuilder:
        """Build a construct parser adapter from a construct

        Args:
            target (Construct): construct to use for parsing and building

        Returns:
            BytesParserBuilder: instance of generated class
        """

        class ParserBuilder(BytesParserBuilder):
            """Adapt the construct for our interface"""

            container = target

            def parse(self, data: bytes) -> Any:
                return self.container.parse(data)

            def build(self, *args: Any, **kwargs: Any) -> bytes:
                return self.container.build(*args, **kwargs)

        return ParserBuilder()

    def parse(self, data: bytes) -> Construct:
        """Parse bytes into construct container

        Args:
            data (bytes): bytes to parse

        Returns:
            Construct: construct container
        """
        return self._construct.parse(data)

    def build(self, obj: Construct) -> bytes:
        """Built bytes from filled out construct container

        Args:
            obj (Construct): construct container

        Returns:
            bytes: built bytes
        """
        return self._construct.build(obj)


T = TypeVar("T")


class ConstructDataclassByteParserBuilder(Generic[T], BytesParserBuilder[T]):
    """Helper class for byte building / parsing using a data class using Construct"""

    def __init__(self, construct: Construct, data_class: T, int_builder: Construct) -> None:
        self.construct = construct
        self.data_class = data_class
        self.int_builder = int_builder

    def parse(self, data: bytes) -> T:  # noqa: D102
        return self.data_class(**to_dict(self.construct.parse(data)))  # type: ignore

    def build(self, obj: Any) -> bytes:  # noqa: D102
        if is_dataclass_instance(obj):
            return self.construct.build(asdict(obj))
        match obj:
            case int():
                return self.int_builder.build(obj)
            case _:
                raise TypeError(f"Can not build from type {type(obj)}")

    def __call__(self) -> ConstructDataclassByteParserBuilder:
        """Helper method to just return itself in order to be used similarly to other parsers that require instantiation

        Returns:
            ConstructDataclassByteParserBuilder: returns self
        """
        return self
