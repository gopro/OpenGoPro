import pytest
import pytest_asyncio

from open_gopro import WirelessGoPro, proto
from open_gopro.models.constants import settings


@pytest_asyncio.fixture(loop_scope="function")
async def wireless_gopro_ble():
    async with WirelessGoPro(interfaces={WirelessGoPro.Interface.BLE}) as gopro:
        assert (await gopro.ble_setting.control_mode.set(settings.ControlMode.PRO)).ok
        yield gopro


@pytest.mark.timeout(60)
@pytest.mark.asyncio
async def test_ble_settings_value_observable_change_resolution(wireless_gopro_ble: WirelessGoPro):
    async with (await wireless_gopro_ble.ble_setting.video_resolution.get_value_observable()).unwrap() as observable:
        assert (
            await wireless_gopro_ble.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_VIDEO)
        ).ok

        # We should always have an initial response
        assert observable.initial_response is not None
        assert observable.initial_response == await observable.single()  # First value is the initial response

        if observable.initial_response == settings.VideoResolution.NUM_1080:
            # Set to 4k
            assert (await wireless_gopro_ble.ble_setting.video_resolution.set(settings.VideoResolution.NUM_4K)).ok
            assert await observable.single() == settings.VideoResolution.NUM_4K
        else:
            # Set to 1080
            assert (await wireless_gopro_ble.ble_setting.video_resolution.set(settings.VideoResolution.NUM_1080)).ok
            assert await observable.single() == settings.VideoResolution.NUM_1080
