# responses.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Any responses that are returned from GoPro commands."""

from __future__ import annotations

import enum
import logging
from dataclasses import dataclass
from typing import Generic, TypeVar

from open_gopro.domain.enum import GoProIntEnum
from open_gopro.models.constants import ErrorCode, QueryCmdId
from open_gopro.models.types import ResponseType
from open_gopro.util import pretty_print

logger = logging.getLogger(__name__)

T = TypeVar("T")


class GoProBlePacketHeader(enum.Enum):
    """Packet Headers."""

    GENERAL = 0b00
    EXT_13 = 0b01
    EXT_16 = 0b10
    RESERVED = 0b11
    CONT = enum.auto()


@dataclass
class GoProResp(Generic[T]):
    """The object used to encapsulate all GoPro responses.

    It consists of several common properties / attribute and a data attribute that varies per response.

    >>> gopro = WirelessGoPro()
    >>> await gopro.open()
    >>> response = await (gopro.ble_setting.resolution).get_value()
    >>> print(response)

    Now let's inspect the responses various attributes / properties:

    >>> print(response.status)
    ErrorCode.SUCCESS
    >>> print(response.ok)
    True
    >>> print(response.identifier)
    QueryCmdId.GET_SETTING_VAL
    >>> print(response.protocol)
    Protocol.BLE

    Now let's print it's data as (as JSON):

    >>> print(response)
    {
        "id" : "QueryCmdId.GET_SETTING_VAL",
        "status" : "ErrorCode.SUCCESS",
        "protocol" : "Protocol.BLE",
        "data" : {
            "SettingId.RESOLUTION" : "Resolution.RES_4K_16_9",
        },
    }

    Attributes:
        protocol (GoProResp.Protocol): protocol response was received on
        status (ErrorCode): status of response
        data (T): parsed response data
        identifier (ResponseType): response identifier, the type of which will vary depending on the response
    """

    class Protocol(enum.Enum):
        """Protocol that Command will be sent on."""

        BLE = "BLE"
        HTTP = "HTTP"

    protocol: GoProResp.Protocol
    status: ErrorCode
    data: T
    identifier: ResponseType

    def _as_dict(self) -> dict:
        """Represent the response as dictionary, merging it's data and meta information

        Returns:
            dict: dict representation
        """
        d = {
            "id": self.identifier,
            "status": self.status,
            "protocol": self.protocol,
        }
        if self.data:
            d["data"] = self.data  # type: ignore
        return d

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, GoProIntEnum):
            return self.identifier == obj
        if isinstance(obj, GoProResp):
            return self.identifier == obj.identifier
        raise TypeError("Equal can only compare GoProResp and ResponseType")

    def __str__(self) -> str:
        return pretty_print(self._as_dict())

    def __repr__(self) -> str:
        return f"GoProResp <{str(self.identifier)}>"

    @property
    def ok(self) -> bool:
        """Are there any errors in this response?

        Returns:
            bool: True if the response is ok (i.e. there are no errors), False otherwise
        """
        return self.status in [ErrorCode.SUCCESS, ErrorCode.UNKNOWN]

    @property
    def _is_push(self) -> bool:
        """Was this response an asynchronous push?

        Returns:
            bool: True if yes, False otherwise
        """
        return self.identifier in [
            QueryCmdId.STATUS_VAL_PUSH,
            QueryCmdId.SETTING_VAL_PUSH,
            QueryCmdId.SETTING_CAPABILITY_PUSH,
        ]

    @property
    def _is_query(self) -> bool:
        """Is this response to a settings / status query?

        Returns:
            bool: True if yes, False otherwise
        """
        return isinstance(self.identifier, QueryCmdId)
