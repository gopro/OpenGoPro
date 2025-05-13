# general.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Jul 31 17:04:07 UTC 2023

"""Other models that don't deserve their own file"""

from __future__ import annotations

import datetime
import json
import tempfile
from base64 import b64encode
from dataclasses import asdict, dataclass
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from open_gopro.models.bases import CustomBaseModel
from open_gopro.models.constants import SettingId


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
        """Get the auth token from the username and password

        Returns:
            str: _description_
        """
        token = b64encode(f"{self.username}:{self.password}".encode("utf-8")).decode("ascii")
        return f"Basic {token}"

    @cached_property
    def certificate_as_path(self) -> Path:
        """Write the certificate to a tempfile and return the tempfile

        This is needed because requests will not take an in-memory certificate string

        Returns:
            Path: Path of temp certificate file
        """
        with tempfile.NamedTemporaryFile(delete=False) as cert_file:
            cert_file.write(self.certificate.encode("utf-8"))
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
        """Are all of the fields non-empty?

        Returns:
            bool: True if complete, False otherwise
        """
        return bool(self.ip_address) and bool(self.username) and bool(self.password) and bool(self.certificate)


@dataclass(frozen=True)
class ScheduledCapture:
    """Scheduled capture request / status"""

    hour: int
    minute: int
    is_enabled: bool
    is_24_hour: bool

    @classmethod
    def from_datetime(cls, dt: datetime.datetime, is_enabled: bool) -> ScheduledCapture:
        """Helper method to build a ScheduledCapture object from Python standard datetime.datetime

        Args:
            dt (datetime.datetime): datetime to build from
            is_enabled (bool): is / should scheduled capture be enabled on the camera?

        Returns:
            ScheduledCapture: _description_
        """
        return cls(
            hour=dt.hour,
            minute=dt.minute,
            is_enabled=is_enabled,
            is_24_hour=True,
        )

    def __str__(self) -> str:
        return json.dumps(asdict(self), indent=8)

    @classmethod
    def off(cls) -> ScheduledCapture:
        """Helper method to return a pre-filled ScheduledCapture object that can be used to turn scheduled capture off

        Returns:
            ScheduledCapture: object with "is_enabled" set to False
        """
        return cls(0, 0, False, False)
