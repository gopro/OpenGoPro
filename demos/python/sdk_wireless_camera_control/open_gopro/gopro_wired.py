# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations
import re
import time
import queue
import logging
from pathlib import Path
from typing import Final, Optional, Any, Union

import wrapt
from zeroconf import IPVersion, ServiceBrowser, ServiceListener, Zeroconf

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
        instance._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_BUSY: False})
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

    See the `Open GoPro SDK <https://gopro.github.io/OpenGoPro/python_sdk>`_ for complete documentation.

    If a serial number is not passed when instantiating, the mDNS server will be queried to find a connected
    GoPro.

    This class also handles:
        - ensuring camera is ready / not encoding before transferring data

    It can be used via context manager:

    >>> from open_gopro import WiredGoPro
    >>> with WiredGoPro() as gopro:
    >>>     gopro.http_command.set_shutter(Params.Toggle.ENABLE)

    Or without:

    >>> from open_gopro import WiredGoPro
    >>> gopro = WiredGoPro()
    >>> gopro.open()
    >>> gopro.http_command.set_shutter(Params.Toggle.ENABLE)
    >>> gopro.close()

    Args:
        serial (Optional[str]): (at least) last 3 digits of GoPro Serial number. If not set, first GoPro
            discovered from mDNS will be used.
        kwargs (Any): additional keyword arguments to pass to base class
    """

    _BASE_IP: Final[str] = "172.2{}.1{}{}.51"
    _BASE_ENDPOINT: Final[str] = "http://{ip}:8080/"
    _MDNS_SERVICE_NAME: Final[str] = "_gopro-web._tcp.local."

    def __init__(self, serial: Optional[str], **kwargs: Any) -> None:
        GoProBase.__init__(self, **kwargs)
        GoProWiredInterface.__init__(self)
        self._serial = serial
        # We currently only support version 2.0
        self._wired_api = WiredApi(self)
        self._open = False

    def open(self, timeout: int = 10, retries: int = 1) -> None:
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
            for retry in range(retries):
                try:
                    self._serial = WiredGoPro._find_serial_via_mdns(timeout)
                    if self._serial:
                        break
                except GpException.FailedToFindDevice as e:
                    if retry == retries:
                        raise e
                    logger.warning(f"Failed to discover GoPro. Retrying #{retry}")

        self.http_command.wired_usb_control(control=Params.Toggle.ENABLE)
        # Find and configure API version
        if (version := self.http_command.get_open_gopro_api_version().flatten) != self.version:
            raise GpException.InvalidOpenGoProVersion(version)
        logger.info(f"Using Open GoPro API version {version}")

        # Wait for initial ready state
        self._wait_for_state({StatusId.ENCODING: False, StatusId.SYSTEM_BUSY: False})

        self._open = True

    def close(self) -> None:
        """Gracefully close the GoPro Client connection"""

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
        return True  # TODO is this what we want?

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    @classmethod
    def _find_serial_via_mdns(cls, timeout: int) -> str:
        """Query the mDNS server to find a GoPro

        Args:
            timeout (int): how long to search for before timing out

        Raises:
            FailedToFindDevice: search timed out
            RuntimeError: unexpected runtime error

        Returns:
            str: First discovered IP address matching base GoPro socket address for USB connections
        """

        class ZeroconfListener(ServiceListener):
            """Listens for mDNS services on the local system and save fully-formed ipaddr URLs"""

            def __init__(self) -> None:
                self.urls: queue.Queue[str] = queue.Queue()

            def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
                """Callback called by ServiceBrowser when a new service is discovered

                Args:
                    zc (Zeroconf): instantiated zeroconf object that owns the search
                    type_ (str): name of mDNS service that search is occurring on
                    name (str): discovered device
                """
                if not (info := zc.get_service_info(type_, name)):
                    return  # Could not resolve info

                for ipv4_address in info.parsed_addresses(IPVersion.V4Only):
                    if re.match(r"172.2\d.1\d\d.51", ipv4_address):
                        self.urls.put_nowait(ipv4_address)

        zeroconf = Zeroconf()
        listener = ZeroconfListener()
        browser = ServiceBrowser(zeroconf, WiredGoPro._MDNS_SERVICE_NAME, listener=listener)
        # Wait for URL discovery
        gopro_ip: Optional[str] = None
        exc: Optional[queue.Empty] = None
        try:
            gopro_ip = listener.urls.get(timeout=timeout)
        except queue.Empty as e:
            exc = e
        browser.cancel()
        zeroconf.close()
        if gopro_ip:
            return "".join([gopro_ip[5], *gopro_ip[8:10]])
        if exc:
            raise GpException.FailedToFindDevice() from exc
        raise RuntimeError("Should never get here")

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
                    logger.trace(f"{key.name} is not {value}") # type: ignore
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

        Raises:
            GoProNotOpened: The GoPro serial has not yet been set / discovered

        Returns:
            str: base endpoint with URL from serial number
        """
        if not self._serial:
            raise GpException.GoProNotOpened("Serial / IP has not yet been discovered")
        return WiredGoPro._BASE_ENDPOINT.format(ip=WiredGoPro._BASE_IP.format(*self._serial[-3:]))

    @enforce_message_rules
    def _get(self, url: str, parser: Optional[JsonParser] = None, **kwargs: Any) -> GoProResp:
        return super()._get(url, parser, **kwargs)

    @enforce_message_rules
    def _stream_to_file(self, url: str, file: Path) -> GoProResp:
        return super()._stream_to_file(url, file)
