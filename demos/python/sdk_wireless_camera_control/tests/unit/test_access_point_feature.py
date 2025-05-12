# test_access_point_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from returns.pipeline import is_successful

from open_gopro.features.access_point_feature import AccessPointFeature
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models.general import CohnInfo
from open_gopro.models.proto.cohn_pb2 import (
    EnumCOHNNetworkState,
    EnumCOHNStatus,
    NotifyCOHNStatus,
)
from open_gopro.models.proto.network_management_pb2 import (
    NotifStartScanning,
    ResponseStartScanning,
)
from open_gopro.models.proto.response_generic_pb2 import EnumResultGeneric

provisioned_status = NotifyCOHNStatus(status=EnumCOHNStatus.COHN_PROVISIONED)
unprovisioned_status = NotifyCOHNStatus(status=EnumCOHNStatus.COHN_UNPROVISIONED)
connected_status = NotifyCOHNStatus(
    status=EnumCOHNStatus.COHN_PROVISIONED,
    state=EnumCOHNNetworkState.COHN_STATE_NetworkConnected,
    ipaddress="ip",
    username="user",
    password="password",
)
cohn_credentials = CohnInfo(ip_address="ip", username="user", password="password", certificate="cert")


@pytest_asyncio.fixture(loop_scope="function")
async def ap_feature(mock_wireless_gopro_basic: WirelessGoPro):
    feature = AccessPointFeature(mock_wireless_gopro_basic, asyncio.get_running_loop())
    yield feature
    feature.close()


@pytest.mark.asyncio
async def test_ap_feature_starts_successfully(ap_feature: AccessPointFeature):
    await ap_feature.wait_for_ready()
    assert ap_feature.is_ready
