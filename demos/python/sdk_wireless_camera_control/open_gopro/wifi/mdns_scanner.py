# mdns_scanner.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Aug  8 18:10:56 UTC 2023

"""MDNS utility functions"""

import asyncio
import logging
from typing import Any

import zeroconf

# Imported this way for monkeypatching in pytest
import zeroconf.asyncio

from open_gopro import exceptions as GpException

logger = logging.getLogger(__name__)


class ZeroconfListener(zeroconf.ServiceListener):
    """Listens for mDNS services on the local system and save fully-formed ipaddr URLs"""

    def __init__(self) -> None:
        self.urls: asyncio.Queue[str] = asyncio.Queue()

    def add_service(self, zc: zeroconf.Zeroconf, type_: str, name: str) -> None:
        """Callback called by ServiceBrowser when a new service is discovered

        Args:
            zc (Zeroconf): instantiated zeroconf object that owns the search
            type_ (str): name of mDNS service that search is occurring on
            name (str): discovered device
        """
        logger.debug(f"Found MDNS service {name}")
        self.urls.put_nowait(name)

    def update_service(self, *_: Any) -> None:
        """Not used

        Args:
            *_ (Any): not used
        """

    def remove_service(self, *_: Any) -> None:
        """Not used

        Args:
            *_ (Any): not used
        """


async def find_first_ip_addr(service: str, timeout: int = 5) -> str:
    """Query the mDNS server to find a an IP address matching a service

    The first IP address matching the service will be returned

    Args:
        service (str): service name to scan for
        timeout (int): how long to search for before timing out in seconds

    Raises:
        FailedToFindDevice: search timed out

    Returns:
        str: First discovered IP address matching service
    """
    logger.info(f"Querying mDNS to find {service}...")
    listener = ZeroconfListener()
    with zeroconf.Zeroconf(unicast=True) as zc:
        zeroconf.asyncio.AsyncServiceBrowser(zc, service, listener)
        try:
            name = await asyncio.wait_for(listener.urls.get(), timeout)
            async with zeroconf.asyncio.AsyncZeroconf(unicast=True) as azc:
                if info := await azc.async_get_service_info(service, name):
                    ip_addr = info.parsed_addresses()[0]
                    return ip_addr
                raise GpException.FailedToFindDevice()
        except Exception as e:
            raise GpException.FailedToFindDevice() from e


async def get_all_services() -> list[str]:
    """Get all service names

    Returns:
        tuple[str, ...]: tuple of service names
    """
    return list(await zeroconf.asyncio.AsyncZeroconfServiceTypes.async_find())
