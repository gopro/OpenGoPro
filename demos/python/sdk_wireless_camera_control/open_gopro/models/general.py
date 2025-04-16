# general.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Other models that don't deserve their own file"""

from __future__ import annotations

import datetime
import os
import tempfile
from base64 import b64encode
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from open_gopro.constants import SettingId, WebcamError, WebcamStatus
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

    status: WebcamStatus | None = Field(default=None)
    error: WebcamError
    setting_id: str | None = Field(default=None)
    supported_options: list[SupportedOption] | None = Field(default=None)


class HttpInvalidSettingResponse(CustomBaseModel):
    """Invalid settings response with optional supported options"""

    error: int
    setting_id: SettingId
    option_id: int | None = Field(default=None)
    supported_options: list[SupportedOption] | None = Field(default=None)


class CohnInfo(BaseModel):
    """Data model to store Camera on the Home Network connection info"""

    ip_address: str
    username: str
    password: str
    certificate: str

    @cached_property
    def auth_token(self) -> str:
        token = b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("ascii")
        return f"Basic {token}"

    # TODO this is ugly and probably unsecure. Why can't I pass a cert as a string to requests?
    @cached_property
    def certificate_as_path(self) -> Path:
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(self.certificate.encode("utf-8"))
            cert_file.close()
            return Path(cert_file.name)

    def __add__(self, other: CohnInfo) -> CohnInfo:
        return CohnInfo(
            ip_address=other.ip_address or self.ip_address,
            username=other.username or self.username,
            password=other.password or self.password,
            certificate=other.certificate or self.certificate,
        )

    @property
    def is_complete(self) -> bool:
        return "" not in {self.ip_address, self.username, self.password, self.certificate}
