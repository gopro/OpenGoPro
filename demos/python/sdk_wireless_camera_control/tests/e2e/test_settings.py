# test_settings.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

from datetime import timedelta

import pytest

from open_gopro import WirelessGoPro
from open_gopro.models import general, proto
from open_gopro.models.constants import settings
from open_gopro.util import get_current_dst_aware_time


@pytest.mark.timeout(60)
async def test_ble_settings_value_observable_change_resolution(wireless_gopro_ble: WirelessGoPro):
    async with (await wireless_gopro_ble.ble_setting.video_resolution.get_value_observable()).unwrap() as observable:
        assert (
            await wireless_gopro_ble.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_VIDEO)
        ).ok

        # We should always have an initial response
        assert observable.initial_response is not None
        observer = observable.observe()
        assert observable.initial_response == await anext(observer)  # First value is the initial response

        if observable.initial_response == settings.VideoResolution.NUM_1080:
            # Set to 4k
            assert (await wireless_gopro_ble.ble_setting.video_resolution.set(settings.VideoResolution.NUM_4K)).ok
            assert await anext(observer) == settings.VideoResolution.NUM_4K
        else:
            # Set to 1080
            assert (await wireless_gopro_ble.ble_setting.video_resolution.set(settings.VideoResolution.NUM_1080)).ok
            assert await anext(observer) == settings.VideoResolution.NUM_1080


@pytest.mark.timeout(180)
async def test_scheduled_capture(wireless_gopro_ble: WirelessGoPro):
    await wireless_gopro_ble.ble_setting.control_mode.set(settings.ControlMode.PRO)

    print("Entering Video Mode")
    assert (
        await wireless_gopro_ble.ble_command.load_preset_group(group=proto.EnumPresetGroup.PRESET_GROUP_ID_VIDEO)
    ).ok

    now, tz_offset, is_dst = get_current_dst_aware_time()
    print(f"Setting the camera's datetime to {now}")
    assert (
        await wireless_gopro_ble.ble_command.set_date_time_tz_dst(date_time=now, tz_offset=tz_offset, is_dst=is_dst)
    ).ok

    print("Getting the current scheduled capture value, just for demonstration.")
    current_scheduled_capture = await wireless_gopro_ble.ble_setting.scheduled_capture.get_value()
    assert current_scheduled_capture.ok
    print(f"Current scheduled capture is: {current_scheduled_capture.data}")

    # Set the video duration
    print("Setting the video encoding duration to 15 seconds.")
    assert (await wireless_gopro_ble.ble_setting.video_duration.set(settings.VideoDuration.NUM_15_SECONDS)).ok

    # Configure scheduled capture for one minute in the future
    capture_time = now + timedelta(minutes=1)
    print(f"Scheduling a scheduled capture at {capture_time}")
    assert (
        await wireless_gopro_ble.ble_setting.scheduled_capture.set(
            general.ScheduledCapture.from_datetime(
                dt=capture_time,
                is_enabled=True,
            )
        )
    ).ok

    print("Scheduled capture is configured successfully")

    print("Waiting for encoding to start...")
    # Wait to receive encoding status
    async with (await wireless_gopro_ble.ble_status.encoding.get_value_observable()).unwrap() as observable:
        await observable.observe().first(lambda status: status == True)

    print("Schedule capture has occurred")
