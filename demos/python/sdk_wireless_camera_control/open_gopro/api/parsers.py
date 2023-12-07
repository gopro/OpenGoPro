# parsers.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Parser implementations"""

from __future__ import annotations

import datetime
import logging
from typing import Any, Callable, TypeVar, cast

import google.protobuf.json_format
from construct import Construct, Flag, Int16sb, Int16ub
from google.protobuf import descriptor
from google.protobuf.json_format import MessageToDict as ProtobufToDict
from pydantic import BaseModel

from open_gopro import types
from open_gopro.constants import SettingId, StatusId
from open_gopro.enum import GoProIntEnum, enum_factory
from open_gopro.parser_interface import (
    BytesBuilder,
    BytesParser,
    BytesParserBuilder,
    GlobalParsers,
    JsonParser,
    JsonTransformer,
)
from open_gopro.util import map_keys, pretty_print

logger = logging.getLogger(__name__)

ProtobufPrinter = google.protobuf.json_format._Printer  # type: ignore # noqa
original_field_to_json = ProtobufPrinter._FieldToJsonObject


# TODO move into below class
def construct_adapter_factory(target: Construct) -> BytesParserBuilder:
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


T = TypeVar("T")


class JsonParsers:
    """The collection of parsers used for additional JSON parsing"""

    class PydanticAdapter(JsonParser[BaseModel]):
        """Parse Json using a Pydantic model

        Args:
            model (type[BaseModel]): model to use for parsing
        """

        def __init__(self, model: type[BaseModel]) -> None:
            self.model = model

        def parse(self, data: types.JsonDict) -> BaseModel:
            """Parse json dict into model

            Args:
                data (dict): data to parse

            Returns:
                BaseModel: parsed model
            """
            return self.model(**data)

    class LambdaParser(JsonParser[T]):
        """Helper class to allow parser definition using a lambda

        Args:
            parser (Callable[[dict], dict]): lambda to parse input
        """

        def __init__(self, parser: Callable[[types.JsonDict], T]) -> None:
            self._parser = parser

        def parse(self, data: types.JsonDict) -> T:
            """Use stored lambda parse for parsing

            Args:
                data (dict): input dict to parse

            Returns:
                T: parsed output
            """
            return self._parser(data)

    class CameraStateParser(JsonParser):
        """Parse integer numbers into Enums"""

        def parse(self, data: types.JsonDict) -> types.CameraState:
            """Parse dict of integer values into human readable (i.e. enum'ed) setting / status map

            Args:
                data (dict): input dict to parse

            Returns:
                dict: output human readable dict
            """
            parsed: dict = {}
            # Parse status and settings values into nice human readable things
            for name, id_map in [("status", StatusId), ("settings", SettingId)]:
                for k, v in data[name].items():
                    identifier = cast(types.ResponseType, id_map(int(k)))
                    try:
                        if not (parser_builder := GlobalParsers.get_query_container(identifier)):
                            parsed[identifier] = v
                        else:
                            parsed[identifier] = parser_builder(v)
                    except ValueError:
                        # This is the case where we receive a value that is not defined in our params.
                        # This shouldn't happen and is either a firmware bug or means the documentation needs to
                        # be updated. However, it isn't functionally critical.
                        logger.warning(f"{str(identifier)} does not contain a value {v}")
                        parsed[identifier] = v
            return parsed


class JsonTransformers:
    """Collection of Json-to-Json transformers"""

    class MapKey(JsonTransformer):
        """Map all matching keys using the input function"""

        def __init__(self, key: str, func: Callable) -> None:
            self.key = key
            self.func = func
            super().__init__()

        def transform(self, data: types.JsonDict) -> types.JsonDict:
            """Transform json, mapping keys

            Args:
                data (types.JsonDict): json data to transform

            Returns:
                types.JsonDict: transformed json data
            """
            map_keys(data, self.key, self.func)
            return data


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


class ByteParserBuilders:
    """Collection byte-to-output type parse (and optionally builders)"""

    class GoProEnum(BytesParserBuilder):
        """Parse into a GoProEnum

        Args:
            target (type[GoProEnum]): enum type to parse into
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

    class Protobuf(BytesParser):
        """Parse into a protobuf object

        The actual returned type is a proxy to a protobuf object but it's attributes can be accessed
        using the protobuf definition

        Args:
            proto (type[types.Protobuf]): protobuf definition to parse (a proxy) into
        """

        def __init__(self, proto: type[types.Protobuf]) -> None:
            class ProtobufByteParser(BytesParser[dict]):
                """Parse bytes into a dict using the protobuf"""

                protobuf = proto

                # TODO can we do this without relying on Protobuf internal implementation
                # pylint: disable=not-callable
                def parse(self, data: bytes) -> Any:
                    response: types.Protobuf = self.protobuf().FromString(bytes(data))

                    # Monkey patch the field-to-json function to use our enum translation
                    ProtobufPrinter._FieldToJsonObject = (
                        lambda self, field, value: enum_factory(field.enum_type)(value)
                        if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM
                        else original_field_to_json(self, field, value)
                    )
                    as_dict = ProtobufToDict(
                        response, including_default_value_fields=False, preserving_proto_field_name=True
                    )
                    # For any unset fields, use None
                    for key in response.DESCRIPTOR.fields_by_name:
                        if key not in as_dict:
                            as_dict[key] = None
                    # Proxy as an object
                    return ProtobufDictProxy.from_proto(as_dict)

            self._proto_parser = ProtobufByteParser()

        def parse(self, data: bytes) -> dict:
            """Parse the bytes into a Protobuf Proxy

            Args:
                data (bytes): bytes to parse

            Returns:
                dict: protobuf proxy dict which provides attribute access
            """
            return self._proto_parser.parse(data)

    class DateTime(BytesParser, BytesBuilder):
        """Handle local and non-local datetime parsing / building"""

        def build(self, obj: datetime.datetime, tzone: int | None = None, is_dst: bool | None = None) -> bytes:
            """Build bytestream from datetime and optional local arguments

            Args:
                obj (datetime.datetime): date and time
                tzone (int | None, optional): timezone (as UTC offset). Defaults to None.
                is_dst (bool | None, optional): is daylight savings time?. Defaults to None.

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
                {"datetime": dt}
                if is_dst_tz
                else {"datetime": dt, "tzone": Int16sb.parse(buf[7:9]), "dst": bool(buf[9])}
            )

    class Construct(BytesParserBuilder):
        """Parse bytes into a construct object

        Args:
            construct (Construct): construct definition
        """

        def __init__(self, construct: Construct) -> None:
            self._construct = construct_adapter_factory(construct)

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

    class DeprecatedMarker(BytesParserBuilder[str]):
        """Used to return "DEPRECATED" when a deprecated setting / status is attempted to be parsed / built"""

        def parse(self, data: bytes) -> str:
            """Return string indicating this ID is deprecated

            Args:
                data (bytes): ignored

            Returns:
                str: "DEPRECATED"
            """
            return "DEPRECATED"

        def build(self, obj: Any) -> bytes:
            """Return empty bytes since this ID is deprecated

            Args:
                obj (Any): ignored

            Returns:
                bytes: empty
            """
            return bytes()
