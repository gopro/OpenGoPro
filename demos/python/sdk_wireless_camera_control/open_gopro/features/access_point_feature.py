# access_point_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Access Point (AP) Feature Abstraction."""

import asyncio
import logging

from returns.pipeline import is_successful
from returns.result import Result

from open_gopro.domain.exceptions import GoProError, ResponseTimeout
from open_gopro.domain.gopro_observable import GoproObserverDistinctInitial
from open_gopro.features.base_feature import BaseFeature
from open_gopro.models import proto
from open_gopro.models.constants import ActionId
from open_gopro.models.constants.constants import FeatureId
from open_gopro.models.proto import (
    EnumProvisioning,
    EnumResultGeneric,
    EnumScanEntryFlags,
    EnumScanning,
    NotifProvisioningState,
    NotifStartScanning,
    ResponseConnect,
    ResponseConnectNew,
    ResponseStartScanning,
)
from open_gopro.models.types import ProtobufId

logger = logging.getLogger(__name__)


class AccessPointFeature(BaseFeature):
    """Access Point (AP) feature abstraction"""

    @property
    def is_supported(self) -> bool:  # noqa: D102
        # All Open GoPro cameras support access point
        return True

    async def close(self) -> None:  # noqa: D102
        return

    async def scan_wifi_networks(self, timeout: int = 60) -> Result[proto.ResponseGetApEntries, GoProError]:
        """Instruct the camera to scan for WiFi networks

        Args:
            timeout (int): How long (in seconds) to attempt to connect before considering the connection a
                failure. Defaults to 60.

        Returns:
            Result[proto.ResponseGetApEntries, GoProError]: Discovered AP entries on success or error
        """
        # Wait to receive scanning success
        logger.info("Scanning for Wifi networks...")

        async with GoproObserverDistinctInitial[ResponseStartScanning, NotifStartScanning](
            gopro=self._gopro,
            update=ProtobufId(FeatureId.NETWORK_MANAGEMENT, ActionId.NOTIF_START_SCAN),
            register_command=self._gopro.ble_command.scan_wifi_networks(),
        ) as observable, asyncio.timeout(timeout):
            if observable.initial_response.result != EnumResultGeneric.RESULT_SUCCESS:
                return Result.from_failure(GoProError("Failed to start scanning."))

            logger.info("Waiting for scanning to complete...")
            result = await observable.observe().first(lambda s: s.scanning_state == EnumScanning.SCANNING_SUCCESS)
            entries = await self._gopro.ble_command.get_ap_entries(scan_id=result.scan_id)
            logger.info(f"Scan complete. Found {len(entries.data.entries)} networks.")
            return Result.from_value(entries.data)

    async def connect(
        self, ssid: str, password: str, timeout: int = 60
    ) -> Result[None, ResponseTimeout | GoProError | RuntimeError]:
        """Connect the camera to a Wifi Access Point

        Args:
            ssid (str): SSID of AP
            password (str): password of AP
            timeout (int): How long (in seconds) to attempt to connect before considering the connection a
                failure. Defaults to 60.

        Returns:
            Result[None, ResponseTimeout | GoProError | RuntimeError]: None if successful, otherwise an error.
        """
        # Get scan results and see if we need to provision
        if is_successful(response := await self.scan_wifi_networks()):
            for entry in response.unwrap().entries:
                if entry.ssid == ssid:
                    # Are we already provisioned?
                    if entry.scan_entry_flags & EnumScanEntryFlags.SCAN_FLAG_CONFIGURED:
                        logger.info(f"Connecting to already provisioned network {ssid}...")
                        command = self._gopro.ble_command.request_wifi_connect(ssid=ssid)
                    else:
                        logger.info(f"Provisioning new network {ssid}...")
                        command = self._gopro.ble_command.request_wifi_connect_new(ssid=ssid, password=password)

                    async with GoproObserverDistinctInitial[
                        ResponseConnect | ResponseConnectNew,
                        NotifProvisioningState,
                    ](
                        gopro=self._gopro,
                        update=ProtobufId(FeatureId.NETWORK_MANAGEMENT, ActionId.NOTIF_PROVIS_STATE),
                        register_command=command,
                    ) as observable:
                        if observable.initial_response.result != EnumResultGeneric.RESULT_SUCCESS:
                            return Result.from_failure(GoProError("Failed to start scanning."))

                        try:
                            async with asyncio.timeout(timeout):
                                await observable.observe().first(
                                    lambda s: s.provisioning_state == EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
                                )
                                return Result.from_value(None)
                        except TimeoutError:
                            return Result.from_failure(ResponseTimeout(timeout))
            logger.error(f"Could not find ssid {ssid}")
            return Result.from_failure(RuntimeError(f"Could not find SSID: {ssid}"))
        return Result.from_failure(GoProError("Scanning for SSID's failed"))
