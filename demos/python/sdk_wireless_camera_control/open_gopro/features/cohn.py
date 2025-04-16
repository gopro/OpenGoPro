from __future__ import annotations

import asyncio
import logging
from math import e
from pathlib import Path
from typing import Any

from returns.pipeline import is_successful
from returns.result import Result
from tinydb import TinyDB

from open_gopro.api.api import WirelessApi
from open_gopro.api.status_flow import StatusFlow
from open_gopro.constants import ActionId
from open_gopro.db import CohnDb
from open_gopro.exceptions import GoProNotOpened
from open_gopro.features.base_feature import BaseFeature
from open_gopro.gopro_base import GoProBase
from open_gopro.models.general import CohnInfo
from open_gopro.proto import EnumCOHNStatus, NotifyCOHNStatus
from open_gopro.proto.cohn_pb2 import EnumCOHNNetworkState

logger = logging.getLogger(__name__)


class CohnFeature(BaseFeature):
    def __init__(
        self,
        cohn_db_path: Path,
        gopro: GoProBase[WirelessApi],
        loop: asyncio.AbstractEventLoop,
        cohn_credentials: CohnInfo | None = None,
    ) -> None:
        super().__init__(gopro, loop)
        self._db = CohnDb(TinyDB(cohn_db_path))
        if cohn_credentials:
            self._db.insert_or_update_credentials(self._gopro.identifier, cohn_credentials)
        self.credentials = self._db.search_credentials(self._gopro.identifier)
        # TODO close this
        self._status_flow = StatusFlow(
            gopro=self._gopro,
            update=ActionId.RESPONSE_GET_COHN_STATUS,
            register_command=self._gopro.ble_command.cohn_get_status(register=True),
        )
        self._status_task: asyncio.Task = asyncio.create_task(self._track_status())
        self._ready_event = asyncio.Event()

    def close(self) -> None:
        self._status_task.cancel()
        print("cancelled")

    async def _track_status(self) -> None:
        while True:
            if self._gopro.is_ble_connected:
                async with self._status_flow.on_start(lambda _: self._ready_event.set()) as flow:

                    async def process_status(status: NotifyCOHNStatus) -> None:
                        logger.debug(f"Received COHN status: {status}")

                    await flow.collect(process_status)
            else:
                await asyncio.sleep(1)

    @property
    def status(self) -> NotifyCOHNStatus:
        if not self.is_ready:
            raise GoProNotOpened("COHN feature is not yet ready")
        else:
            assert self._status_flow.current
            return self._status_flow.current

    @property
    def is_ready(self) -> bool:
        return self._ready_event.is_set()

    async def wait_for_ready(self, timeout: float = 60) -> None:
        await asyncio.wait_for(self._ready_event.wait(), timeout)

    @property
    async def is_configured(self) -> bool:
        # TODO validate cohn credentials are all set?
        if bool(self.credentials):
            # Validate COHN
            try:
                return (await self._gopro.http_command.get_open_gopro_api_version()).ok
            except Exception as e:
                logger.error(repr(e))
        return False

    async def _provision_cohn(self, timeout: int = 60) -> Result[CohnInfo, TimeoutError]:
        """Provision the camera for Camera on the Home Network

        Args:
            timeout (int): time in seconds to wait for provisioning success

        Returns:
            bool: True if success, False otherwise
        """
        if not self._gopro.is_ble_connected:
            raise RuntimeError("COHN needs to be provisioned but BLE is not connected")

        logger.info("Provisioning COHN")
        # Always override. Assume if we're here, we are purposely (re)configuring COHN
        assert (await self._gopro.ble_command.cohn_create_certificate(override=True)).ok

        try:
            logger.debug("Waiting for COHN to provision")
            status = await asyncio.wait_for(
                self._status_flow.first(lambda status: status.status == EnumCOHNStatus.COHN_PROVISIONED),
                timeout,
            )
            logger.info("COHN is provisioned!!")

            cert = (await self._gopro.ble_command.cohn_get_certificate()).data.cert
            credentials = CohnInfo(
                ip_address=status.ipaddress,
                username=status.username,
                password=status.password,
                certificate=cert,
            )
            return Result.from_value(credentials)
        except TimeoutError as e:
            return Result.from_failure(e)

    async def configure(self, timeout: int = 60) -> Result[CohnInfo, RuntimeError | TimeoutError]:
        """Prepare Camera on the Home Network

        Provision if not provisioned
        Then wait for COHN to be connected and ready

        Args:
            timeout (int): time in seconds to wait for COHN to be ready. Defaults to 60.

        Returns:
            bool: True if success, False otherwise
        """
        # TODO verify connected to AP?

        # If we don't have credentials or peer isn't provisioned, we need to (re)provision
        if not self.is_configured:
            if is_successful(result := await self._provision_cohn()):
                self.credentials = result.unwrap()  # TODO make this a property with a setter to write to DB
                self._db.insert_or_update_credentials(self._gopro.identifier, self.credentials)
            else:
                return result
        try:
            logger.info("Waiting for COHN to be connected")
            await asyncio.wait_for(
                self._status_flow.first(
                    lambda status: status.state == EnumCOHNNetworkState.COHN_STATE_NetworkConnected
                ),
                timeout,
            )
            assert self.credentials
            return Result.from_value(self.credentials)
        except TimeoutError as e:
            return Result.from_failure(e)
