from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Any
import logging

from tinydb import TinyDB
from returns.result import Success, Failure, Result
from returns.pipeline import is_successful

from open_gopro.api.api import WirelessApi
from open_gopro.flow import Flow, FlowManager
from open_gopro.gopro_base import GoProBase
from open_gopro.proto import EnumCOHNStatus, NotifyCOHNStatus
from open_gopro.constants import ActionId
from open_gopro.db import CohnDb
from open_gopro.models.general import CohnInfo
from open_gopro.proto.cohn_pb2 import EnumCOHNNetworkState

logger = logging.getLogger(__name__)


class CohnFeature:
    def __init__(
        self,
        cohn_db_path: Path,
        gopro: GoProBase[WirelessApi],
        loop: asyncio.AbstractEventLoop,
        cohn_credentials: CohnInfo | None = None,
    ) -> None:
        self._loop = loop
        self._gopro = gopro
        self._db = CohnDb(TinyDB(cohn_db_path))
        if cohn_credentials:
            self._db.insert_or_update_credentials(self._gopro.identifier, cohn_credentials)
        self.credentials = self._db.search_credentials(self._gopro.identifier)
        # TODO close this
        self._status_task = asyncio.ensure_future(self._track_cohn_status())
        self._status_flow_filler: FlowManager[NotifyCOHNStatus] = FlowManager()
        self._status_flow = self.get_status_flow()

    def get_status_flow(self) -> Flow[NotifyCOHNStatus]:
        return Flow(self._status_flow_filler)

    async def _track_cohn_status(self) -> None:
        async def wait_for_cohn_ready(_: Any, status: NotifyCOHNStatus) -> None:
            await self._status_flow_filler.emit(status)

        self._gopro.register_update(wait_for_cohn_ready, ActionId.RESPONSE_GET_COHN_STATUS)
        await self._gopro.ble_command.cohn_get_status(register=True)

    @property
    def is_ready(self) -> bool:
        # TODO validate cohn credentials are all set?
        return bool(self.credentials)

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
        if not self.credentials or not await self._is_peer_provisioned:
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

    @property
    async def _is_peer_provisioned(self) -> bool:
        """Is COHN currently provisioned?

        Get the current COHN status from the camera

        Returns:
            bool: True if COHN is provisioned, False otherwise
        """
        return self._status_flow.current == EnumCOHNStatus.COHN_PROVISIONED
