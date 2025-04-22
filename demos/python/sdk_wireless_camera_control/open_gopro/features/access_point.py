"""Access Point (AP) Feature Abstraction."""

import asyncio
import logging

from returns.pipeline import is_successful
from returns.result import Result

from open_gopro import proto
from open_gopro.api.status_flow import StatusFlowSeparateInitial
from open_gopro.constants import ActionId
from open_gopro.exceptions import GoProError, ResponseTimeout
from open_gopro.features.base_feature import BaseFeature

logger = logging.getLogger(__name__)


class AccessPointFeature(BaseFeature):
    """Access Point (AP) feature abstraction"""

    @property
    def is_ready(self) -> bool:  # noqa: D102
        # It's ready upon initialization
        return True

    async def wait_for_ready(self) -> None:  # noqa: D102
        return

    def close(self) -> None:  # noqa: D102
        return

    async def scan_wifi_networks(self) -> Result[proto.ResponseGetApEntries, GoProError]:
        """Instruct the camera to scan for WiFi networks

        Returns:
            Result[proto.ResponseGetApEntries, GoProError]: Discovered AP entries on success or error
        """
        # Wait to receive scanning success
        logger.info("Scanning for Wifi networks")

        async with StatusFlowSeparateInitial[proto.ResponseStartScanning, proto.NotifStartScanning](
            gopro=self._gopro,
            update=ActionId.NOTIF_START_SCAN,
            register_command=self._gopro.ble_command.scan_wifi_networks(),
        ) as flow:
            if flow.initial_response.result != proto.EnumResultGeneric.RESULT_SUCCESS:
                return Result.from_failure(GoProError("Failed to start scanning."))

            async def collect(scan_result: proto.NotifStartScanning) -> bool:
                if scan_result.scanning_state == proto.EnumScanning.SCANNING_SUCCESS:
                    return False
                error_message = f"Scan failed: {str(scan_result.scanning_state)}"
                logger.error(error_message)
                return False

            result = await flow.collect_while(collect)
            entries = await self._gopro.ble_command.get_ap_entries(scan_id=result.scan_id)
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
                    if entry.scan_entry_flags & proto.EnumScanEntryFlags.SCAN_FLAG_CONFIGURED:
                        logger.info(f"Connecting to already provisioned network {ssid}...")
                        command = self._gopro.ble_command.request_wifi_connect(ssid=ssid)
                    else:
                        logger.info(f"Provisioning new network {ssid}...")
                        command = self._gopro.ble_command.request_wifi_connect_new(ssid=ssid, password=password)

                    async with StatusFlowSeparateInitial[
                        proto.ResponseConnect | proto.ResponseConnectNew, proto.NotifProvisioningState
                    ](
                        gopro=self._gopro,
                        update=ActionId.NOTIF_PROVIS_STATE,
                        register_command=command,
                    ) as flow:
                        if flow.initial_response.result != proto.EnumResultGeneric.RESULT_SUCCESS:
                            return Result.from_failure(GoProError("Failed to start scanning."))

                        try:
                            await asyncio.wait_for(
                                flow.first(
                                    lambda s: s.provisioning_state == proto.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
                                ),
                                timeout,
                            )
                            return Result.from_value(None)
                        except TimeoutError:
                            return Result.from_failure(ResponseTimeout(timeout))
            logger.error(f"Could not find ssid {ssid}")
            return Result.from_failure(RuntimeError(f"Could not find SSID: {ssid}"))
        return Result.from_failure(GoProError("Scanning for SSID's failed"))
