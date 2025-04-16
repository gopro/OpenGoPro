import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from returns.pipeline import is_successful

from open_gopro.features.access_point import AccessPointFeature
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models.general import CohnInfo
from open_gopro.proto.cohn_pb2 import (
    EnumCOHNNetworkState,
    EnumCOHNStatus,
    NotifyCOHNStatus,
)
from open_gopro.proto.network_management_pb2 import (
    NotifStartScanning,
    ResponseStartScanning,
)
from open_gopro.proto.response_generic_pb2 import EnumResultGeneric

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


# TODO. We need to monkey patch status flow...
# @pytest.mark.asyncio
# async def test_ap_feature_scan(ap_feature: AccessPointFeature):
#     # GIVEN
#     scan_response = ResponseStartScanning(result=EnumResultGeneric.RESULT_SUCCESS)
#     scan_notification = NotifStartScanning(scan_id=9)

#     # WHEN
#     async def send_scanning_success():
#         await ap_feature._status_flow._flow_manager.emit(unprovisioned_status)

#     async with asyncio.TaskGroup() as task_group:
#         task_group.create_task(send_scanning_success())
#         task_group.create_task(ap_feature.sc)

#     assert not ap_feature.is_configured

#     async def send_cohn_provisioned():
#         await ap_feature._status_flow._flow_manager.emit(connected_status)

#     async with asyncio.TaskGroup() as task_group:
#         task_group.create_task(send_cohn_provisioned())
#         configure_task = task_group.create_task(ap_feature.configure())
#     result = configure_task.result()

#     # THEN
#     assert is_successful(result)
#     assert result.unwrap() == cohn_credentials
