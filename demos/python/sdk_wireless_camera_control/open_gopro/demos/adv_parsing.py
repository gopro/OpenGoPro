from __future__ import annotations
import asyncio
import json
from typing import Any
from dataclasses import dataclass, field, asdict

from construct import Int16ub
from bleak import BleakScanner
from bleak.backends.scanner import AdvertisementData

from construct import (
    GreedyString,
    Struct,
    Byte,
    Int16ub,
    Bytes,
    BitStruct,
    Flag,
    Padding,
    Enum,
    this,
    Hex,
    Int16ul,
    Adapter,
)


class Hexlify(Adapter):
    def _decode(self, obj: bytes, context, path):
        return obj.hex(":")

    def _encode(self, obj: str, context, path):
        return list(map(int, obj.split(":")))


example_adv_data = bytes(
    [
        0x02,
        0x01,
        0x02,
        0x03,
        0x02,
        0xA6,
        0xFE,
        0x0F,
        0xFF,
        0xF2,
        0x02,
        0x02,
        0x01,
        0x38,
        0x33,
        0x00,
        0xB3,
        0xFE,
        0x2A,
        0x79,
        0xDC,
        0xEB,
        0x0F,
    ]
)

camera_status_struct = BitStruct(
    "processor_state" / Flag,
    "wifi_ap_state" / Flag,
    "peripheral_pairing_state" / Flag,
    "central_role_enabled" / Flag,
    "is_new_media_available" / Flag,
    "reserved" / Padding(3),
)

camera_id_struct = Enum(
    Byte,
    Hero11Black=56,
    Fraction=66,
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
    "camera_id" / camera_id_struct,
    "camera_capabilities" / camera_capability_struct,
    "id_hash" / Hexlify(Bytes(6)),
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

example_scan_response_data = bytes(
    [
        0x0B,
        0x09,
        0x47,
        0x6F,
        0x50,
        0x72,
        0x6F,
        0x20,
        0x31,
        0x30,
        0x35,
        0x38,
        0x0B,
        0x16,
        0xA6,
        0xFE,
        0xF7,
        0xA9,
        0x76,
        0x88,
        0x31,
        0x30,
        0x35,
        0x38,
    ]
)

service_data_struct = Struct(
    "ap_mac_address" / Hexlify(Bytes(4)),
    "serial_number" / GreedyString("utf8"),
)

scan_response_struct = Struct(
    "name_length" / Byte,
    "name_type" / Hex(Byte),
    "name" / Bytes(this.name_length - 1),
    "service_length" / Byte,
    "service_type" / Hex(Byte),
    "service_uuid" / Hex(Int16ul),
    "service_data" / service_data_struct,
)


@dataclass
class Jsonable:
    def __str__(self) -> str:
        def default_decode(obj: Any) -> Any:
            if isinstance(obj, (bytes, bytearray)):
                return obj.hex(":")
            return str(obj)

        return json.dumps(asdict(self), indent=4, default=default_decode)


@dataclass
class GoProAdvData(Jsonable):
    name: str
    schema_version: int
    processor_state: bool
    wifi_ap_state: bool
    peripheral_pairing_state: bool
    is_new_media_available: bool
    camera_id: str
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
    partial_serial_number: bytes

    @classmethod
    def fromAdvData(cls, data: AdvData) -> GoProAdvData:
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
            camera_id=manuf_data.camera_id,
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
    local_name: str = ""
    manufacturer_data: dict[str, Any] = field(default_factory=dict)
    service_uuids: list[str] = field(default_factory=list)
    service_data: dict = field(default_factory=dict)

    @staticmethod
    def deeply_update_dict(d: dict, u: dict) -> dict:
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = AdvData.deeply_update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def update(self, data: AdvertisementData) -> None:
        self_dict = asdict(self)
        for k, v in data._asdict().items():
            if not v:
                continue
            if isinstance(v, dict):
                self.__setattr__(k, self.deeply_update_dict(self_dict[k], v))
            elif isinstance(v, list):
                self.__setattr__(k, [*self_dict[k], v])
            else:
                self.__setattr__(k, v)


async def main():
    # print(adv_data_struct.parse(example_adv_data))
    # print(scan_response_struct.parse(example_scan_response_data))

    adv_data = AdvData()

    async with BleakScanner(service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"]) as scanner:
        async for _, data in scanner.advertisement_data():
            adv_data.update(data)
            if adv_data.local_name:  # Once we've received the scan response...
                break

    print(f"GoPro Data: {GoProAdvData.fromAdvData(adv_data)}")


if __name__ == "__main__":
    asyncio.run(main())
