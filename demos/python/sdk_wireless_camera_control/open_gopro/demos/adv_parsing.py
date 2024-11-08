"""Demo to retrieve and parse bleak-level advertisements"""

import asyncio

from bleak import BleakScanner

from open_gopro.models.ble_advertisement import AdvData, GoProAdvData


async def main() -> None:
    adv_data = AdvData()

    async with BleakScanner(service_uuids=["0000fea6-0000-1000-8000-00805f9b34fb"]) as scanner:
        async for _, data in scanner.advertisement_data():
            adv_data.update(data)
            if adv_data.local_name:  # Once we've received the scan response...
                break

    print(f"GoPro Data: {GoProAdvData.fromAdvData(adv_data)}")


if __name__ == "__main__":
    asyncio.run(main())
