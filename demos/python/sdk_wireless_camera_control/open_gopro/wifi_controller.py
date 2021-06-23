# wifi_controller.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

"""Manage a WiFI connection using native OS commands."""

# TODO This file needs to be cleaned up.

import os
import re
import time
import logging
import tempfile
from enum import Enum, auto
from typing import List, Optional, Tuple, Any

from open_gopro.util import cmd
from open_gopro.interfaces import WifiController

logger = logging.getLogger(__name__)


def cmp(a: Any, b: Any) -> int:
    """Define this since it is not implemented in Python 3.

    Args:
        a (Any): compare to
        b (Any): compare against

    Returns:
        int: compare result
    """
    if a < b:
        return -1

    if a == b:
        return 0

    return 1


def ensure_sudo() -> None:
    """Verify that we are running as root

    Raises:
        Exception: Program is running as a user other than root
    """
    user = cmd("whoami")
    if "root" not in user:
        logger.error(f"You need to be the root user to run this program but you are running as {user}")
        raise Exception("Program needs to be run as root user.")


class Wireless(WifiController):
    """Top level abstraction of different WiFi drivers.

    If interface is not specified (i.e. it is None), we will attempt ot automatically Receive response -->
    disover a suitable interface

    Args:
        interface (str, optional): Interface. Defaults to None.

    Raises:
        Exception: Failed to find a suitable driver or auto-detect the network interface.
    """

    _driver_name = "NOT INITIALIZED"
    _driver: WifiController

    # init
    def __init__(self, interface: Optional[str] = None):
        # detect and init appropriate driver
        self._driver_name = self._detectDriver()
        if self._driver_name == "nmcli":
            self._driver = NmcliWireless(interface=interface)
        elif self._driver_name == "nmcli0990":
            self._driver = Nmcli0990Wireless(interface=interface)
        elif self._driver_name == "wpa_supplicant":
            self._driver = WpasupplicantWireless(interface=interface)
        elif self._driver_name == "networksetup":
            self._driver = NetworksetupWireless(interface=interface)
        elif self._driver_name == "netsh":
            self._driver = NetshWireless(interface=interface)

        # attempt to auto detect the interface if none was provided
        if self.interface() is None:
            interfaces = self.interfaces()
            if len(interfaces) > 0:
                self.interface(interfaces[0])

        # raise an error if there is still no interface defined
        if self.interface() is None:
            raise Exception("Unable to auto-detect the network interface.")

        logger.debug(f"Using WiFi driver: {self._driver_name} with interface {self.interface()}")

    def _detectDriver(self) -> str:
        """Try to find a Wifi driver that can be used.

        Raises:
            Exception: We weren't able to find a suitable driver

        Returns:
            str: Name of discovered driver
        """
        if os.name == 'nt':
            # try netsh (Windows).
            response = cmd("where netsh")
            if len(response) > 0 and "not found" not in response and "not recognized" not in response:
                return "netsh"
            response = cmd("powershell get-command netsh")
            if len(response) > 0 and "not found" not in response and "not recognized" not in response:
                return "netsh"
        else:
            # try nmcli (Ubuntu 14.04)
            response = cmd("which nmcli")
            if len(response) > 0 and "not found" not in response:
                response = cmd("nmcli --version")
                parts = response.split()
                ver = parts[-1]
                compare = self.vercmp(ver, "0.9.9.0")
                if compare >= 0:
                    return "nmcli0990"

                return "nmcli"

            # try nmcli (Ubuntu w/o network-manager)
            response = cmd("which wpa_supplicant")
            if len(response) > 0 and "not found" not in response:
                return "wpa_supplicant"

        # try networksetup (Mac OS 10.10)
        response = cmd("which networksetup")
        if len(response) > 0 and "not found" not in response:
            return "networksetup"

        raise Exception("Unable to find compatible wireless driver.")

    @staticmethod
    def vercmp(actual: Any, test: Any) -> int:
        """Compare two versions.

        Args:
            actual (str): Version being compared
            test (str): Thing that version is being compared to

        Returns:
            -1: a is less than b
            0: a is equal to b
            1: a is greater than b
        """

        def normalize(v: str) -> List[int]:
            """Normalize a string vresion

            Args:
                v (str): input string

            Returns:
                List[int]: output int list
            """
            return [int(x) for x in re.sub(r"(\.0+)*$", "", v).split(".")]

        return cmp(normalize(actual), normalize(test))

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Wrapper to call the OS-specific driver method.

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if the connect was successful, False otherwise
        """
        return self._driver.connect(ssid, password)

    def disconnect(self) -> bool:
        """Wrapper to call the OS-specific driver method.

        Returns:
            bool: True if the disconnect was successful, False otherwise
        """
        return self._driver.disconnect()

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """Wrapper to call the OS-specific driver method.

        Returns:
            Tuple[Optional[str], Optional[str]]: (ssid, network state)
        """
        return self._driver.current()

    def interfaces(self) -> List[str]:
        """Wrapper to call the OS-specific driver method.

        Returns:
            List[str]: list of discovered interfaces
        """
        return self._driver.interfaces()

    def interface(self, interface: Optional[str] = None) -> Optional[str]:
        """Wrapper to call the OS-specific driver method.

        Use a str as interface to set it, otherwise use None to get it.

        Args:
            interface (Optional[str], optional): get or set interface. Defaults to None.

        Returns:
            Optional[str]: Str if getting
        """
        return self._driver.interface(interface)

    @property
    def is_on(self) -> bool:
        """Wrapper to call the OS-specific driver method.

        Returns:
            bool: True if on, False if off
        """
        return self._driver.is_on

    def power(self, power: bool) -> None:
        """Wrapper to call the OS-specific driver method.

        Args:
            power (bool): [description]

        Returns:
            [type]: [description]
        """
        return self._driver.power(power)

    def driver(self) -> str:
        """Get the name of the driver currently being used.

        Returns:
            str: Driver name.
        """
        return self._driver_name


class NmcliWireless(WifiController):
    """Linux nmcli Driver < 0.9.9.0."""

    _interface = None

    def __init__(self, interface: str = None) -> None:
        ensure_sudo()
        self.interface(interface)

    @staticmethod
    def _clean(partial: str) -> None:
        """Clean up connections.

        This is needed to prevent the following error after extended use:
        'maximum number of pending replies per connection has been reached'

        Args:
            partial (str): part of the connection name
        """
        # list matching connections
        response = cmd(f"nmcli --fields UUID,NAME con list | grep {partial}")

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                cmd(f"nmcli con delete uuid {line.split()[0]}")

    @staticmethod
    def _errorInResponse(response: str) -> bool:
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
        """[summary].

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # clean up previous connection
        current, _ = self.current()
        if current is not None:
            self._clean(current)

        # attempt to connect
        response = cmd(
            "nmcli dev wifi connect {} password {} iface {}".format(ssid, password, self._interface)
        )

        # parse response
        return not self._errorInResponse(response)

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """[summary].

        Returns:
            Tuple[Optional[str], Optional[str]]: [description]
        """
        # list active connections for all interfaces
        response = cmd("nmcli con status | grep {}".format(self.interface()))

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return (line.split()[0], None)

        # return none if there was not an active connection
        return (None, None)

    def interfaces(self) -> List[str]:
        """[summary].

        Returns:
            List[str]: [description]
        """
        # grab list of interfaces
        response = cmd("nmcli dev")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if "wireless" in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    def interface(self, interface: Optional[str] = None) -> Optional[str]:
        """[summary].

        Args:
            interface (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Optional[str]: [description]
        """
        if interface is not None:
            self._interface = interface
            return None
        return self._interface

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "enabled" in cmd("nmcli nm wifi")

    def power(self, power: bool) -> None:
        """[summary].

        Args:
            power (bool): [description]
        """
        if power:
            cmd("nmcli nm wifi on")
        else:
            cmd("nmcli nm wifi off")


class Nmcli0990Wireless(WifiController):
    """Linux nmcli Driver >= 0.9.9.0."""

    _interface = None

    def __init__(self, interface: str = None):
        ensure_sudo()
        self.interface(interface)

    # TODO Is this needed?
    @staticmethod
    def _clean(partial: str) -> None:
        """Clean up connections.

        This is needed to prevent the following error after extended use:
        'maximum number of pending replies per connection has been reached'

        Args:
            partial (str): part of the connection name
        """
        # list matching connections
        response = cmd("nmcli --fields UUID,NAME con show | grep {}".format(partial))

        # delete all of the matching connections
        for line in response.splitlines():
            if len(line) > 0:
                uuid = line.split()[0]
                cmd("nmcli con delete uuid {}".format(uuid))

    @staticmethod
    def _errorInResponse(response: str) -> bool:
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
        """[summary].

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # Scan for networks. Don't bother checking: we'll allow the error to be passed from the connect.
        cmd("nmcli dev wifi list --rescan yes")
        # attempt to connect
        response = cmd(f"nmcli dev wifi connect {ssid} password {password} ifname {self._interface}")

        # TODO verify that we're connected (and use timeout)

        # parse response
        return not self._errorInResponse(response)

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """[summary].

        Returns:
            Tuple[Optional[str], Optional[str]]: [description]
        """
        # list active connections for all interfaces
        response = cmd("nmcli con | grep {}".format(self.interface()))

        # the current network is in the first column
        for line in response.splitlines():
            if len(line) > 0:
                return (line.split()[0], None)

        # return none if there was not an active connection
        return (None, None)

    def interfaces(self) -> List[str]:
        """[summary].

        Returns:
            List[str]: [description]
        """
        # grab list of interfaces
        response = cmd("nmcli dev")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if "wifi" in line:
                # this line has our interface name in the first column
                interfaces.append(line.split()[0])

        # return list
        return interfaces

    def interface(self, interface: Optional[str] = None) -> Optional[str]:
        """[summary].

        Args:
            interface (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Optional[str]: [description]
        """
        if interface is not None:
            self._interface = interface
            return None
        return self._interface

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "enabled" in cmd("nmcli r wifi")

    def power(self, power: bool) -> None:
        """[summary].

        Args:
            power (bool): [description]
        """
        if power:
            cmd("nmcli r wifi on")
        else:
            cmd("nmcli r wifi off")


class WpasupplicantWireless(WifiController):
    """Linux wpa_supplicant Driver."""

    _file = "/tmp/wpa_supplicant.conf"
    _interface = None

    def __init__(self, interface: str = None):
        self.interface(interface)

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """[summary].

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: [description]
        """
        # attempt to stop any active wpa_supplicant instances
        # ideally we do this just for the interface we care about
        cmd("sudo killall wpa_supplicant")

        # don't do DHCP for GoPros; can cause dropouts with the server
        cmd("sudo ifconfig {} 10.5.5.10/24 up".format(self._interface))

        # create configuration file
        f = open(self._file, "w")
        f.write('network={{\n    ssid="{}"\n    psk="{}"\n}}\n'.format(ssid, password))
        f.close()

        # attempt to connect
        cmd("sudo wpa_supplicant -i{} -c{} -B".format(self._interface, self._file))

        # check that the connection was successful
        # i've never seen it take more than 3 seconds for the link to establish
        time.sleep(5)
        current_ssid, _ = self.current()
        if current_ssid != ssid:
            return False

        # attempt to grab an IP
        # better hope we are connected because the timeout here is really long
        # cmd('sudo dhclient {}'.format(self._interface))

        # parse response
        return True

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """[summary].

        Returns:
            Tuple[Optional[str], Optional[str]]: [description]
        """
        # get interface status
        response = cmd("iwconfig {}".format(self.interface()))

        # the current network is on the first line like ESSID:"network"
        line = response.splitlines()[0]
        line = line.replace('"', "")
        parts = line.split("ESSID:")
        if len(parts) > 1:
            network = parts[1].strip()
            if network != "off/any":
                return (network, None)

        # return none if there was not an active connection
        return (None, None)

    def interfaces(self) -> List[str]:
        """[summary].

        Returns:
            List[str]: [description]
        """
        # grab list of interfaces
        response = cmd("iwconfig")

        # parse response
        interfaces = []
        for line in response.splitlines():
            if len(line) > 0 and not line.startswith(" "):
                # this line contains an interface name!
                if "no wireless extensions" not in line:
                    # this is a wireless interface
                    interfaces.append(line.split()[0])
        return interfaces

    def interface(self, interface: Optional[str] = None) -> Optional[str]:
        """[summary].

        Args:
            interface (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Optional[str]: [description]
        """
        if interface is not None:
            self._interface = interface
            return None
        return self._interface

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        # TODO
        return True

    def power(self, power: bool) -> None:
        """[summary].

        Args:
            power (bool): [description]
        """
        # TODO
        return


class NetworksetupWireless(WifiController):
    """OS X networksetup Driver."""

    _interface = None

    def __init__(self, interface: str = None):
        self.interface(interface)

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """[summary].

        Args:
            ssid (str): network SSID
            password (str): network password
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Raises:
            Exception: [description]

        Returns:
            bool: [description]
        """
        # Escape single quotes
        ssid = ssid.replace(r"'", '''"'"''')
        response = cmd(
            "networksetup -setairportnetwork '{}' '{}' '{}'".format(self._interface, ssid, password)
        )

        if "not find" in response.lower():
            return False
        # Now wait for network to actually establish
        current = self.current()[0]
        logger.debug(f"current wifi: {current}")
        while current is not None and ssid not in current and timeout < 10:
            time.sleep(1)
            current = self.current()[0]
            logger.debug(f"current wifi: {current}")
            timeout -= 1
            if timeout == 0:
                raise Exception("Wi-Fi connection timeout.")

        # TODO There is some delay required here, presumably because the network is not ready.
        time.sleep(5)

        return True

    def disconnect(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return False

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """[summary].

        Returns:
            Tuple[Optional[str], Optional[str]]: [description]
        """
        # attempt to get current network
        response = cmd("networksetup -getairportnetwork {}".format(self._interface))

        # parse response
        phrase = "Current Wi-Fi Network: "
        if phrase in response:
            return (response.replace("Current Wi-Fi Network: ", "").strip(), None)
        return (None, None)

    def interfaces(self) -> List[str]:
        """[summary].

        Returns:
            List[str]: [description]
        """
        # grab list of interfaces
        response = cmd("networksetup -listallhardwareports")

        # parse response
        interfaces = []
        detectedWifi = False
        for line in response.splitlines():
            if detectedWifi:
                # this line has our interface name in it
                interfaces.append(line.replace("Device: ", ""))
                detectedWifi = False
            else:
                # search for the line that has 'Wi-Fi' in it
                if "Wi-Fi" in line:
                    detectedWifi = True

        # return list
        return interfaces

    def interface(self, interface: Optional[str] = None) -> Optional[str]:
        """[summary].

        Args:
            interface (Optional[str], optional): [description]. Defaults to None.

        Returns:
            Optional[str]: [description]
        """
        if interface is not None:
            self._interface = interface
            return None
        return self._interface

    @property
    def is_on(self) -> bool:
        """[summary].

        Returns:
            bool: [description]
        """
        return "On" in cmd("networksetup -getairportpower {}".format(self._interface))

    def power(self, power: bool) -> None:
        """[summary].

        Args:
            power (bool): [description]
        """
        if power:
            cmd("networksetup -setairportpower {} on".format(self._interface))
        else:
            cmd("networksetup -setairportpower {} off".format(self._interface))


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

    def __init__(self, interface: str = None) -> None:
        self._interface: Optional[str] = None
        self.interface(interface)
        self.ssid: Optional[str] = None

    def __del__(self) -> None:
        # TODO Do we want this?
        # self._clean(self.ssid)
        pass

    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        """Establish a connection.

        This is blocking and won't return until either a connection is established or
        a 10 second timeout

        Args:
            ssid (str): SSID of network to connect to
            password (str): password of network to connect to
            timeout (float, optional): Time before considering connection failed (in seconds). Defaults to 15.

        Returns:
            bool: True if connected, False otherwise
        """
        # Replace ampersand as it causes problems
        password = password.replace("&", "&amp;")

        logger.info(f"Attempting to establish WiFi connection to {ssid}...")

        # Start fresh each time.
        self._clean(ssid)

        # Create new profile
        output = NetshWireless.template.format(ssid=ssid, auth="WPA2PSK", encrypt="AES", passwd=password)
        logger.debug(output)
        # Need ugly low level mkstemp and os here because standard tempfile can't be accessed by a subprocess in Windows :(
        fd, filename = tempfile.mkstemp()
        os.write(fd, output.encode("utf-8"))
        os.close(fd)
        response = cmd(f"netsh wlan add profile filename={filename}")
        if "is added on interface" not in response:
            raise Exception(response)
        os.remove(filename)

        # Try to connect
        ssid_quotes = f'"{ssid}"'
        response = cmd(f"netsh wlan connect ssid={ssid_quotes} name={ssid_quotes} interface={self._interface}")
        if "was completed successfully" not in response:
            raise Exception(response)

        while self.current() != (ssid, "connected"):
            logger.debug("Waiting 1 second for Wi-Fi connection to establish...")
            time.sleep(1)
            timeout -= 1
            if timeout == 0:
                raise Exception("Wi-Fi connection timeout.")

        logger.info("Wifi connection established!")
        self.ssid = ssid

        return True

    def disconnect(self) -> bool:
        """Terminate the WiFi connection.

        Returns:
            bool: True if the disconnect was successful, False otherwise.
        """
        response = cmd(f"netsh wlan disconnect interface={self.interface()}")

        return bool("completed successfully" in response.lower())

    def current(self) -> Tuple[Optional[str], Optional[str]]:
        """Get the current network SSID and state.

        # Here is an example of what we are parsing (i.e. to find FunHouse SSID):
        # Name                   : Wi-Fi
        # Description            : TP-Link Wireless USB Adapter
        # GUID                   : 093d8022-33cb-4400-8362-275eaf24cb86
        # Physical address       : 98:48:27:88:cb:18
        # State                  : connected
        # SSID                   : FunHouse

        Raises:
            Exception: Unexpected error.

        Returns:
            Tuple[Optional[str], Optional[str]]: Tuple of (ssid, network_state)
        """

        class ParseState(Enum):
            """Current state of interface parsing"""

            PARSE_INTERFACE = auto()
            PARSE_SSID = auto()
            PARSE_STATE = auto()

        if self.interface is None:
            self._interface = self.interfaces()[0]
        if self._interface is None:
            raise Exception("Can't auto-assign interface. None found.")

        response = cmd("netsh wlan show interfaces")
        parse_state = ParseState.PARSE_INTERFACE
        ssid: Optional[str] = None
        network_state: Optional[str] = None
        for field in response.split("\r\n"):
            if parse_state is ParseState.PARSE_INTERFACE:
                if "Name" in field and self._interface in field:
                    parse_state = ParseState.PARSE_STATE
            elif parse_state is ParseState.PARSE_STATE:
                if "State" in field:
                    network_state = field.split(":")[1].strip()
                    parse_state = ParseState.PARSE_SSID
            elif parse_state is ParseState.PARSE_SSID:
                if "SSID" in field:
                    ssid = field.split(":")[1].strip()
                    break

        return (ssid, network_state)

    def interfaces(self) -> List[str]:
        """Discover all available interfaces.

        # We're parsing, for example, the following line to find "Wi-Fi":
        # Name                   : Wi-Fi

        Returns:
            List[str]: List of interfaces
        """
        response = cmd("netsh wlan show interfaces")
        interfaces = []

        # Look behind to find field, then match (non-greedy) any chars until CRLF
        match = "(?<={}).+?(?=\\r\\n)"
        for interface in re.findall(match.format("Name"), response):
            # Strip leading whitespace and then the first two chars of remaining (i.e. " :")
            interfaces.append(interface.strip()[2:])

        return interfaces

    def interface(self, interface: str = None) -> Optional[str]:
        """Get or set the current interface.

        Args:
            interface (str, optional): String to set or None to get. Defaults to None.

        Returns:
            Optional[str]: If interface argument is None, this will be a string if there is a valid interface; otherwise None
        """
        if interface is not None:
            self._interface = interface
            return None
        return self._interface

    @property
    def is_on(self) -> bool:
        """Is Wifi enabled?

        Returns:
            bool: True if yes, False if no.
        """
        # TODO
        return True

    def power(self, power: bool) -> None:
        """Enable / Disable WiFi.

        Args:
            power (bool): True to enable, False to disable.
        """
        arg = "enable" if power is True else "disable"
        cmd(f"netsh interface set interface {self._interface} {arg}")

    @staticmethod
    def _clean(ssid: Optional[str]) -> None:
        """Disconnect and delete SSID profile.

        Args:
            ssid (Optional[str]): name of SSID
        """
        cmd("netsh wlan disconnect")
        if ssid is not None:
            cmd(f'netsh wlan delete profile name="{ssid}"')
