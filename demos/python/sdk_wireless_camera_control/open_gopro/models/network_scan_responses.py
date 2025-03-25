# ble_advertisement.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Nov 18 21:03:37 UTC 2024

"""GoPro specific advertisement entities and parsing structures"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from typing import Any

from bleak.backends.scanner import AdvertisementData
from construct import (
    Adapter,
    BitStruct,
    Byte,
    Bytes,
    Flag,
    GreedyString,
    Hex,
    Int16ub,
    Int16ul,
    PaddedString,
    Padding,
    Struct,
    this,
)

from open_gopro.util import deeply_update_dict

logger = logging.getLogger(__name__)


class Hexlify(Adapter):
    """Construct adapter for pretty hex representation"""

    def _decode(self, obj: bytes, context: Any, path: Any) -> str:
        return obj.hex(":")

    def _encode(self, obj: str, context: Any, path: Any) -> list[int]:
        return list(map(int, obj.split(":")))


camera_status_struct = BitStruct(
    "processor_state" / Flag,
    "wifi_ap_state" / Flag,
    "peripheral_pairing_state" / Flag,
    "central_role_enabled" / Flag,
    "is_new_media_available" / Flag,
    "reserved" / Padding(3),
)


camera_capability_struct = BitStruct(
    "cnc" / Flag,
    "ble_metadata" / Flag,
    "wideband_audio" / Flag,
    "concurrent_master_slave" / Flag,
    "onboarding" / Flag,
    "new_media_available" / Flag,
    "reserved" / Padding(10),
)

media_offload_status_struct = BitStruct(
    "available" / Flag,
    "new_media_available" / Flag,
    "battery_ok" / Flag,
    "sd_card_ok" / Flag,
    "busy" / Flag,
    "paused" / Flag,
    "reserved" / Padding(2),
)

manuf_data_struct = Struct(
    "schema_version" / Byte,
    "camera_status" / camera_status_struct,
    "camera_id" / Byte,
    "camera_capabilities" / camera_capability_struct,
    "id_hash" / Bytes(6),
    "media_offload_status" / media_offload_status_struct,
)

adv_data_struct = Struct(
    "flags_length" / Byte,
    "flags" / Hex(Int16ub),
    "uuids_length" / Byte,
    "uuids_type" / Hex(Byte),
    "uuids" / Hex(Int16ul),
    "manuf_length" / Byte,
    "manuf_type" / Hex(Byte),
    "company_id" / Hex(Int16ub),
    "manuf_data" / manuf_data_struct,
)

service_data_struct = Struct(
    "ap_mac_address" / Hexlify(Bytes(4)),
    "serial_number" / GreedyString("utf8"),
)

scan_response_struct = Struct(
    "name_length" / Byte,
    "name_type" / Hex(Byte),
    "name" / PaddedString(this.name_length - 1, "utf8"),
    "service_length" / Byte,
    "service_type" / Hex(Byte),
    "service_uuid" / Hex(Int16ul),
    "service_data" / service_data_struct,
)


@dataclass
class Jsonable:
    """Mixin to use pretty hex presentation for JSON decoding"""

    def __str__(self) -> str:
        def default_decode(obj: Any) -> Any:
            if isinstance(obj, (bytes, bytearray)):
                return obj.hex(":")
            return str(obj)

        return json.dumps(asdict(self), indent=4, default=default_decode)


camera_id_map: dict[int, str] = {
    55: "C344",
    57: "C346",
    58: "C347",
    60: "C349",
    62: "C350",
    64: "C352",
    65: "C353",
}


@dataclass
class GoProAdvData(Jsonable):
    """GoPro-specific advertising data"""

    name: str
    schema_version: int
    processor_state: bool
    wifi_ap_state: bool
    peripheral_pairing_state: bool
    is_new_media_available: bool
    camera_id: int
    supports_cnc: bool
    supports_ble_metadata: bool
    supports_wideband_audio: bool
    supports_concurrent_master_slave: bool
    supports_onboarding: bool
    supports_new_media_available: bool
    id_hash: bytes
    is_media_upload_new_media_available: bool
    is_media_upload_available: bool
    is_media_upload_battery_ok: bool
    is_media_upload_sd_card_ok: bool
    is_media_upload_busy: bool
    is_media_upload_paused: bool
    ap_mac_address: bytes
    partial_serial_number: str

    def __hash__(self) -> int:
        return hash(self.serial_number)

    @property
    def serial_number(self) -> str:
        """Get the serial number as accurately as possible

        Returns:
            str: serial number with X's denoting unknown characters
        """
        try:
            prefix_4 = camera_id_map[self.camera_id]
        except KeyError:
            logger.warning(f"Unknown camera ID {self.camera_id}")
            prefix_4 = "XXXX"
        try:
            middle_6 = self.id_hash.decode("utf-8")
        except UnicodeDecodeError:
            middle_6 = "XXXXXX"
        return f"{prefix_4}{middle_6}{self.partial_serial_number}"

    @classmethod
    def fromAdvData(cls, data: AdvData) -> GoProAdvData:
        """Build GoPro specific advertisement from standard BLE advertisement data

        Args:
            data (AdvData): standard BLE advertisement data

        Returns:
            GoProAdvData: parsed GoPro specific advertising data
        """
        manuf_data = manuf_data_struct.parse(list(data.manufacturer_data.values())[0])
        service_data = service_data_struct.parse(list(data.service_data.values())[0])
        return GoProAdvData(
            # Name from scan response data
            name=data.local_name,
            # Schema version from advertising data manufacturer data
            schema_version=manuf_data.schema_version,
            # Camera status from advertising data manufacturer data
            processor_state=manuf_data.camera_status.processor_state,
            wifi_ap_state=manuf_data.camera_status.wifi_ap_state,
            peripheral_pairing_state=manuf_data.camera_status.peripheral_pairing_state,
            is_new_media_available=manuf_data.camera_status.is_new_media_available,
            # Camera ID from advertising data manufacturer data
            camera_id=int(manuf_data.camera_id),
            # Camera capabilities from advertising data manufacturer data
            supports_ble_metadata=manuf_data.camera_capabilities.ble_metadata,
            supports_cnc=manuf_data.camera_capabilities.cnc,
            supports_onboarding=manuf_data.camera_capabilities.onboarding,
            supports_wideband_audio=manuf_data.camera_capabilities.wideband_audio,
            supports_concurrent_master_slave=manuf_data.camera_capabilities.concurrent_master_slave,
            supports_new_media_available=manuf_data.camera_capabilities.new_media_available,
            # ID Hash from advertising data manufacturer's data
            id_hash=manuf_data.id_hash,
            # Media offload status status from advertising data manufacturer's data
            is_media_upload_new_media_available=manuf_data.media_offload_status.new_media_available,
            is_media_upload_available=manuf_data.media_offload_status.available,
            is_media_upload_battery_ok=manuf_data.media_offload_status.battery_ok,
            is_media_upload_sd_card_ok=manuf_data.media_offload_status.sd_card_ok,
            is_media_upload_busy=manuf_data.media_offload_status.busy,
            is_media_upload_paused=manuf_data.media_offload_status.paused,
            # Mac address from scan response data service data
            ap_mac_address=service_data.ap_mac_address,
            # Partial serial number from scan response data service data
            partial_serial_number=service_data.serial_number,
        )


@dataclass
class AdvData(Jsonable):
    """Standard BLE advertising data

    Only contains fields that are currently used by GoPro
    """

    serial_number: str = ""
    local_name: str = ""
    manufacturer_data: dict[str, Any] = field(default_factory=dict)
    service_uuids: list[str] = field(default_factory=list)
    service_data: dict = field(default_factory=dict)

    def update(self, data: AdvertisementData) -> None:
        """Update with a (potentially incomplete) advertisement

        Args:
            data (AdvertisementData): advertisement to use for updating
        """
        self_dict = asdict(self)
        for k, v in data._asdict().items():
            if not v:
                continue
            if isinstance(v, dict):
                setattr(self, k, deeply_update_dict(self_dict[k], v))
            elif isinstance(v, list):
                setattr(self, k, [*self_dict[k], v])
            else:
                setattr(self, k, v)


@dataclass
class DnsScanResponse:
    """mDNS scan data"""

    service: str
    ip_addr: str
    name: str
