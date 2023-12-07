# general.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Other models that don't deserve their own file"""

from __future__ import annotations

import datetime
from base64 import b64encode
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import ConfigDict, Field

from open_gopro import constants
from open_gopro.models.bases import CustomBaseModel


class CameraInfo(CustomBaseModel):
    """General camera info"""

    model_config = ConfigDict(protected_namespaces=())
    model_number: int  #: Camera model number
    model_name: str  #: Camera model name as string
    firmware_version: str  #: Complete firmware version
    serial_number: str  #: Camera serial number
    ap_mac_addr: str  #: Camera access point MAC address
    ap_ssid: str  #: Camera access point SSID name


class TzDstDateTime(CustomBaseModel):
    """DST aware datetime"""

    datetime: datetime.datetime
    tzone: int
    dst: bool


class SupportedOption(CustomBaseModel):
    """A supported option in an invalid setting response"""

    display_name: str
    id: int


class WebcamResponse(CustomBaseModel):
    """Common Response from Webcam Commands"""

    status: Optional[constants.WebcamStatus] = Field(default=None)
    error: constants.WebcamError
    setting_id: Optional[str] = Field(default=None)
    supported_options: Optional[list[SupportedOption]] = Field(default=None)


class HttpInvalidSettingResponse(CustomBaseModel):
    """Invalid settings response with optional supported options"""

    error: int
    setting_id: constants.SettingId
    option_id: Optional[int] = Field(default=None)
    supported_options: Optional[list[SupportedOption]] = Field(default=None)


# TODO add to / from json methods
@dataclass
class CohnInfo:
    """Data model to store Camera on the Home Network connection info"""

    ip_address: str
    username: str
    password: str
    certificate: str
    cert_path: Path = Path("cohn.crt")

    def __post_init__(self) -> None:
        token = b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("ascii")
        self.auth_token = f"Basic {token}"
        # self.token = f"Basic {token}"
        with open(self.cert_path, "w") as fp:
            fp.write(self.certificate)
