# test_Wirelessgopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://Wirelessgopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Sep 10 01:35:03 UTC 2021

# pylint: disable=redefined-outer-name


"""Unit testing of GoPro Client"""

import asyncio
from dataclasses import dataclass
from typing import Final

import pytest

from open_gopro import WiredGoPro
from open_gopro.models import DnsScanResponse
from open_gopro.models.constants import statuses
from open_gopro.network.wifi.mdns_scanner import ZeroconfListener, find_first_ip_addr


async def test_mdns_scan(monkeypatch):
    # GIVEN
    ip_addr = "172.20.123.51"

    @dataclass
    class MockServiceInfo:
        def parsed_addresses(self, *args, **kwargs):
            return [ip_addr]

    class MockZeroconf:
        def __init__(self, *args, **kwargs) -> None:
            pass

        def __enter__(self, *args, **kwargs):
            return self

        def __exit__(self, *args, **kwargs):
            pass

        def get_service_info(self, *args, **kwargs):
            return MockServiceInfo()

        def close(self): ...

    class MockAsyncZeroConf:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def __aenter__(self, *args, **kwargs):
            return self

        async def __aexit__(self, *args, **kwargs): ...

        async def async_get_service_info(*args, **kwargs):
            return MockServiceInfo()

    class MockServiceBrowser:
        def __init__(self, zc: MockZeroconf, service_name: str, listener: ZeroconfListener) -> None:
            self.service_name = service_name
            listener.urls.put_nowait("result")

        def cancel(self): ...

    monkeypatch.setattr("zeroconf.Zeroconf", MockZeroconf)
    monkeypatch.setattr("zeroconf.asyncio.AsyncServiceBrowser", MockServiceBrowser)
    monkeypatch.setattr("zeroconf.asyncio.AsyncZeroconf", MockAsyncZeroConf)
    assert (await find_first_ip_addr("service")).ip_addr == ip_addr


async def test_wired_lifecycle(mock_wired_gopro: WiredGoPro, monkeypatch):
    # GIVEN
    ip_addr = "172.27.111.51"
    serial_number = "C3501324500711"

    class MockMdnsScanner:
        async def find_first_ip_addr(self, *args, **kwargs) -> DnsScanResponse:
            return DnsScanResponse(
                args[0],
                ip_addr,
                f"{serial_number}._gopro-web._tcp.local.",
            )

    async def set_ready():
        await asyncio.sleep(1)  # Allow initial poll to fail
        mock_wired_gopro.set_state_response(  # type: ignore
            {
                statuses.StatusId.ENCODING: 0,
                statuses.StatusId.BUSY: 0,
            }
        )

    monkeypatch.setattr("open_gopro.network.wifi.mdns_scanner", MockMdnsScanner)
    await asyncio.gather(mock_wired_gopro.open(), set_ready())
    assert mock_wired_gopro.is_open
    assert await mock_wired_gopro.is_ready
    assert mock_wired_gopro.identifier == serial_number
    assert mock_wired_gopro._base_url == f"http://{ip_addr}:8080/"
