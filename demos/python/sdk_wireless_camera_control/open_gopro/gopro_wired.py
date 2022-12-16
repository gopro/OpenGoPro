# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import time
import logging
from pathlib import Path
from typing import Final, Optional, Any, Union

import wrapt

import open_gopro.exceptions as GpException
from open_gopro.gopro_base import GoProBase, MessageMethodType
from open_gopro.constants import StatusId, SettingId
from open_gopro.responses import GoProResp
from open_gopro.api import WiredApi, BleCommands, BleSettings, BleStatuses, HttpCommands, HttpSettings, Params
from open_gopro.interface import GoProWiredInterface, JsonParser, MessageRules

logger = logging.getLogger(__name__)

GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5


@wrapt.decorator
def enforce_message_rules(
    wrapped: MessageMethodType, instance: WiredGoPro, args: Any, kwargs: Any
) -> GoProResp:
    """Wrap the input message method, applying any message rules (MessageRules)

    Args:
        wrapped (MessageMethodType): Method that will be wrapped
        instance (WiredGoPro): owner of method
        args (Any): positional arguments
        kwargs (Any): keyword arguments

    Returns:
        GoProResp: forward response of message method
    """
    rules: list[MessageRules] = kwargs.pop("rules", [])

    # Acquire ready lock unless we are initializing or this is a Set Shutter Off command
    if instance._should_maintain_state and instance.is_open and not MessageRules.FASTPASS in rules:
        # Wait for not encoding and not busy
        logger.trace("Waiting for camera to be ready to receive messages.")  # type: ignore
        instance._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_READY: True})
        logger.trace("Camera is ready to receive messages")  # type: ignore
        response = wrapped(*args, **kwargs)
    else:  # Either we're not maintaining state, we're not opened yet, or this is a fastpass message
        response = wrapped(*args, **kwargs)

    # Release the lock if we acquired it
    if instance._should_maintain_state:
        if response.is_ok:
            # Is there any special handling required after receiving the response?
            if MessageRules.WAIT_FOR_ENCODING_START in rules:
                logger.trace("Waiting to receive encoding started.")  # type: ignore
                # Wait for encoding to start
                instance._wait_for_state({StatusId.ENCODING: True})
    return response


class WiredGoPro(GoProBase[WiredApi], GoProWiredInterface):
    """The top-level USB interface to a Wired GoPro device.

    Args:
        serial (str): (at least) last 3 digits of GoPro Serial number
    """

    _BASE_IP: Final[str] = "172.2{}.1{}{}.51"
    _BASE_ENDPOINT: Final[str] = "http://{ip}:8080/"

    def __init__(self, serial: str, **kwargs: Any) -> None:
        GoProBase.__init__(self, **kwargs)
        GoProWiredInterface.__init__(self)
        self._serial = serial
        # We currently only support version 2.0
        self._wired_api = WiredApi(self)
        self._open = False

    def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to the Wired GoPro Client and prepare it for communication

        Args:
            timeout (int): time before considering connection a failure. Defaults to 10.
            retries (int): number of connection retries. Defaults to 5.

        Raises:
            InvalidOpenGoProVersion: the GoPro camera does not support the correct Open GoPro API version
        """
        # TODO optional mdns discovery
        self.http_command.wired_usb_control(control=Params.Toggle.ENABLE)
        # Find and configure API version
        if (version := self.http_command.get_open_gopro_api_version().flatten) != "2.0":
            raise GpException.InvalidOpenGoProVersion(version)
        logger.info(f"Using Open GoPro API version {version}")

        # Wait for initial ready state
        self._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_READY: True})

        self._open = True

    def close(self) -> None:
        """Gracefully close the GoPro Client connection"""

    @property
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """
        return self._serial

    @property
    def version(self) -> str:
        """The Open GoPro API version of the GoPro Client

        Only Version 2.0 is currently supported.

        Returns:
            str: string version
        """
        return self._api.version

    @property
    def http_command(self) -> HttpCommands:
        """Used to access the USB commands

        Returns:
            HttpCommands: the commands
        """
        return self._api.http_command

    @property
    def http_setting(self) -> HttpSettings:
        """Used to access the USB settings

        Returns:
            HttpSettings: the settings
        """
        return self._api.http_setting

    @property
    def ble_command(self) -> BleCommands:
        """Used to call the BLE commands

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def ble_setting(self) -> BleSettings:
        """Used to access the BLE settings

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def ble_status(self) -> BleStatuses:
        """Used to access the BLE statuses

        Raises:
            NotImplementedError: Not valid for WiredGoPro
        """
        raise NotImplementedError

    @property
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """
        return self._open

    @property
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return False

    @property
    def is_http_connected(self) -> bool:
        """Are we connected via Wifi to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """
        return True  # TODO is this what we want?

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    def _wait_for_state(self, check: dict[Union[StatusId, SettingId], Any], poll_period: int = 1) -> None:
        """Poll the current state until a variable amount of states are all equal to desired values

        Args:
            check (dict[Union[StatusId, SettingId], Any]): dict{setting / status: value} of settings / statuses
                and values to wait for
            poll_period (int): How frequently (in seconds) to poll the current state. Defaults to 1.

        """
        while state := self.http_command.get_camera_state():
            for key, value in check.items():
                if state[key] != value:
                    time.sleep(poll_period)
                    break  # Get new state and try again
            else:
                return  # Everything matches. Exit

    @property
    def _api(self) -> WiredApi:
        return self._wired_api

    @property
    def _base_url(self) -> str:
        """Build the base endpoint for USB commands

        Returns:
            str: base endpoint with URL from serial number
        """
        return WiredGoPro._BASE_ENDPOINT.format(ip=WiredGoPro._BASE_IP.format(*self._serial[-3:]))

    @enforce_message_rules
    def _get(self, url: str, parser: Optional[JsonParser] = None, **kwargs: Any) -> GoProResp:
        return super()._get(url, parser, **kwargs)

    @enforce_message_rules
    def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        return super()._stream_to_file(url, file)
