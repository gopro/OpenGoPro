import pytest

from open_gopro import WirelessGoPro


@pytest.mark.timeout(180)
async def test_can_set_camera_name(wireless_gopro: WirelessGoPro):
    old_name = (await wireless_gopro.http_command.get_camera_name()).data
    new_name = "Test Camera"

    if old_name == new_name:
        new_name += " newer"

    # Set via HTTP to new name and verify
    assert (await wireless_gopro.http_command.set_camera_name(name=new_name)).ok
    current_name = (await wireless_gopro.http_command.get_camera_name()).data
    assert current_name == new_name

    # Now set back to old name via BLE and verify (via HTTP)
    assert (await wireless_gopro.ble_command.set_camera_name(name=old_name)).ok
    current_name = (await wireless_gopro.http_command.get_camera_name()).data
    assert current_name == old_name
