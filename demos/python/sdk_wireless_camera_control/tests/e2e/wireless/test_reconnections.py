import pytest

from open_gopro import WirelessGoPro


@pytest.mark.timeout(60)
@pytest.mark.asyncio
async def test_ble_reconnects_5_times_in_one_minute():
    connections = 0

    while True:
        print("======================================================================================================")
        print(f"Iteration #{connections + 1}")
        print("======================================================================================================")
        print("Connecting...")
        async with WirelessGoPro(enable_wifi=False) as gopro:
            print("Getting statuses...")
            assert (await gopro.ble_command.get_camera_statuses()).ok
            print("Disconnecting... ")
            connections += 1
            if connections == 5:
                break

    assert connections == 5


@pytest.mark.timeout(120)
@pytest.mark.asyncio
async def test_ble_reconnects_5_times_in_two_minutes_after_sleeping():
    connections = 0

    while True:
        print("======================================================================================================")
        print(f"Iteration #{connections + 1}")
        print("======================================================================================================")
        print("Connecting...")
        async with WirelessGoPro(enable_wifi=False) as gopro:
            print("Getting statuses...")
            assert (await gopro.ble_command.get_camera_statuses()).ok
            print("Putting the camera to sleep...")
            await gopro.ble_command.sleep()
            print("Disconnecting... ")
            connections += 1
            if connections == 5:
                break

    assert connections == 5
