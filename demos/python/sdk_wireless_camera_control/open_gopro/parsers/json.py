# json.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Apr 21 22:24:00 UTC 2025

"""JSON Parser and Transformer implementations"""

from __future__ import annotations

import logging
from typing import Callable, TypeVar, cast

from construct import FormatFieldError
from pydantic import BaseModel

from open_gopro.domain.communicator_interface import GlobalParsers
from open_gopro.domain.parser_interface import JsonParser, JsonTransformer
from open_gopro.models.constants import SettingId, StatusId
from open_gopro.models.types import CameraState, JsonDict, ResponseType
from open_gopro.util import map_keys

T = TypeVar("T")

logger = logging.getLogger()


class CameraStateJsonParser(JsonParser):
    """Parse integer numbers into Enums"""

    def parse(self, data: JsonDict) -> CameraState:
        """Parse dict of integer values into human readable (i.e. enum'ed) setting / status map

        Args:
            data (JsonDict): input dict to parse

        Returns:
            CameraState: output human readable dict
        """
        parsed: dict = {}
        # Parse status and settings values into nice human readable things
        for name, id_map in [("status", StatusId), ("settings", SettingId)]:
            for k, v in data[name].items():
                try:
                    identifier = cast(ResponseType, id_map(int(k)))
                    if not (parser_builder := GlobalParsers.get_query_container(identifier)):
                        parsed[identifier] = v
                    else:
                        parsed[identifier] = parser_builder(v)
                except (ValueError, FormatFieldError) as e:
                    logger.trace(f"Error Parsing {name}::{k}, value: {v} ==> {repr(e)}")  # type: ignore
                    continue
        return parsed


class PydanticAdapterJsonParser(JsonParser[BaseModel]):
    """Parse Json using a Pydantic model

    Args:
        model (type[BaseModel]): model to use for parsing
    """

    def __init__(self, model: type[BaseModel]) -> None:
        self.model = model

    def parse(self, data: JsonDict) -> BaseModel:
        """Parse json dict into model

        Args:
            data (JsonDict): data to parse

        Returns:
            BaseModel: parsed model
        """
        return self.model(**data)


class LambdaJsonParser(JsonParser[T]):
    """Helper class to allow parser definition using a lambda

    Args:
        parser (Callable[[JsonDict], T]): lambda to parse input
    """

    def __init__(self, parser: Callable[[JsonDict], T]) -> None:
        self._parser = parser

    def parse(self, data: JsonDict) -> T:
        """Use stored lambda parse for parsing

        Args:
            data (JsonDict): input dict to parse

        Returns:
            T: parsed output
        """
        return self._parser(data)


class MapJsonKey(JsonTransformer):
    """Map all matching keys using the input function"""

    def __init__(self, key: str, func: Callable) -> None:
        self.key = key
        self.func = func
        super().__init__()

    def transform(self, data: JsonDict) -> JsonDict:
        """Transform json, mapping keys

        Args:
            data (JsonDict): json data to transform

        Returns:
            JsonDict: transformed json data
        """
        map_keys(data, self.key, self.func)
        return data
