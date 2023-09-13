# parsers.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jun 26 18:26:05 UTC 2023

"""Parser Protocol and Bases"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Callable, ClassVar, Generic, Protocol, TypeVar, cast

from open_gopro import types
from open_gopro.constants import ActionId, FeatureId

logger = logging.getLogger(__name__)

T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")

########################################################################################
####### Transformers
########################################################################################


class BaseTransformer(ABC, Generic[T]):
    """Transformer interface.

    A transformer is something that transforms the input into the same output type
    """

    @abstractmethod
    def transform(self, data: T) -> T:
        """Transform data into output matching the input type

        Args:
            data (T): data to transform

        Returns:
            T: transformed data
        """
        raise NotImplementedError


class BytesTransformer(BaseTransformer[bytes]):
    """Bytes to Bytes transformer interface"""


class JsonTransformer(BaseTransformer[types.JsonDict]):
    """Json to json transformer interface"""


########################################################################################
####### Parsers
########################################################################################


class BaseParser(ABC, Generic[T, T_co]):
    """Base Parser Interface

    A parser is something that transforms input into a different type
    """

    @abstractmethod
    def parse(self, data: T) -> T_co:  # pylint: disable=method-hidden
        """Parse data into output type

        Args:
            data (T): input data to parse

        Returns:
            T_co: parsed output
        """
        raise NotImplementedError


class JsonParser(BaseParser[types.JsonDict, T_co]):
    """Json to Target Type Parser Interface"""


class BytesParser(BaseParser[bytes, T_co]):
    """Bytes to Target Type Parser Interface"""


class Parser(ABC, Generic[T]):
    """The common monolithic Parser that is used for all byte and json parsing / transforming

    Algorithm is:
        1. Variable number of byte transformers (bytes --> bytes)
        2. One bytes Json adapter (bytes --> json)
        3. Variable number of json transformers (json --> json)
        4. One JSON parser (json -> Any)

    Args:
        byte_transformers (list[BytesTransformer] | None, optional): bytes --> bytes. Defaults to None.
        byte_json_adapter (BytesParser[types.JsonDict] | None, optional): bytes --> json. Defaults to None.
        json_transformers (list[JsonTransformer] | None, optional): json --> json. Defaults to None.
        json_parser (JsonParser[T] | None, optional): json --> T. Defaults to None.
    """

    def __init__(
        self,
        byte_transformers: list[BytesTransformer] | None = None,
        byte_json_adapter: BytesParser[types.JsonDict] | None = None,
        json_transformers: list[JsonTransformer] | None = None,
        json_parser: JsonParser[T] | None = None,
    ) -> None:
        self.byte_transformers = byte_transformers or []
        self.byte_json_adapter = byte_json_adapter
        self.json_transformers = json_transformers or []
        self.json_parser = json_parser

    def parse(self, data: bytes | bytearray | types.JsonDict) -> T:
        """Perform the parsing using the stored transformers and parsers

        Args:
            data (bytes | bytearray | types.JsonDict): input bytes or json to parse

        Raises:
            RuntimeError: attempted to parse bytes when a byte-json adapter does not exist

        Returns:
            T: TODO
        """
        parsed_json: types.JsonDict
        if isinstance(data, (bytes, bytearray)):
            data = bytes(data)
            if not self.byte_json_adapter:
                raise RuntimeError("Can not parse bytes without Json Adapter")
            # Filter bytes
            parsed_bytes = bytes(data)
            for byte_transformer in self.byte_transformers:
                parsed_bytes = byte_transformer.transform(data)
            parsed_json = self.byte_json_adapter.parse(parsed_bytes)
        else:
            parsed_json = data

        for json_transformer in self.json_transformers:
            parsed_json = json_transformer.transform(parsed_json)
        if self.json_parser:
            return self.json_parser.parse(parsed_json)
        return cast(T, parsed_json)


########################################################################################
####### Builders
########################################################################################


class BytesBuilder(Protocol):
    """Base bytes serializer protocol definition"""

    def build(self, obj: Any) -> bytes:
        """Build bytestream from object

        # noqa: DAR202

        Args:
            obj (Any): object to serialize

        Returns:
            bytes: serialized bytestream
        """


class BytesParserBuilder(BytesParser[T_co], BytesBuilder):
    """Class capable of both building / parsing bytes to / from object"""

    @abstractmethod
    def parse(self, data: bytes) -> T_co:
        """Parse input bytes to output

        Args:
            data (bytes): data to parsed

        Returns:
            T_co: parsed output
        """
        raise NotImplementedError

    @abstractmethod
    def build(self, obj: Any) -> bytes:
        """Build bytestream from object

        # noqa: DAR202

        Args:
            obj (Any): object to serialize

        Returns:
            bytes: serialized bytestream
        """


class GlobalParsers:
    """Parsers that relate globally to ID's as opposed to contextualized per-message

    This is intended to be used as a singleton, i.e. not instantiated

    Returns:
        _type_: _description_
    """

    _feature_action_id_map: ClassVar[dict[FeatureId, list[ActionId]]] = defaultdict(list)
    _global_parsers: ClassVar[dict[types.ResponseType, Parser]] = {}

    @classmethod
    def add_feature_action_id_mapping(cls, feature_id: FeatureId, action_id: ActionId) -> None:
        """Add a feature id-to-action id mapping entry

        Args:
            feature_id (FeatureId): Feature ID of protobuf command
            action_id (ActionId): Action ID of protobuf command
        """
        cls._feature_action_id_map[feature_id].append(action_id)

    @classmethod
    def add(cls, identifier: types.ResponseType, parser: Parser) -> None:
        """Add a global parser that can be accessed by this class's class methods

        Args:
            identifier (types.ResponseType): identifier to add parser for
            parser (Parser): parser to add
        """
        cls._global_parsers[identifier] = parser

    @classmethod
    def get_query_container(cls, identifier: types.ResponseType) -> Callable | None:
        """Attempt to get a callable that will translate an input value to the ID-appropriate value.

        For example, _get_query_container(SettingId.RESOLUTION) will return
        :py:class:`open_gopro.api.params.Resolution`

        As another example, _get_query_container(StatusId.TURBO_MODE) will return bool()

        Note! Not all ID's are currently parsed so None will be returned if the container does not exist

        Args:
            identifier (Union[SettingId, StatusId]): identifier to find container for

        Returns:
            Callable: container if found else None
        """
        try:
            parser_builder = cast(BytesParserBuilder, cls._global_parsers[identifier].byte_json_adapter)
            return lambda data, parse=parser_builder.parse, build=parser_builder.build: parse(build(data))
        except KeyError:
            return None

    @classmethod
    def get_parser(cls, identifier: types.ResponseType) -> Parser | None:
        """Get a globally defined parser for the given ID.

        Currently, only BLE uses globally defined parsers

        Args:
            identifier (types.ResponseType): ID to get parser for

        Returns:
            Optional[Parser]: parser if found, else None
        """
        return cls._global_parsers.get(identifier)
