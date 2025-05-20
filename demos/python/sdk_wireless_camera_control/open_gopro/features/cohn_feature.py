# cohn_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Camera on the home network (COHN) feature abstraction."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from returns.pipeline import is_successful
from returns.result import Result
from tinydb import TinyDB

from open_gopro.database.cohn_db import CohnDb
from open_gopro.domain.exceptions import GoProError, GoProNotOpened
from open_gopro.domain.gopro_observable import GoProObservable
from open_gopro.features.base_feature import BaseFeature, require_supported
from open_gopro.gopro_base import GoProBase
from open_gopro.models import proto
from open_gopro.models.constants import ActionId
from open_gopro.models.constants.constants import FeatureId
from open_gopro.models.general import CohnInfo
from open_gopro.models.proto import EnumCOHNNetworkState, EnumCOHNStatus
from open_gopro.models.proto.cohn_pb2 import NotifyCOHNStatus
from open_gopro.models.types import ProtobufId

logger = logging.getLogger(__name__)


class CohnFeature(BaseFeature):
    """Camera on the home network (COHN) feature abstraction"""

    def __init__(self, cohn_db: TinyDB) -> None:
        super().__init__()
        self._gopro: GoProBase[Any] | None = None  # type: ignore # TODO fix this.
        self._db = CohnDb(cohn_db)
        self._ready_event: asyncio.Event
        self._status_observable: GoProObservable[NotifyCOHNStatus]
        self._status_task: asyncio.Task | None = None
        self._supported: bool | None = None

    @property
    def is_supported(self) -> bool:  # noqa: D102
        if self._supported is None:
            raise RuntimeError("COHN feature is not yet ready")
        return self._supported

    async def open(  # pylint: disable=arguments-differ
        self,
        loop: asyncio.AbstractEventLoop,
        gopro: GoProBase[Any],
        *args: Any,
        cohn_credentials: CohnInfo | None = None,
        **kwargs: Any,
    ) -> None:  # noqa: D102
        self._supported = None  # Wait for this to be updated
        logger.debug("Opening COHN")
        await super().open(loop, gopro, *args, **kwargs)
        assert self._gopro
        if cohn_credentials:
            self.credentials = cohn_credentials
        self._ready_event = asyncio.Event()
        self._status_observable = GoProObservable(
            gopro=self._gopro,
            update=ProtobufId(FeatureId.QUERY, ActionId.RESPONSE_GET_COHN_STATUS),
            register_command=self._gopro.ble_command.cohn_get_status(register=True),
        ).on_start(lambda _: self._ready_event.set())
        self._status_task = asyncio.create_task(self._track_status())
        logger.debug("COHN opened")

    async def wait_until_ready(self) -> None:
        """Wait until COHN is ready (the first status is received)"""
        logger.debug("Waiting for COHN to be ready")
        await asyncio.wait_for(self._ready_event.wait(), 30)

    async def close(self) -> None:  # noqa: D102
        if self._status_task and not self._status_task.done():
            logger.debug("Closing COHN")
            await self._status_observable.stop()
            self._status_task.cancel()
            try:
                await self._status_task
            except asyncio.CancelledError:
                pass  # This exception is expected when cancelling a task
            self._status_task = None
            logger.debug("COHN closed")

    async def _track_status(self) -> None:
        """Task to continuously monitor COHN status"""
        while True:
            assert self._gopro, "not yet open"
            if self._gopro.is_ble_connected:
                try:
                    logger.debug("Starting COHN status tracking")
                    async with self._status_observable as observable:
                        self._supported = True
                        async for status in observable.observe(debug_id="Cohn Feature"):
                            logger.debug(f"Feature Received COHN status: {status}")
                except GoProError as exc:
                    logger.warning(f"Failed to start COHN feature: {str(exc)}")
                    self._supported = False
                    self._ready_event.set()
            else:
                await asyncio.sleep(1)

    @property
    def credentials(self) -> CohnInfo | None:
        """The camera's COHN credentials

        Returns:
            CohnInfo | None: Credentials if they exist or None if they have not yet been discovered
        """
        if not self._gopro:
            return None
        return self._db.search_credentials(self._gopro.identifier)

    @credentials.setter
    def credentials(self, new_credentials: CohnInfo) -> None:
        if not self._gopro:
            raise GoProNotOpened("COHN feature is not yet ready")
        self._db.insert_or_update_credentials(self._gopro.identifier, new_credentials)

    @property
    @require_supported
    def status(self) -> proto.NotifyCOHNStatus:
        """The current COHN status

        Raises:
            GoProNotOpened: There is no status yet because the camera is not yet ready.

        Returns:
            proto.NotifyCOHNStatus: The current COHN status
        """
        if not self._status_observable.current:
            raise GoProNotOpened("COHN feature is not yet ready")
        return self._status_observable.current

    @property
    async def is_configured(self) -> bool:
        """Is COHN ready for communication?

        This will check if there are credentials and that validate that a basic HTTP operations works.

        Returns:
            bool: True if configured, False otherwise
        """
        return bool(self.credentials and self.credentials.is_complete)

    @property
    @require_supported
    def is_connected(self) -> bool:
        """Is COHN connected to an Access Point?

        Returns:
            bool: True if connected, False otherwise
        """
        return self.status.state == EnumCOHNNetworkState.COHN_STATE_NetworkConnected

    @property
    @require_supported
    def _is_provisioned(self) -> bool:
        """Is COHN provisioned?

        Returns:
            bool: True if provisioned, False otherwise
        """
        return self.status.status == EnumCOHNStatus.COHN_PROVISIONED

    @require_supported
    async def _provision_cohn(self, timeout: int = 60) -> Result[CohnInfo, TimeoutError]:
        """Provision the camera, clearing any current certificate and forcing reprovision

        Args:
            timeout (int): How long in seconds to wait before considering the provision a failure.
                Defaults to 60.

        Raises:
            GoProNotOpened: BLE is not available

        Returns:
            Result[CohnInfo, TimeoutError]: COHN Credentials if provisioning succeeds, otherwise an error
        """
        assert self._gopro, "Not yet open"
        if not self._gopro.is_ble_connected:
            raise GoProNotOpened("COHN needs to be provisioned but BLE is not connected")

        logger.info("Provisioning COHN")
        try:
            async with asyncio.timeout(timeout):
                # Start fresh by clearing cert and wait until we receive unprovisioned status
                await self._gopro.ble_command.cohn_clear_certificate()
                await self._status_observable.observe().first(
                    lambda status: status.status == EnumCOHNStatus.COHN_UNPROVISIONED
                )
                logger.info("COHN has been unprovisioned")

                # Reprovision and wait until we receive provisioned status
                assert (await self._gopro.ble_command.cohn_create_certificate(override=True)).ok
                status = await self._status_observable.observe().first(
                    lambda status: status.status == EnumCOHNStatus.COHN_PROVISIONED
                )
                logger.info("COHN has been successfully provisioned!!")

                cert = (await self._gopro.ble_command.cohn_get_certificate()).data.cert
                credentials = CohnInfo(
                    ip_address=status.ipaddress,
                    username=status.username,
                    password=status.password,
                    certificate=cert,
                )
                self.credentials = credentials
                return Result.from_value(credentials)
        except TimeoutError as exc:
            return Result.from_failure(exc)

    @require_supported
    async def configure(
        self,
        force_reprovision: bool = False,
        timeout: int = 60,
    ) -> Result[CohnInfo, RuntimeError | TimeoutError]:
        """Prepare Camera on the Home Network

        Provision if not provisioned
        Then wait for COHN to be connected and ready

        Args:
            force_reprovision (bool): Set to True to force reprovisioning. Defaults to False.
            timeout (int): time in seconds to wait for COHN to be ready. Defaults to 60.

        Returns:
            Result[CohnInfo, RuntimeError | TimeoutError]: _description_
        """
        # If we don't have credentials or peer isn't provisioned, we need to (re)provision
        if force_reprovision or not await self.is_configured:
            if not is_successful(result := await self._provision_cohn()):
                return result
        # We should at least have incomplete credentials after provisioning
        assert self.credentials
        try:
            if not self.is_connected:
                logger.info("Waiting for COHN to be connected")

                async with asyncio.timeout(timeout):
                    await self._status_observable.observe().first(
                        lambda s: s.state == EnumCOHNNetworkState.COHN_STATE_NetworkConnected
                    )

            logger.info("COHN is connected")
            # On some cameras, the IP address only comes with this status. Let's just always take all of the available
            # information from the current status which was potentially just retrieved from connecting.
            self.credentials = CohnInfo(
                username=self.status.username,
                password=self.status.password,
                ip_address=self.status.ipaddress,
                certificate=self.credentials.certificate,
            )

        except TimeoutError as exc:
            return Result.from_failure(exc)
        # If the credentials are still not complete at this point, something bad has happened
        if not self.credentials.is_complete:
            logger.error("Failed to get COHN credentials")
            return Result.from_failure(RuntimeError("Failed to get COHN credentials"))
        logger.info("COHN is provisioned, connected, and ready for communication")
        return Result.from_value(self.credentials)
