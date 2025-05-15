# ble_settings.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 20 23:24:52 UTC 2025

"""BLE Settings"""

########################################################################################################################
#
# Warning!! This file is auto-generated. Do not modify it manually.
#
########################################################################################################################

from open_gopro import models, parsers
from open_gopro.api.builders import BleSettingFacade as BleSetting
from open_gopro.domain.communicator_interface import BleMessages, GoProBle
from open_gopro.models.constants import SettingId, settings


class BleSettings(BleMessages[BleSetting.BleSettingMessageBase]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all BLE Settings.

    To be used by a GoProBle delegate to build setting messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProBle):

        self.video_resolution: BleSetting[settings.VideoResolution] = BleSetting[settings.VideoResolution](
            communicator, SettingId.VIDEO_RESOLUTION, settings.VideoResolution
        )

        """Video Resolution

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)"""

        self.frames_per_second: BleSetting[settings.FramesPerSecond] = BleSetting[settings.FramesPerSecond](
            communicator, SettingId.FRAMES_PER_SECOND, settings.FramesPerSecond
        )

        """Frames Per Second

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)"""

        self.video_timelapse_rate: BleSetting[settings.VideoTimelapseRate] = BleSetting[settings.VideoTimelapseRate](
            communicator, SettingId.VIDEO_TIMELAPSE_RATE, settings.VideoTimelapseRate
        )

        """Video Timelapse Rate

        How frequently to take a video when performing a Video Timelapse

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5)"""

        self.photo_timelapse_rate: BleSetting[settings.PhotoTimelapseRate] = BleSetting[settings.PhotoTimelapseRate](
            communicator, SettingId.PHOTO_TIMELAPSE_RATE, settings.PhotoTimelapseRate
        )

        """Photo Timelapse Rate

        How frequently to take a photo when performing a Photo Timelapse.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30)"""

        self.nightlapse_rate: BleSetting[settings.NightlapseRate] = BleSetting[settings.NightlapseRate](
            communicator, SettingId.NIGHTLAPSE_RATE, settings.NightlapseRate
        )

        """Nightlapse Rate

        How frequently to take a video or photo when performing a Nightlapse.
		
		This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32)"""

        self.webcam_digital_lenses: BleSetting[settings.WebcamDigitalLenses] = BleSetting[settings.WebcamDigitalLenses](
            communicator, SettingId.WEBCAM_DIGITAL_LENSES, settings.WebcamDigitalLenses
        )

        """Webcam Digital Lenses

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43)"""

        self.auto_power_down: BleSetting[settings.AutoPowerDown] = BleSetting[settings.AutoPowerDown](
            communicator, SettingId.AUTO_POWER_DOWN, settings.AutoPowerDown
        )

        """Auto Power Down

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59)"""

        self.gps: BleSetting[settings.Gps] = BleSetting[settings.Gps](communicator, SettingId.GPS, settings.Gps)

        """GPS

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83)"""

        self.lcd_brightness: BleSetting[int] = BleSetting[int](
            communicator, SettingId.LCD_BRIGHTNESS, parsers.IntByteParserBuilder(1)
        )

        """LCD Brightness

        The LCD brightness as a percentage value from 10-100

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lcd-brightness-88)"""

        self.led: BleSetting[settings.Led] = BleSetting[settings.Led](communicator, SettingId.LED, settings.Led)

        """LED

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#led-91)"""

        self.video_aspect_ratio: BleSetting[settings.VideoAspectRatio] = BleSetting[settings.VideoAspectRatio](
            communicator, SettingId.VIDEO_ASPECT_RATIO, settings.VideoAspectRatio
        )

        """Video Aspect Ratio

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108)"""

        self.video_lens: BleSetting[settings.VideoLens] = BleSetting[settings.VideoLens](
            communicator, SettingId.VIDEO_LENS, settings.VideoLens
        )

        """Video Lens

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121)"""

        self.photo_lens: BleSetting[settings.PhotoLens] = BleSetting[settings.PhotoLens](
            communicator, SettingId.PHOTO_LENS, settings.PhotoLens
        )

        """Photo Lens

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122)"""

        self.time_lapse_digital_lenses: BleSetting[settings.TimeLapseDigitalLenses] = BleSetting[
            settings.TimeLapseDigitalLenses
        ](communicator, SettingId.TIME_LAPSE_DIGITAL_LENSES, settings.TimeLapseDigitalLenses)

        """Time Lapse Digital Lenses

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123)"""

        self.photo_output: BleSetting[settings.PhotoOutput] = BleSetting[settings.PhotoOutput](
            communicator, SettingId.PHOTO_OUTPUT, settings.PhotoOutput
        )

        """Photo Output

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125)"""

        self.media_format: BleSetting[settings.MediaFormat] = BleSetting[settings.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT, settings.MediaFormat
        )

        """Media Format

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128)"""

        self.anti_flicker: BleSetting[settings.Anti_Flicker] = BleSetting[settings.Anti_Flicker](
            communicator, SettingId.ANTI_FLICKER, settings.Anti_Flicker
        )

        """Anti-Flicker

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134)"""

        self.hypersmooth: BleSetting[settings.Hypersmooth] = BleSetting[settings.Hypersmooth](
            communicator, SettingId.HYPERSMOOTH, settings.Hypersmooth
        )

        """Hypersmooth

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135)"""

        self.video_horizon_leveling: BleSetting[settings.VideoHorizonLeveling] = BleSetting[
            settings.VideoHorizonLeveling
        ](communicator, SettingId.VIDEO_HORIZON_LEVELING, settings.VideoHorizonLeveling)

        """Video Horizon Leveling

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150)"""

        self.photo_horizon_leveling: BleSetting[settings.PhotoHorizonLeveling] = BleSetting[
            settings.PhotoHorizonLeveling
        ](communicator, SettingId.PHOTO_HORIZON_LEVELING, settings.PhotoHorizonLeveling)

        """Photo Horizon Leveling

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151)"""

        self.video_duration: BleSetting[settings.VideoDuration] = BleSetting[settings.VideoDuration](
            communicator, SettingId.VIDEO_DURATION, settings.VideoDuration
        )

        """Video Duration

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-duration-156)"""

        self.multi_shot_duration: BleSetting[settings.MultiShotDuration] = BleSetting[settings.MultiShotDuration](
            communicator, SettingId.MULTI_SHOT_DURATION, settings.MultiShotDuration
        )

        """Multi Shot Duration

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-duration-157)"""

        self.max_lens: BleSetting[settings.MaxLens] = BleSetting[settings.MaxLens](
            communicator, SettingId.MAX_LENS, settings.MaxLens
        )

        """Max Lens

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162)"""

        self.hindsight: BleSetting[settings.Hindsight] = BleSetting[settings.Hindsight](
            communicator, SettingId.HINDSIGHT, settings.Hindsight
        )

        """HindSight

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167)"""

        self.scheduled_capture: BleSetting[models.ScheduledCapture] = BleSetting[models.ScheduledCapture](
            communicator, SettingId.SCHEDULED_CAPTURE, parsers.ScheduledCaptureParser
        )

        """Scheduled Capture

        Configure or disable the scheduled capture functionality to start encoding at a future time.
		
		This is a bit-masked value with the following bitwise definitions,
		numbered from least significant bit, with the example showing parsed fields from a sample of `0x00000c8b`.
		
		| Bit(s) | Definition                    | Example |
		| ------ | ----------------------------- | ------- |
		| 0      | Is Scheduled Capture Enabled? | 1       |
		| 1      | Is 24 hour format?            | 1       |
		| 2-8    | Minute                        | 34      |
		| 9-13   | Hour                          | 12      |
		| 14-63  | Reserved                      | 0       |
		
		Note that when the scheduled capture time occurs, encoding will be started and continue indefinitely.  One
		of the duration settings (156, 157, 172) can be used to set the encoding duration depending on the camera mode.

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#scheduled-capture-168)"""

        self.photo_single_interval: BleSetting[settings.PhotoSingleInterval] = BleSetting[settings.PhotoSingleInterval](
            communicator, SettingId.PHOTO_SINGLE_INTERVAL, settings.PhotoSingleInterval
        )

        """Photo Single Interval

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171)"""

        self.photo_interval_duration: BleSetting[settings.PhotoIntervalDuration] = BleSetting[
            settings.PhotoIntervalDuration
        ](communicator, SettingId.PHOTO_INTERVAL_DURATION, settings.PhotoIntervalDuration)

        """Photo Interval Duration

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172)"""

        self.video_performance_mode: BleSetting[settings.VideoPerformanceMode] = BleSetting[
            settings.VideoPerformanceMode
        ](communicator, SettingId.VIDEO_PERFORMANCE_MODE, settings.VideoPerformanceMode)

        """Video Performance Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173)"""

        self.control_mode: BleSetting[settings.ControlMode] = BleSetting[settings.ControlMode](
            communicator, SettingId.CONTROL_MODE, settings.ControlMode
        )

        """Control Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#control-mode-175)"""

        self.easy_mode_speed: BleSetting[settings.EasyModeSpeed] = BleSetting[settings.EasyModeSpeed](
            communicator, SettingId.EASY_MODE_SPEED, settings.EasyModeSpeed
        )

        """Easy Mode Speed

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176)"""

        self.enable_night_photo: BleSetting[settings.EnableNightPhoto] = BleSetting[settings.EnableNightPhoto](
            communicator, SettingId.ENABLE_NIGHT_PHOTO, settings.EnableNightPhoto
        )

        """Enable Night Photo

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177)"""

        self.wireless_band: BleSetting[settings.WirelessBand] = BleSetting[settings.WirelessBand](
            communicator, SettingId.WIRELESS_BAND, settings.WirelessBand
        )

        """Wireless Band

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178)"""

        self.star_trails_length: BleSetting[settings.StarTrailsLength] = BleSetting[settings.StarTrailsLength](
            communicator, SettingId.STAR_TRAILS_LENGTH, settings.StarTrailsLength
        )

        """Star Trails Length

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179)"""

        self.system_video_mode: BleSetting[settings.SystemVideoMode] = BleSetting[settings.SystemVideoMode](
            communicator, SettingId.SYSTEM_VIDEO_MODE, settings.SystemVideoMode
        )

        """System Video Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180)"""

        self.video_bit_rate: BleSetting[settings.VideoBitRate] = BleSetting[settings.VideoBitRate](
            communicator, SettingId.VIDEO_BIT_RATE, settings.VideoBitRate
        )

        """Video Bit Rate

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182)"""

        self.bit_depth: BleSetting[settings.BitDepth] = BleSetting[settings.BitDepth](
            communicator, SettingId.BIT_DEPTH, settings.BitDepth
        )

        """Bit Depth

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183)"""

        self.profiles: BleSetting[settings.Profiles] = BleSetting[settings.Profiles](
            communicator, SettingId.PROFILES, settings.Profiles
        )

        """Profiles

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184)"""

        self.video_easy_mode: BleSetting[settings.VideoEasyMode] = BleSetting[settings.VideoEasyMode](
            communicator, SettingId.VIDEO_EASY_MODE, settings.VideoEasyMode
        )

        """Video Easy Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186)"""

        self.lapse_mode: BleSetting[settings.LapseMode] = BleSetting[settings.LapseMode](
            communicator, SettingId.LAPSE_MODE, settings.LapseMode
        )

        """Lapse Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187)"""

        self.max_lens_mod: BleSetting[settings.MaxLensMod] = BleSetting[settings.MaxLensMod](
            communicator, SettingId.MAX_LENS_MOD, settings.MaxLensMod
        )

        """Max Lens Mod

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189)"""

        self.max_lens_mod_enable: BleSetting[settings.MaxLensModEnable] = BleSetting[settings.MaxLensModEnable](
            communicator, SettingId.MAX_LENS_MOD_ENABLE, settings.MaxLensModEnable
        )

        """Max Lens Mod Enable

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190)"""

        self.easy_night_photo: BleSetting[settings.EasyNightPhoto] = BleSetting[settings.EasyNightPhoto](
            communicator, SettingId.EASY_NIGHT_PHOTO, settings.EasyNightPhoto
        )

        """Easy Night Photo

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191)"""

        self.multi_shot_aspect_ratio: BleSetting[settings.MultiShotAspectRatio] = BleSetting[
            settings.MultiShotAspectRatio
        ](communicator, SettingId.MULTI_SHOT_ASPECT_RATIO, settings.MultiShotAspectRatio)

        """Multi Shot Aspect Ratio

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192)"""

        self.framing: BleSetting[settings.Framing] = BleSetting[settings.Framing](
            communicator, SettingId.FRAMING, settings.Framing
        )

        """Framing

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193)"""

        self.camera_volume: BleSetting[settings.CameraVolume] = BleSetting[settings.CameraVolume](
            communicator, SettingId.CAMERA_VOLUME, settings.CameraVolume
        )

        """Camera Volume

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-volume-216)"""

        self.setup_screen_saver: BleSetting[settings.SetupScreenSaver] = BleSetting[settings.SetupScreenSaver](
            communicator, SettingId.SETUP_SCREEN_SAVER, settings.SetupScreenSaver
        )

        """Setup Screen Saver

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219)"""

        self.setup_language: BleSetting[settings.SetupLanguage] = BleSetting[settings.SetupLanguage](
            communicator, SettingId.SETUP_LANGUAGE, settings.SetupLanguage
        )

        """Setup Language

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223)"""

        self.photo_mode: BleSetting[settings.PhotoMode] = BleSetting[settings.PhotoMode](
            communicator, SettingId.PHOTO_MODE, settings.PhotoMode
        )

        """Photo Mode

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227)"""

        self.video_framing: BleSetting[settings.VideoFraming] = BleSetting[settings.VideoFraming](
            communicator, SettingId.VIDEO_FRAMING, settings.VideoFraming
        )

        """Video Framing

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232)"""

        self.multi_shot_framing: BleSetting[settings.MultiShotFraming] = BleSetting[settings.MultiShotFraming](
            communicator, SettingId.MULTI_SHOT_FRAMING, settings.MultiShotFraming
        )

        """Multi Shot Framing

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233)"""

        self.frame_rate: BleSetting[settings.FrameRate] = BleSetting[settings.FrameRate](
            communicator, SettingId.FRAME_RATE, settings.FrameRate
        )

        """Frame Rate

        See [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234)"""

        super().__init__(communicator)
