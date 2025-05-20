# test_access_point_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

import asyncio
from typing import Any

import pytest_asyncio
from returns.pipeline import is_successful
from returns.result import Result

import open_gopro.features
from open_gopro.domain.exceptions import GoProError
from open_gopro.features.access_point_feature import AccessPointFeature
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models.proto import (
    EnumProvisioning,
    EnumResultGeneric,
    EnumScanEntryFlags,
    EnumScanning,
    NotifProvisioningState,
    NotifStartScanning,
    ResponseConnect,
    ResponseConnectNew,
    ResponseGetApEntries,
    ResponseStartScanning,
)
from tests.mocks import MockGoproResp, MockObserver


@pytest_asyncio.fixture(loop_scope="function")
async def ap_feature(mock_wireless_gopro_basic: WirelessGoPro):
    feature = AccessPointFeature()
    await feature.open(
        gopro=mock_wireless_gopro_basic,
        loop=asyncio.get_running_loop(),
    )
    yield feature
    await feature.close()


def create_scan_entry(ssid: str, is_configured: bool = False) -> ResponseGetApEntries.ScanEntry:
    """Helper to create scan entries for testing"""
    flags = EnumScanEntryFlags.SCAN_FLAG_CONFIGURED if is_configured else 0
    return ResponseGetApEntries.ScanEntry(
        ssid=ssid,
        scan_entry_flags=flags,
    )


async def test_ap_feature_is_supported(ap_feature: AccessPointFeature):
    # AccessPointFeature is always supported
    assert ap_feature.is_supported


async def test_scan_wifi_networks_successful(ap_feature: AccessPointFeature, monkeypatch: Any):
    # GIVEN
    scan_entries = [
        create_scan_entry("TestNetwork1"),
        create_scan_entry("TestNetwork2", is_configured=True),
    ]
    # Mock BLE command response
    scan_id = 12345

    async def mock_scan_wifi_networks(*args: Any, **kwargs: Any) -> Any:
        return MockGoproResp(value=ResponseStartScanning(result=EnumResultGeneric.RESULT_SUCCESS))

    async def mock_get_ap_entries(*args: Any, **kwargs: Any) -> Any:
        return MockGoproResp(value=ResponseGetApEntries(entries=scan_entries))

    MockObserver.initial_response = ResponseStartScanning(result=EnumResultGeneric.RESULT_SUCCESS)
    MockObserver.first_response = NotifStartScanning(
        scanning_state=EnumScanning.SCANNING_SUCCESS,
        scan_id=scan_id,
    )

    # Apply mocks
    monkeypatch.setattr(ap_feature._gopro.ble_command, "scan_wifi_networks", mock_scan_wifi_networks)
    monkeypatch.setattr(ap_feature._gopro.ble_command, "get_ap_entries", mock_get_ap_entries)
    monkeypatch.setattr(open_gopro.features.access_point_feature, "GoproObserverDistinctInitial", MockObserver)

    # WHEN
    result = await ap_feature.scan_wifi_networks()

    # THEN
    assert is_successful(result)
    networks = result.unwrap()
    assert len(networks.entries) == 2
    assert networks.entries[0].ssid == "TestNetwork1"
    assert networks.entries[1].ssid == "TestNetwork2"
    assert networks.entries[1].scan_entry_flags & EnumScanEntryFlags.SCAN_FLAG_CONFIGURED


async def test_connect_to_configured_network(ap_feature: AccessPointFeature, monkeypatch: Any):
    # GIVEN
    test_ssid = "TestNetwork"
    test_password = "password123"
    scan_entries = [create_scan_entry(test_ssid, is_configured=True)]

    # Setup mocks for scan_wifi_networks
    async def mock_scan_wifi_networks(*args: Any, **kwargs: Any) -> Any:
        return Result.from_value(ResponseGetApEntries(entries=scan_entries))

    # Mock for request_wifi_connect
    async def mock_request_wifi_connect(*args: Any, **kwargs: Any) -> Any:
        return MockGoproResp(value=ResponseConnect(result=EnumResultGeneric.RESULT_SUCCESS))

    MockObserver.initial_response = ResponseConnect(result=EnumResultGeneric.RESULT_SUCCESS)
    MockObserver.first_response = NotifProvisioningState(
        provisioning_state=EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
    )

    # Apply mocks
    monkeypatch.setattr(ap_feature, "scan_wifi_networks", mock_scan_wifi_networks)
    monkeypatch.setattr(ap_feature._gopro.ble_command, "request_wifi_connect", mock_request_wifi_connect)
    monkeypatch.setattr(open_gopro.features.access_point_feature, "GoproObserverDistinctInitial", MockObserver)

    # WHEN
    result = await ap_feature.connect(test_ssid, test_password)

    # THEN
    assert is_successful(result)


async def test_connect_to_new_network(ap_feature: AccessPointFeature, monkeypatch: Any):
    # GIVEN
    test_ssid = "NewNetwork"
    test_password = "newpassword123"
    scan_entries = [create_scan_entry(test_ssid, is_configured=False)]

    # Setup mocks for scan_wifi_networks
    async def mock_scan_wifi_networks(*args: Any, **kwargs: Any) -> Any:
        from returns.result import Result

        return Result.from_value(ResponseGetApEntries(entries=scan_entries))

    # Mock for request_wifi_connect_new
    async def mock_request_wifi_connect_new(*args: Any, **kwargs: Any) -> Any:
        return ResponseConnectNew(result=EnumResultGeneric.RESULT_SUCCESS)

    MockObserver.initial_response = ResponseConnectNew(result=EnumResultGeneric.RESULT_SUCCESS)
    MockObserver.first_response = NotifProvisioningState(
        provisioning_state=EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
    )

    # Apply mocks
    monkeypatch.setattr(ap_feature, "scan_wifi_networks", mock_scan_wifi_networks)
    monkeypatch.setattr(ap_feature._gopro.ble_command, "request_wifi_connect_new", mock_request_wifi_connect_new)
    monkeypatch.setattr(open_gopro.features.access_point_feature, "GoproObserverDistinctInitial", MockObserver)

    # WHEN
    result = await ap_feature.connect(test_ssid, test_password)

    # THEN
    assert is_successful(result)


async def test_connect_failure_network_not_found(ap_feature: AccessPointFeature, monkeypatch: Any):
    # GIVEN
    test_ssid = "NonexistentNetwork"
    test_password = "password123"
    scan_entries = [create_scan_entry("DifferentNetwork")]

    # Setup mocks for scan_wifi_networks
    async def mock_scan_wifi_networks(*args: Any, **kwargs: Any) -> Any:
        from returns.result import Result

        return Result.from_value(ResponseGetApEntries(entries=scan_entries))

    # Apply mocks
    monkeypatch.setattr(ap_feature, "scan_wifi_networks", mock_scan_wifi_networks)

    # WHEN
    result = await ap_feature.connect(test_ssid, test_password)

    # THEN
    assert not is_successful(result)
    assert "Could not find SSID" in str(result.failure())


async def test_connect_failure_scan_failed(ap_feature: AccessPointFeature, monkeypatch: Any):
    # GIVEN
    test_ssid = "TestNetwork"
    test_password = "password123"

    # Setup mocks for scan_wifi_networks to fail
    async def mock_scan_wifi_networks_fail(*args: Any, **kwargs: Any) -> Any:
        return Result.from_failure(GoProError("Scanning failed"))

    # Apply mocks
    monkeypatch.setattr(ap_feature, "scan_wifi_networks", mock_scan_wifi_networks_fail)

    # WHEN
    result = await ap_feature.connect(test_ssid, test_password)

    # THEN
    assert not is_successful(result)
    assert "Scanning for SSID's failed" in str(result.failure())
