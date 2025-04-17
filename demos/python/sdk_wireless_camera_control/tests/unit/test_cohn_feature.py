import asyncio

import pytest
import pytest_asyncio
from returns.pipeline import is_successful
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


from open_gopro.features.cohn import CohnFeature
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models.general import CohnInfo
from open_gopro.proto.cohn_pb2 import (
    EnumCOHNNetworkState,
    EnumCOHNStatus,
    NotifyCOHNStatus,
)

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
async def cohn_feature(mock_wireless_gopro_basic: WirelessGoPro):
    cohn = CohnFeature(
        cohn_db=TinyDB(storage=MemoryStorage),
        gopro=mock_wireless_gopro_basic,
        loop=asyncio.get_running_loop(),
        cohn_credentials=cohn_credentials,
    )
    yield cohn
    cohn.close()


@pytest.mark.asyncio
async def test_cohn_feature_starts_successfully(cohn_feature: CohnFeature):
    # WHEN
    async def send_cohn_status():
        await cohn_feature._status_flow._flow_manager.emit(NotifyCOHNStatus())

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_cohn_status())
        task_group.create_task(cohn_feature.wait_for_ready())

    # THEN
    assert cohn_feature.is_ready


@pytest.mark.asyncio
async def test_cohn_feature_start_times_out(cohn_feature: CohnFeature):
    # WHEN / THEN
    with pytest.raises(TimeoutError):
        await cohn_feature.wait_for_ready(timeout=0.1)


@pytest.mark.asyncio
async def test_cohn_feature_is_configured(cohn_feature: CohnFeature):
    # WHEN
    async def send_cohn_status():
        await cohn_feature._status_flow._flow_manager.emit(provisioned_status)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(send_cohn_status())
        tg.create_task(cohn_feature.wait_for_ready())

    # THEN
    assert cohn_feature.is_ready
    assert await cohn_feature.is_configured


@pytest.mark.asyncio
async def test_cohn_feature_configure_without_provisioning(cohn_feature: CohnFeature):
    # WHEN
    async def send_cohn_status():
        await cohn_feature._status_flow._flow_manager.emit(provisioned_status)
        await cohn_feature._status_flow._flow_manager.emit(connected_status)

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_cohn_status())
        task_group.create_task(cohn_feature.wait_for_ready())

    result = await cohn_feature.configure()

    # THEN
    assert is_successful(result)
    assert result.unwrap() == cohn_credentials


@pytest.mark.asyncio
async def test_cohn_feature_provision(cohn_feature: CohnFeature):
    # WHEN
    async def send_cohn_unprovisioned():
        await cohn_feature._status_flow._flow_manager.emit(unprovisioned_status)

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_cohn_unprovisioned())
        task_group.create_task(cohn_feature.wait_for_ready())

    async def send_cohn_provisioned():
        await cohn_feature._status_flow._flow_manager.emit(connected_status)

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_cohn_provisioned())
        configure_task = task_group.create_task(cohn_feature.configure())
    result = configure_task.result()

    # THEN
    assert is_successful(result)
    assert result.unwrap() == cohn_credentials
