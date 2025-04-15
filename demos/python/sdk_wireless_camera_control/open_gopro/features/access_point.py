    @GoProBase._ensure_opened((GoProMessageInterface.BLE,))
    async def connect_to_access_point(self, ssid: str, password: str) -> bool:
        """Connect the camera to a Wifi Access Point

        Args:
            ssid (str): SSID of AP
            password (str): password of AP

        Returns:
            bool: True if AP is currently connected, False otherwise
        """
        scan_result: asyncio.Queue[proto.NotifStartScanning] = asyncio.Queue()
        provisioned_result: asyncio.Queue[proto.NotifProvisioningState] = asyncio.Queue()

        async def wait_for_scan(_: Any, result: proto.NotifStartScanning) -> None:
            await scan_result.put(result)

        async def wait_for_provisioning(_: Any, result: proto.NotifProvisioningState) -> None:
            await provisioned_result.put(result)

        # Wait to receive scanning success
        logger.info("Scanning for Wifi networks")
        self.register_update(wait_for_scan, ActionId.NOTIF_START_SCAN)
        await self.ble_command.scan_wifi_networks()
        if (sresult := await scan_result.get()).scanning_state != proto.EnumScanning.SCANNING_SUCCESS:
            logger.error(f"Scan failed: {str(sresult.scanning_state)}")
            return False
        scan_id = sresult.scan_id
        self.unregister_update(wait_for_scan)

        # Get scan results and see if we need to provision
        for entry in (await self.ble_command.get_ap_entries(scan_id=scan_id)).data.entries:
            if entry.ssid == ssid:
                self.register_update(wait_for_provisioning, ActionId.NOTIF_PROVIS_STATE)
                # Are we already provisioned?
                if entry.scan_entry_flags & proto.EnumScanEntryFlags.SCAN_FLAG_CONFIGURED:
                    logger.info(f"Connecting to already provisioned network {ssid}...")
                    await self.ble_command.request_wifi_connect(ssid=ssid)
                else:
                    logger.info(f"Provisioning new network {ssid}...")
                    await self.ble_command.request_wifi_connect_new(ssid=ssid, password=password)
                if (
                    presult := (await provisioned_result.get())
                ).provisioning_state != proto.EnumProvisioning.PROVISIONING_SUCCESS_NEW_AP:
                    logger.error(f"Provision failed: {str(presult.provisioning_state)}")
                    return False
                self.unregister_update(wait_for_provisioning)
                logger.info(f"Successfully connected to {ssid}")
                return True
        logger.error(f"Could not find ssid {ssid}")
        return False
