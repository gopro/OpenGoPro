# test_cohn_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

import asyncio

import pytest
import pytest_asyncio
from returns.pipeline import is_successful
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from open_gopro.features.cohn_feature import CohnFeature
from open_gopro.gopro_wireless import WirelessGoPro
from open_gopro.models.general import CohnInfo
from open_gopro.models.proto.cohn_pb2 import (
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
    cohn = CohnFeature(cohn_db=TinyDB(storage=MemoryStorage))
    await cohn.open(
        gopro=mock_wireless_gopro_basic,
        loop=asyncio.get_running_loop(),
        cohn_credentials=cohn_credentials,
    )
    async with asyncio.TaskGroup() as tg:
        tg.create_task(cohn.wait_until_ready())
        tg.create_task(cohn._status_observable.emit(NotifyCOHNStatus()))
    yield cohn
    await cohn.close()


async def test_cohn_feature_starts_successfully(cohn_feature: CohnFeature):
    # THEN
    assert cohn_feature.is_supported


async def test_cohn_feature_is_configured(cohn_feature: CohnFeature):
    # WHEN
    await cohn_feature._status_observable.emit(provisioned_status)

    # THEN
    assert await cohn_feature.is_configured


async def test_cohn_feature_configure_without_provisioning(cohn_feature: CohnFeature):
    # WHEN
    await cohn_feature._status_observable.emit(provisioned_status)
    await cohn_feature._status_observable.emit(connected_status)

    result = await cohn_feature.configure()

    # THEN
    assert is_successful(result)
    assert result.unwrap() == cohn_credentials


async def test_cohn_feature_provision(cohn_feature: CohnFeature):
    # WHEN
    await cohn_feature._status_observable.emit(unprovisioned_status)

    async def send_cohn_provisioned():
        await cohn_feature._status_observable.emit(connected_status)

    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(send_cohn_provisioned())
        configure_task = task_group.create_task(cohn_feature.configure())
    result = configure_task.result()

    # THEN
    assert is_successful(result)
    assert result.unwrap() == cohn_credentials
