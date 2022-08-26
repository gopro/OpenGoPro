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
