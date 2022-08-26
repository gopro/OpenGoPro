# reconnect_test.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Aug 26 23:10:01 UTC 2022

import asyncio

from tutorial_modules import connect_ble


def dummy_notification_handler(*_) -> None:
    ...


async def main():
    while True:
        client = await connect_ble(dummy_notification_handler)
        await client.disconnect()
        print("============================ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())
