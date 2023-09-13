# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any, Final

import wrapt

import open_gopro.exceptions as GpException
import open_gopro.wifi.mdns_scanner  # Imported this way for pytest monkeypatching
from open_gopro import types
from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    Params,
    WiredApi,
)
from open_gopro.communicator_interface import GoProWiredInterface, MessageRules
from open_gopro.constants import StatusId
from open_gopro.gopro_base import GoProBase, MessageMethodType
from open_gopro.models import GoProResp

logger = logging.getLogger(__name__)

GET_TIMEOUT: Final = 5
HTTP_GET_RETRIES: Final = 5


@wrapt.decorator
async def enforce_message_rules(wrapped: MessageMethodType, instance: WiredGoPro, args: Any, kwargs: Any) -> GoProResp:
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
        await instance._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_BUSY: False})
        logger.trace("Camera is ready to receive messages")  # type: ignore
        response = await wrapped(*args, **kwargs)
    else:  # Either we're not maintaining state, we're not opened yet, or this is a fastpass message
        response = await wrapped(*args, **kwargs)

    # Release the lock if we acquired it
    if instance._should_maintain_state:
        if response.ok:
            # Is there any special handling required after receiving the response?
            if MessageRules.WAIT_FOR_ENCODING_START in rules:
                logger.trace("Waiting to receive encoding started.")  # type: ignore
                # Wait for encoding to start
                await instance._wait_for_state({StatusId.ENCODING: True})
    return response


class WiredGoPro(GoProBase[WiredApi], GoProWiredInterface):
    """The top-level USB interface to a Wired GoPro device.

    See the `Open GoPro SDK <https://gopro.github.io/OpenGoPro/python_sdk>`_ for complete documentation.

    If a serial number is not passed when instantiating, the mDNS server will be queried to find a connected
    GoPro.

    This class also handles:
        - ensuring camera is ready / not encoding before transferring data

    It can be used via context manager:

    >>> async with WiredGoPro() as gopro:
    >>>     print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
    >>>     # Send some messages now

    Or without:

    >>> gopro = WiredGoPro()
    >>> await gopro.open()
    >>> print("Yay! I'm connected via USB, opened, and ready to send / get data now!")
    >>> # Send some messages now

    Args:
        serial (Optional[str]): (at least) last 3 digits of GoPro Serial number. If not set, first GoPro
            discovered from mDNS will be used. Defaults to None
        kwargs (Any): additional keyword arguments to pass to base class
    """

    _BASE_IP: Final[str] = "172.2{}.1{}{}.51"
    _BASE_ENDPOINT: Final[str] = "http://{ip}:8080/"
    _MDNS_SERVICE_NAME: Final[str] = "_gopro-web._tcp.local."

    def __init__(self, serial: str | None = None, **kwargs: Any) -> None:
        GoProBase.__init__(self, **kwargs)
        GoProWiredInterface.__init__(self)
        self._serial = serial
        # We currently only support version 2.0
        self._wired_api = WiredApi(self)
        self._open = False
        self._poll_period = kwargs.get("poll_period", 2)
        self._encoding = False
        self._busy = False

    async def open(self, timeout: int = 10, retries: int = 1) -> None:
        """Connect to the Wired GoPro Client and prepare it for communication

        Args:
            timeout (int): time (in seconds) before considering connection a failure. Defaults to 10.
            retries (int): number of connection retries. Defaults to 1.

        # noqa: DAR401

        Raises:
            InvalidOpenGoProVersion: the GoPro camera does not support the correct Open GoPro API version
            FailedToFindDevice: could not auto-discover GoPro via mDNS # noqa: DAR402
        """
        if not self._serial:
            for retry in range(retries + 1):
                try:
                    ip_addr = await open_gopro.wifi.mdns_scanner.find_first_ip_addr(
                        WiredGoPro._MDNS_SERVICE_NAME, timeout
                    )
                    self._serial = "GoPro X" + "".join([ip_addr[5], *ip_addr[8:10]])
                    break
                except GpException.FailedToFindDevice as e:
                    if retry == retries:
                        raise e
                    logger.warning(f"Failed to discover GoPro. Retrying #{retry + 1}")

        await self.http_command.wired_usb_control(control=Params.Toggle.ENABLE)
        # Find and configure API version
        version = await self.http_command.get_open_gopro_api_version()
        if (version := (await self.http_command.get_open_gopro_api_version()).data) != self.version:
            raise GpException.InvalidOpenGoProVersion(version)
        logger.info(f"Using Open GoPro API version {version}")

        # Wait for initial ready state
        await self._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_BUSY: False})

        self._open = True

    async def close(self) -> None:
        """Gracefully close the GoPro Client connection"""

    @property
    async def is_ready(self) -> bool:
        """Is gopro ready to receive commands

        Returns:
            bool: yes if ready, no otherwise
        """
        current_state = (await self.http_command.get_camera_state()).data
        self._encoding = bool(current_state[StatusId.ENCODING])
        self._busy = bool(current_state[StatusId.SYSTEM_BUSY])
        return not (self._encoding or self._busy)

    @property
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Raises:
            GoProNotOpened: serial was not passed to instantiation and IP has not yet been discovered

        Returns:
            str: identifier
        """
        if self._serial:
            return self._serial
        raise GpException.GoProNotOpened("IP address has not yet been discovered")

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
        return True  # TODO find a better way to do this

    def register_update(self, callback: types.UpdateCb, update: types.UpdateType) -> None:
        """Register for callbacks when an update occurs

        Args:
            callback (types.UpdateCb): callback to be notified in
            update (types.UpdateType): update to register for

        Raises:
            NotImplementedError: not yet possible
        """
        raise NotImplementedError

    def unregister_update(self, callback: types.UpdateCb, update: types.UpdateType | None = None) -> None:
        """Unregister for asynchronous update(s)

        Args:
            callback (types.UpdateCb): callback to stop receiving update(s) on
            update (types.UpdateType | None): updates to unsubscribe for. Defaults to None (all
                updates that use this callback will be unsubscribed).

        Raises:
            NotImplementedError: not yet possible
        """
        raise NotImplementedError

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    async def _wait_for_state(self, check: types.CameraState) -> None:
        """Poll the current state until a variable amount of states are all equal to desired values

        Args:
            check (dict[Union[StatusId, SettingId], Any]): dict{setting / status: value} of settings / statuses
                and values to wait for

        """
        while True:
            state = (await self.http_command.get_camera_state()).data
            for key, value in check.items():
                if state.get(key) != value:
                    await asyncio.sleep(self._poll_period)
                    break  # Get new state and try again
            else:
                return  # Everything matches. Exit

    @property
    def _api(self) -> WiredApi:
        return self._wired_api

    @property
    def _base_url(self) -> str:
        """Build the base endpoint for USB commands

        Raises:
            GoProNotOpened: The GoPro serial has not yet been set / discovered

        Returns:
            str: base endpoint with URL from serial number
        """
        if not self._serial:
            raise GpException.GoProNotOpened("Serial / IP has not yet been discovered")
        return WiredGoPro._BASE_ENDPOINT.format(ip=WiredGoPro._BASE_IP.format(*self._serial[-3:]))

    @enforce_message_rules
    async def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        return await super()._stream_to_file(url, file)
