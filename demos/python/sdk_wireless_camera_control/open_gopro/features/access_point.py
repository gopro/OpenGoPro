import asyncio
import logging
from typing import Any

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success
from setuptools import Command

from open_gopro.api.api import WirelessApi
from open_gopro.api.status_flow import StatusFlow, StatusFlowSeparateInitial
from open_gopro.constants import ActionId
from open_gopro.exceptions import GoProError, ResponseTimeout
from open_gopro.features.base_feature import BaseFeature
from open_gopro.flow import Flow, FlowManager
from open_gopro.gopro_base import GoProBase
from open_gopro.proto import (
    EnumProvisioning,
    EnumScanEntryFlags,
    EnumScanning,
    NotifProvisioningState,
    NotifStartScanning,
)
from open_gopro.proto.network_management_pb2 import (
    ResponseConnect,
    ResponseConnectNew,
    ResponseGetApEntries,
    ResponseStartScanning,
)
from open_gopro.proto.response_generic_pb2 import EnumResultGeneric

logger = logging.getLogger(__name__)


class AccessPointFeature(BaseFeature):
    @property
    def is_ready(self) -> bool:
        # It's ready upon initialization
        return True

    async def wait_for_ready(self) -> None:
        return

    async def scan_wifi_networks(self) -> Result[ResponseGetApEntries, GoProError]:
        # Wait to receive scanning success
        logger.info("Scanning for Wifi networks")

        async with StatusFlowSeparateInitial[ResponseStartScanning, NotifStartScanning](
            gopro=self._gopro,
            update=ActionId.NOTIF_START_SCAN,
            register_command=self._gopro.ble_command.scan_wifi_networks(),
        ) as flow:
            if flow.initial_response.result != EnumResultGeneric.RESULT_SUCCESS:
                return Result.from_failure(GoProError("Failed to start scanning."))

            async def collect(scan_result: NotifStartScanning) -> bool:
                if scan_result.scanning_state == EnumScanning.SCANNING_SUCCESS:
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

        Returns:
            bool: True if AP is currently connected, False otherwise
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

                    async with StatusFlowSeparateInitial[ResponseConnect | ResponseConnectNew, NotifProvisioningState](
                        gopro=self._gopro,
                        update=ActionId.NOTIF_PROVIS_STATE,
                        register_command=command,
                    ) as flow:
                        if flow.initial_response.result != EnumResultGeneric.RESULT_SUCCESS:
                            return Result.from_failure(GoProError("Failed to start scanning."))

                        try:
                            await asyncio.wait_for(
                                flow.first(
                                    lambda s: s.provisioning_state == EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP
                                ),
                                timeout,
                            )
                            return Result.from_value(None)
                        except TimeoutError as e:
                            return Result.from_failure(ResponseTimeout(timeout))
            logger.error(f"Could not find ssid {ssid}")
            return Result.from_failure(RuntimeError(f"Could not find SSID: {ssid}"))
        else:
            return Result.from_failure(GoProError(f"Scanning for SSID's failed"))

    def close(self) -> None: ...
