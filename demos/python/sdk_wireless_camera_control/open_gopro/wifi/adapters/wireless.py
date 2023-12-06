# wifi_controller.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:51 PM

"""Manage a WiFI connection using native OS commands."""

from __future__ import annotations

import ctypes
import html
import locale
import logging
import os
import platform
import re
import tempfile
import time
from enum import Enum, auto
from getpass import getpass
from shutil import which
from typing import Any, Callable, Optional

import wrapt
from packaging.version import Version

from open_gopro.util import cmd
from open_gopro.wifi import SsidState, WifiController

logger = logging.getLogger(__name__)


def ensure_us_english() -> None:
    """Validate the system language is US English for CLI response parsing

    From https://stackoverflow.com/questions/3425294/how-to-detect-the-os-default-language-in-python

    Raises:
        RuntimeError: The system is using any language other then en_US
    """
    if platform.system().lower() == "windows":
        windll = getattr(ctypes, "windll").kernel32
        language = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        language = os.environ["LANG"]

    if not language.startswith("en_US"):
        raise RuntimeError(
            f"The Wifi driver parses CLI responses and only supports en_US where your language is {language}"
        )


@wrapt.decorator
def pass_through_to_driver(wrapped: Callable, instance: WifiCli, args: Any, kwargs: Any) -> Any:
    """Call this same method on the _driver attribute

    Args:
        wrapped (Callable): method to call
        instance (WifiCli): instance to use to find driver
        args (Any): positional arguments
        kwargs (Any): keyword arguments

    Returns:
        Any: result after pass through to driver
    """
    driver_method = getattr(instance._driver, wrapped.__name__)
    return driver_method(*args, **kwargs)


class WifiCli(WifiController):
    """Top level abstraction of different Wifi drivers.

    If interface is not specified (i.e. it is None), we will attempt to automatically
    discover a suitable interface
    """

    def __init__(self, interface: Optional[str] = None, password: Optional[str] = None) -> None:
        """Constructor

        Args:
            interface (str, Optional): Interface. Defaults to None.
            password (str, Optional): User Password for sudo. Defaults to None.

        #noqa: DAR402

        Raises:
            RuntimeError: The system is using any language other then en_US
            RuntimeError: We weren't able to find a suitable driver or auto-detect an interface after detecting driver
        """
        ensure_us_english()
        WifiController.__init__(self, interface, password)

        # detect and init appropriate driver
        self._driver = self._detect_driver()

        # Attempt to set interface (will raise an exception if not able to auto-detect)
        self.interface = interface  # type: ignore

        logger.debug(f"Wifi setup. Using {self}")

    def __str__(self) -> str:
        return f"[{type(self).__name__}] driver::[{self.interface}] interface"

    def _detect_driver(self) -> WifiController:
        """Try to find and instantiate a Wifi driver that can be used.

        Raises:
            RuntimeError: We weren't able to find a suitable driver
            RuntimeError: We weren't able to auto-detect an interface after detecting driver

        Returns:
            WifiController: [description]
        """
        # Try netsh (Windows).
        if os.name == "nt" and which("netsh"):
            return NetshWireless()

        # try networksetup (Mac OS 10.10)
        if which("networksetup"):
            return NetworksetupWireless()

        # Try Linux options. Need password for sudo
        if not self._password:
            self._password = getpass("Need to run as sudo. Enter password: ")
        # Validate password
        if "VALID PASSWORD" not in cmd(f'echo "{self._password}" | sudo -S echo "VALID PASSWORD"'):
            raise RuntimeError("Invalid password")

        # try nmcli (Ubuntu 14.04). Allow for use in Snap Package
        if which("nmcli") or which("nmcli", path="/snap/bin/"):
            version = cmd("nmcli --version").split()[-1]
            return (
                Nmcli0990Wireless(password=self._password)
                if Version(version) >= Version("0.9.9.0")
                else NmcliWireless(password=self._password)
            )
        # try nmcli (Ubuntu w/o network-manager)
        if which("wpa_supplicant"):
            return WpasupplicantWireless(password=self._password)

        raise RuntimeError("Unable to find compatible wireless driver.")

    @pass_through_to_driver
    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:  # type: ignore
        """Connect to a network.

        # noqa: DAR202

        Args:
            ssid (str): SSID of network to connect to
            password (str): password of network to connect to
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if successful, False otherwise
        """

    @pass_through_to_driver
    def disconnect(self) -> bool:  # type: ignore
        """Disconnect from a network.

        # noqa: DAR202

        Returns:
            bool: True if successful, False otherwise
        """

    @pass_through_to_driver
    def current(self) -> tuple[Optional[str], SsidState]:  # type: ignore
        """Return the SSID and state of the current network.

        # noqa: DAR202

        Returns:
            tuple[Optional[str], SsidState]: Tuple of SSID str and state. If SSID is None,
            there is no current connection.
        """

    @pass_through_to_driver
    def available_interfaces(self) -> list[str]:  # type: ignore
        """Return a list of the available Wifi interfaces

        # noqa: DAR202

        Returns:
            list[str]: list of available interfaces
        """

    @pass_through_to_driver
    def power(self, power: bool) -> bool:  # type: ignore
        """Enable / disable the wireless driver.

        # noqa: DAR202

        Args:
            power (bool): Enable if True. Disable if False.

        Returns:
            bool: True if successful, False otherwise
        """

    @property
    def interface(self) -> str:
        """Get the Wifi Interface

        Returns:
            str: interface
        """
        return self._driver.interface

    @interface.setter
    def interface(self, interface: Optional[str]) -> None:
        """Set the Wifi interface.

        If None is passed, interface will attempt to be auto-detected

        Args:
            interface (Optional[str]): interface (or None)
        """
        self._driver.interface = interface  # type: ignore

    @property
    def is_on(self) -> bool:
        """Is the wireless driver currently enabled.

        Returns:
            bool: True if yes. False if no.
        """
        return self._driver.is_on


class NmcliWireless(WifiController):
    """Linux nmcli Driver < 0.9.9.0."""

    def __init__(self, password: str, interface: Optional[str] = None) -> None:
        WifiController.__init__(self, interface=interface, password=password)

    def _clean(self, partial: str) -> None:
        """Clean up connections.

        This is needed to prevent the following error after extended use:
        'maximum number of pending replies per connection has been reached'

        Args:
            partial (str): part of the connection name
        """
        # list matching connections
        response = cmd(f'{self.sudo} nmcli --fields BleUUID,NAME con list | grep "{partial}"')

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                cmd(f"{self.sudo} nmcli con delete uuid {line.split()[0]}")

    @staticmethod
    def _error_in_response(response: str) -> bool:
        """Ignore warnings in nmcli output.

        Sometimes there are warnings but we connected just fine

        Args:
            response (str): output to parse

        Returns:
            bool: True if errors found. False if not.
        """
        # no error if no response
        if len(response) == 0:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith("Error"):
                return True

        # if we didn't find an error then we are in the clear
        return False

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Connect to WiFi SSID.

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # clean up previous connection
        current, _ = self.current()
        if current is not None:
            self._clean(current)

        # First scan to ensure our network is there
        logger.info(f"Scanning for {ssid}...")
        cmd(f"{self.sudo} nmcli device wifi rescan")

        start = time.time()
        discovered = False
        while not discovered and (time.time() - start) <= timeout:
            # Scan for network
            response = cmd(f"{self.sudo} nmcli -f SSID device wifi list")
            for result in response.splitlines()[1:]:  # Skip title row
                if result.strip() == ssid.strip():
                    discovered = True
                    break
            if discovered:
                break
            time.sleep(1)
        else:
            logger.warning("Wifi Scan timed out")
            return False

        # attempt to connect
        logger.info(f"Connecting to {ssid}...")
        response = cmd(f'{self.sudo} nmcli dev wifi connect "{ssid}" password "{password}" iface "{self.interface}"')

        # parse response
        return not self._error_in_response(response)

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> tuple[Optional[str], SsidState]:
        """[summary].

        Returns:
            tuple[Optional[str], SsidState]: [description]
        """
        # list active connections for all interfaces
        response = cmd(f'{self.sudo} nmcli con status | grep "{self.interface}"')

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return (line.split()[0], SsidState.CONNECTED)

        # return none if there was not an active connection
        return (None, SsidState.DISCONNECTED)

    def available_interfaces(self) -> list[str]:
        """Return a list of available Wifi Interface strings

        Returns:
            list[str]: list of interfaces
        """
        # grab list of interfaces
        response = cmd(f"{self.sudo} nmcli dev")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if "wireless" in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "enabled" in cmd(f"{self.sudo} nmcli nm wifi")

    def power(self, power: bool) -> bool:
        """Enable or disbale the Wifi controller

        Args:
            power (bool): True to enable, False to Disable

        Returns:
            bool: True if success, False otherwise
        """
        if power:
            cmd(f"{self.sudo} nmcli nm wifi on")
        else:
            cmd(f"{self.sudo} nmcli nm wifi off")

        return True


class Nmcli0990Wireless(WifiController):
    """Linux nmcli Driver >= 0.9.9.0."""

    def __init__(self, password: str, interface: Optional[str] = None) -> None:
        WifiController.__init__(self, interface=interface, password=password)

    def _clean(self, partial: str) -> None:
        """Clean up connections.

        This is needed to prevent the following error after extended use:
        'maximum number of pending replies per connection has been reached'

        Args:
            partial (str): part of the connection name
        """
        # list matching connections
        response = cmd(f'{self.sudo} nmcli --fields UUID,NAME con show | grep "{partial}"')

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd(f"{self.sudo} nmcli con delete uuid {uuid}")

    @staticmethod
    def _error_in_response(response: str) -> bool:
        """Ignore warnings in nmcli output.

        Sometimes there are warnings but we connected just fine

        Args:
            response (str): output to parse

        Returns:
            bool: True if errors found. False if not.
        """
        # no error if no response
        if len(response) == 0:
            return False

        # loop through each line
        for line in response.splitlines():
            # all error lines start with 'Error'
            if line.startswith("Error"):
                logger.error("line")
                return True

        # if we didn't find an error then we are in the clear
        return False

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Connect to Wifi SSID.

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if connection suceeded, False otherwise
        """
        # First scan to ensure our network is there
        logger.info(f"Scanning for {ssid}...")
        start = time.time()
        discovered = False
        while not discovered and (time.time() - start) <= timeout:
            # Scan for network
            cmd(f"{self.sudo} nmcli device wifi rescan")
            response = cmd(f"{self.sudo} nmcli -f SSID device wifi list")
            for result in response.splitlines()[1:]:  # Skip title row
                if result.strip() == ssid.strip():
                    discovered = True
                    break
            if discovered:
                break
            time.sleep(1)
        else:
            logger.warning("Wifi Scan timed out")
            return False

        # attempt to connect
        logger.info(f"Connecting to {ssid}...")
        response = cmd(f'{self.sudo} nmcli dev wifi connect "{ssid}" password "{password}" ifname "{self.interface}"')

        # parse response
        return not self._error_in_response(response)

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> tuple[Optional[str], SsidState]:
        """[summary].

        Returns:
            tuple[Optional[str], SsidState]: [description]
        """
        # list active connections for all interfaces
        response = cmd(f'{self.sudo} nmcli con | grep "{self.interface}"')

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return (line.split()[0], SsidState.CONNECTED)

        # return none if there was not an active connection
        return (None, SsidState.DISCONNECTED)

    def available_interfaces(self) -> list[str]:
        """Return a list of available Wifi Interface strings

        Returns:
            list[str]: list of interfaces
        """
        # grab list of interfaces
        response = cmd(f"{self.sudo} nmcli dev")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if "wifi" in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "enabled" in cmd(f"{self.sudo} nmcli r wifi")

    def power(self, power: bool) -> bool:
        """Enable or disbale the Wifi controller

        Args:
            power (bool): True to enable, False to Disable

        Returns:
            bool: True if success, False otherwise
        """
        if power:
            cmd(f"{self.sudo} nmcli r wifi on")
        else:
            cmd(f"{self.sudo} nmcli r wifi off")

        return True


class WpasupplicantWireless(WifiController):
    """Linux wpa_supplicant Driver."""

    _file = "/tmp/wpa_supplicant.conf"

    def __init__(self, password: str, interface: Optional[str] = None) -> None:
        WifiController.__init__(self, interface=interface, password=password)

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """[summary].

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # attempt to stop any active wpa_supplicant instances
        # ideally we do this just for the interface we care about
        cmd(f"{self.sudo} killall wpa_supplicant")

        # don't do DHCP for GoPros; can cause dropouts with the server
        cmd(f'{self.sudo} ifconfig "{self.interface}" 10.5.5.10/24 up')

        # create configuration file
        with open(self._file, "w") as fp:
            fp.write(f'network={{\n    ssid="{ssid}"\n    psk="{password}"\n}}\n')
            fp.close()

        # attempt to connect
        cmd(f'{self.sudo} wpa_supplicant -i"{self.interface}" -c"{self._file}" -B')

        # check that the connection was successful
        # i've never seen it take more than 3 seconds for the link to establish
        time.sleep(5)
        current_ssid, _ = self.current()
        if current_ssid != ssid:
            return False

        # attempt to grab an IP
        # better hope we are connected because the timeout here is really long
        # cmd(f"{self.sudo} dhclient {self.interface}"")

        # parse response
        return True

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> tuple[Optional[str], SsidState]:
        """[summary].

        Returns:
            tuple[Optional[str], SsidState]: [description]
        """
        # get interface status
        response = cmd(f'{self.sudo} iwconfig "{self.interface}"')

        # the current network is on the first line like ESSID:"network"
        line = response.splitlines()[0]
        line = line.replace('"', "")
        parts = line.split("ESSID:")
        if len(parts) > 1:
            network = parts[1].strip()
            if network != "off/any":
                return (network, SsidState.CONNECTED)

        # return none if there was not an active connection
        return (None, SsidState.DISCONNECTED)

    def available_interfaces(self) -> list[str]:
        """Return a list of available Wifi Interface strings

        Returns:
            list[str]: list of interfaces
        """
        # grab list of interfaces
        response = cmd(f"{self.sudo} iwconfig")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if len(line) > 0 and not line.startswith(" "):
                # this line contains an interface name!
                if "no wireless extensions" not in line:
                    # this is a wireless interface
                    interfaces.append(line.split()[0])
        return interfaces

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "enabled" in cmd(f"{self.sudo} nmcli r wifi")

    def power(self, power: bool) -> bool:
        """Enable or disable the Wifi controller

        Args:
            power (bool): True to enable, False to Disable

        Returns:
            bool: True if success, False otherwise
        """
        return False


class NetworksetupWireless(WifiController):
    """OS X networksetup Driver."""

    def __init__(self, interface: Optional[str] = None) -> None:
        WifiController.__init__(self, interface)

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Connect to SSID.

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # Escape single quotes
        ssid = ssid.replace(r"'", '''"'"''')

        logger.info(f"Scanning for {ssid}...")
        start = time.time()
        discovered = False
        while not discovered and (time.time() - start) <= timeout:
            # Scan for network
            # Surprisingly, yes this is the industry standard location for this and no, there's no shortcut for it
            response = cmd(
                r"/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport --scan"
            )
            # TODO Sometimes the response is blank?
            if not response:
                logger.warning("MacOS did not return a response to SSID scanning.")
                continue
            lines = response.splitlines()
            ssid_end_index = lines[0].index("SSID") + 4  # Find where the SSID column ends

            for result in lines[1:]:  # Skip title row
                current_ssid = result[:ssid_end_index].strip()
                if current_ssid == ssid.strip():
                    discovered = True
                    break
            if discovered:
                break
            time.sleep(1)
        else:
            logger.warning("Wifi Scan timed out")
            return False

        # If we're already connected, return
        if self.current()[0] == ssid:
            return True

        # Connect now that we found the ssid
        logger.info(f"Connecting to {ssid}...")
        response = cmd(f"networksetup -setairportnetwork '{self.interface}' '{ssid}' '{password}'")

        if "not find" in response.lower():
            return False
        # Now wait for network to actually establish
        current = self.current()[0]
        logger.debug(f"current wifi: {current}")
        while current is not None and ssid not in current and timeout > 0:
            time.sleep(1)
            current = self.current()[0]
            logger.debug(f"current wifi: {current}")
            timeout -= 1
            if timeout == 0:
                return False

        # There is some delay required here, presumably because the network is not ready.
        time.sleep(5)

        return True

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> tuple[Optional[str], SsidState]:
        """[summary].

        Returns:
            tuple[Optional[str], SsidState]: [description]
        """
        # attempt to get current network
        response = cmd(f"networksetup -getairportnetwork '{self.interface}'")

        # parse response
        phrase = "Current Wi-Fi Network: "
        if phrase in response:
            return (response.replace("Current Wi-Fi Network: ", "").strip(), SsidState.CONNECTED)
        return (None, SsidState.DISCONNECTED)

    def available_interfaces(self) -> list[str]:
        """Return a list of available Wifi Interface strings

        Returns:
            list[str]: list of interfaces
        """
        # grab list of interfaces
        response = cmd("networksetup -listallhardwareports")

        # parse response
        interfaces = []
        detected_wifi = False
        for line in response.splitlines():
            if detected_wifi:
                # this line has our interface name in it
                interfaces.append(line.replace("Device: ", ""))
                detected_wifi = False
            else:
                # search for the line that has 'Wi-Fi' in it
                if "Wi-Fi" in line:
                    detected_wifi = True

        # return list
        return interfaces

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "On" in cmd(f"networksetup -getairportpower '{self.interface}'")

    def power(self, power: bool) -> bool:
        """Enable or disbale the Wifi controller

        Args:
            power (bool): True to enable, False to Disable

        Returns:
            bool: True if success, False otherwise
        """
        cmd(f"networksetup -setairportpower '{self.interface}' {'on' if power else 'off'}")

        return True


class NetshWireless(WifiController):
    """Windows Driver."""

    # Used to build profile
    template = r"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>{auth}</authentication>
                <encryption>{encrypt}</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{passwd}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
    <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
        <enableRandomization>false</enableRandomization>
    </MacRandomization>
</WLANProfile>"""

    def __init__(self, interface: Optional[str] = None) -> None:
        WifiController.__init__(self, interface)
        self.ssid: Optional[str] = None

    def __del__(self) -> None:
        self._clean(self.ssid)

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Establish a connection.

        This is blocking and won't return until either a connection is established or
        a 10 second timeout

        Args:
            ssid (str): SSID of network to connect to
            password (str): password of network to connect to
            timeout (float): Time before considering connection failed (in seconds). Defaults to 15.

        Raises:
            RuntimeError: Can not add profile or request to connect to SSID fails

        Returns:
            bool: True if connected, False otherwise
        """
        # Replace xml tokens (&, <, >, etc.)
        password = html.escape(password)
        ssid = html.escape(ssid)

        logger.info(f"Attempting to establish Wifi connection to {ssid}...")

        # Start fresh each time.
        self._clean(ssid)

        # Create new profile
        output = NetshWireless.template.format(ssid=ssid, auth="WPA2PSK", encrypt="AES", passwd=password)
        logger.debug(f"Using template {output}")
        # Need ugly low level mkstemp and os here because standard tempfile can't be accessed by a subprocess in Windows :(
        fd, filename = tempfile.mkstemp()
        os.write(fd, output.encode("utf-8"))
        os.close(fd)
        response = cmd(f"netsh wlan add profile filename={filename}")
        if "is added on interface" not in response:
            raise RuntimeError(response)
        os.remove(filename)

        # Try to connect
        response = cmd(f'netsh wlan connect ssid="{ssid}" name="{ssid}" interface="{self.interface}"')
        if "was completed successfully" not in response:
            raise RuntimeError(response)
        # Wait for connection to establish
        DELAY = 1
        while (current := self.current()) != (ssid, SsidState.CONNECTED):
            logger.debug(f"Waiting {DELAY} second for Wi-Fi connection to establish...")
            time.sleep(DELAY)
            timeout -= DELAY
            if timeout <= 0 or current[1] is SsidState.DISCONNECTED:
                return False

        logger.info("Wifi connection established!")
        self.ssid = ssid

        return True

    def disconnect(self) -> bool:
        """Terminate the Wifi connection.

        Returns:
            bool: True if the disconnect was successful, False otherwise.
        """
        response = cmd(f'netsh wlan disconnect interface="{self.interface}"')

        return bool("completed successfully" in response.lower())

    def current(self) -> tuple[Optional[str], SsidState]:
        """Get the current network SSID and state.

        # Here is an example of what we are parsing (i.e. to find FunHouse SSID):
        # Name                   : Wi-Fi
        # Description            : TP-Link Wireless USB Adapter
        # GUID                   : 093d8022-33cb-4400-8362-275eaf24cb86
        # Physical address       : 98:48:27:88:cb:18
        # State                  : connected
        # SSID                   : FunHouse

        Returns:
            tuple[Optional[str], SsidState]: Tuple of (ssid, network_state)
        """

        class ParseState(Enum):
            """Current state of interface parsing"""

            PARSE_INTERFACE = auto()
            PARSE_SSID = auto()
            PARSE_STATE = auto()

        response = cmd("netsh wlan show interfaces")
        parse_state = ParseState.PARSE_INTERFACE
        ssid: Optional[str] = None
        network_state: Optional[str] = None
        for field in response.split("\r\n"):
            if parse_state is ParseState.PARSE_INTERFACE:
                if "Name" in field and self.interface in field:
                    parse_state = ParseState.PARSE_STATE
            elif parse_state is ParseState.PARSE_STATE:
                if "State" in field:
                    network_state = field.split(":")[1].strip().lower()
                    parse_state = ParseState.PARSE_SSID
            elif parse_state is ParseState.PARSE_SSID:
                if "SSID" in field:
                    ssid = field.split(":")[1].strip()
                    break

        if network_state == "connected":
            state = SsidState.CONNECTED
        elif network_state == "disconnected":
            state = SsidState.DISCONNECTED
        else:
            state = SsidState.ESTABLISHING
        return (ssid, state)

    def available_interfaces(self) -> list[str]:
        """Discover all available interfaces.

        # We're parsing, for example, the following line to find "Wi-Fi":
        # Name                   : Wi-Fi

        Returns:
            list[str]: List of interfaces
        """
        response = cmd("netsh wlan show interfaces")
        interfaces = []

        # Look behind to find field, then match (non-greedy) any chars until CRLF
        match = "(?<={}).+?(?=\\r\\n)"
        for interface in re.findall(match.format("Name"), response):
            # Strip leading whitespace and then the first two chars of remaining (i.e. " :")
            interfaces.append(interface.strip()[2:])

        return interfaces

    @property
    def is_on(self) -> bool:
        """Is Wifi enabled?

        For Windows, this means "Is there at least one Wifi interfaces available?"

        Returns:
            bool: True if yes, False if no.
        """
        response = cmd("netsh wlan show interfaces")
        # Is there at least one interfaces enabled?
        if "no wireless interface" in response.lower():
            return False
        return True

    def power(self, power: bool) -> bool:
        """Enable or disbale the Wifi controller

        Args:
            power (bool): True to enable, False to Disable

        Returns:
            bool: True if success, False otherwise
        """
        arg = "enable" if power else "disable"
        response = cmd(f'netsh interface set interface "{self._interface}" "{arg}"')
        return "not exist" not in response

    @staticmethod
    def _clean(ssid: Optional[str]) -> None:
        """Disconnect and delete SSID profile.

        Args:
            ssid (Optional[str]): name of SSID
        """
        cmd("netsh wlan disconnect")
        if ssid is not None:
            cmd(f'netsh wlan delete profile name="{ssid}"')
