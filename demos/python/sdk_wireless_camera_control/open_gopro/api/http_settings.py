# http_settings.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 20 23:24:52 UTC 2025

"""HTTP Settings"""

########################################################################################################################
#
# Warning!! This file is auto-generated. Do not modify it manually.
#
########################################################################################################################

from open_gopro import models
from open_gopro.api.builders import HttpSetting
from open_gopro.domain.communicator_interface import GoProHttp, HttpMessages
from open_gopro.models.constants import SettingId, settings


class HttpSettings(HttpMessages[HttpSetting]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all HTTP Settings

    Args:
        communicator (GoProHttp): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProHttp):

        self.video_resolution: HttpSetting[settings.VideoResolution] = HttpSetting[settings.VideoResolution](
            communicator, SettingId.VIDEO_RESOLUTION
        )

        """Video Resolution

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-resolution-2)"""

        self.frames_per_second: HttpSetting[settings.FramesPerSecond] = HttpSetting[settings.FramesPerSecond](
            communicator, SettingId.FRAMES_PER_SECOND
        )

        """Frames Per Second

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frames-per-second-3)"""

        self.video_timelapse_rate: HttpSetting[settings.VideoTimelapseRate] = HttpSetting[settings.VideoTimelapseRate](
            communicator, SettingId.VIDEO_TIMELAPSE_RATE
        )

        """Video Timelapse Rate

        How frequently to take a video when performing a Video Timelapse

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-timelapse-rate-5)"""

        self.photo_timelapse_rate: HttpSetting[settings.PhotoTimelapseRate] = HttpSetting[settings.PhotoTimelapseRate](
            communicator, SettingId.PHOTO_TIMELAPSE_RATE
        )

        """Photo Timelapse Rate

        How frequently to take a photo when performing a Photo Timelapse.

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-timelapse-rate-30)"""

        self.nightlapse_rate: HttpSetting[settings.NightlapseRate] = HttpSetting[settings.NightlapseRate](
            communicator, SettingId.NIGHTLAPSE_RATE
        )

        """Nightlapse Rate

        How frequently to take a video or photo when performing a Nightlapse.
		
		This controls the Video or Photo Nightlapse rate if Setting 128 is set to 21 or 26 respectively.

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#nightlapse-rate-32)"""

        self.webcam_digital_lenses: HttpSetting[settings.WebcamDigitalLenses] = HttpSetting[
            settings.WebcamDigitalLenses
        ](communicator, SettingId.WEBCAM_DIGITAL_LENSES)

        """Webcam Digital Lenses

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#webcam-digital-lenses-43)"""

        self.auto_power_down: HttpSetting[settings.AutoPowerDown] = HttpSetting[settings.AutoPowerDown](
            communicator, SettingId.AUTO_POWER_DOWN
        )

        """Auto Power Down

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#auto-power-down-59)"""

        self.gps: HttpSetting[settings.Gps] = HttpSetting[settings.Gps](communicator, SettingId.GPS)

        """GPS

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#gps-83)"""

        self.lcd_brightness: HttpSetting[int] = HttpSetting[int](communicator, SettingId.LCD_BRIGHTNESS)

        """LCD Brightness

        The LCD brightness as a percentage value from 10-100

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lcd-brightness-88)"""

        self.led: HttpSetting[settings.Led] = HttpSetting[settings.Led](communicator, SettingId.LED)

        """LED

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#led-91)"""

        self.video_aspect_ratio: HttpSetting[settings.VideoAspectRatio] = HttpSetting[settings.VideoAspectRatio](
            communicator, SettingId.VIDEO_ASPECT_RATIO
        )

        """Video Aspect Ratio

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-aspect-ratio-108)"""

        self.video_lens: HttpSetting[settings.VideoLens] = HttpSetting[settings.VideoLens](
            communicator, SettingId.VIDEO_LENS
        )

        """Video Lens

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-lens-121)"""

        self.photo_lens: HttpSetting[settings.PhotoLens] = HttpSetting[settings.PhotoLens](
            communicator, SettingId.PHOTO_LENS
        )

        """Photo Lens

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-lens-122)"""

        self.time_lapse_digital_lenses: HttpSetting[settings.TimeLapseDigitalLenses] = HttpSetting[
            settings.TimeLapseDigitalLenses
        ](communicator, SettingId.TIME_LAPSE_DIGITAL_LENSES)

        """Time Lapse Digital Lenses

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#time-lapse-digital-lenses-123)"""

        self.photo_output: HttpSetting[settings.PhotoOutput] = HttpSetting[settings.PhotoOutput](
            communicator, SettingId.PHOTO_OUTPUT
        )

        """Photo Output

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-output-125)"""

        self.media_format: HttpSetting[settings.MediaFormat] = HttpSetting[settings.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT
        )

        """Media Format

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#media-format-128)"""

        self.anti_flicker: HttpSetting[settings.Anti_Flicker] = HttpSetting[settings.Anti_Flicker](
            communicator, SettingId.ANTI_FLICKER
        )

        """Anti-Flicker

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#anti-flicker-134)"""

        self.hypersmooth: HttpSetting[settings.Hypersmooth] = HttpSetting[settings.Hypersmooth](
            communicator, SettingId.HYPERSMOOTH
        )

        """Hypersmooth

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hypersmooth-135)"""

        self.video_horizon_leveling: HttpSetting[settings.VideoHorizonLeveling] = HttpSetting[
            settings.VideoHorizonLeveling
        ](communicator, SettingId.VIDEO_HORIZON_LEVELING)

        """Video Horizon Leveling

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-horizon-leveling-150)"""

        self.photo_horizon_leveling: HttpSetting[settings.PhotoHorizonLeveling] = HttpSetting[
            settings.PhotoHorizonLeveling
        ](communicator, SettingId.PHOTO_HORIZON_LEVELING)

        """Photo Horizon Leveling

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-horizon-leveling-151)"""

        self.video_duration: HttpSetting[settings.VideoDuration] = HttpSetting[settings.VideoDuration](
            communicator, SettingId.VIDEO_DURATION
        )

        """Video Duration

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-duration-156)"""

        self.multi_shot_duration: HttpSetting[settings.MultiShotDuration] = HttpSetting[settings.MultiShotDuration](
            communicator, SettingId.MULTI_SHOT_DURATION
        )

        """Multi Shot Duration

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-duration-157)"""

        self.max_lens: HttpSetting[settings.MaxLens] = HttpSetting[settings.MaxLens](communicator, SettingId.MAX_LENS)

        """Max Lens

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-162)"""

        self.hindsight: HttpSetting[settings.Hindsight] = HttpSetting[settings.Hindsight](
            communicator, SettingId.HINDSIGHT
        )

        """HindSight

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#hindsight-167)"""

        self.scheduled_capture: HttpSetting[models.ScheduledCapture] = HttpSetting[models.ScheduledCapture](
            communicator, SettingId.SCHEDULED_CAPTURE
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

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#scheduled-capture-168)"""

        self.photo_single_interval: HttpSetting[settings.PhotoSingleInterval] = HttpSetting[
            settings.PhotoSingleInterval
        ](communicator, SettingId.PHOTO_SINGLE_INTERVAL)

        """Photo Single Interval

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-single-interval-171)"""

        self.photo_interval_duration: HttpSetting[settings.PhotoIntervalDuration] = HttpSetting[
            settings.PhotoIntervalDuration
        ](communicator, SettingId.PHOTO_INTERVAL_DURATION)

        """Photo Interval Duration

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-interval-duration-172)"""

        self.video_performance_mode: HttpSetting[settings.VideoPerformanceMode] = HttpSetting[
            settings.VideoPerformanceMode
        ](communicator, SettingId.VIDEO_PERFORMANCE_MODE)

        """Video Performance Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-performance-mode-173)"""

        self.control_mode: HttpSetting[settings.ControlMode] = HttpSetting[settings.ControlMode](
            communicator, SettingId.CONTROL_MODE
        )

        """Control Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#control-mode-175)"""

        self.easy_mode_speed: HttpSetting[settings.EasyModeSpeed] = HttpSetting[settings.EasyModeSpeed](
            communicator, SettingId.EASY_MODE_SPEED
        )

        """Easy Mode Speed

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-mode-speed-176)"""

        self.enable_night_photo: HttpSetting[settings.EnableNightPhoto] = HttpSetting[settings.EnableNightPhoto](
            communicator, SettingId.ENABLE_NIGHT_PHOTO
        )

        """Enable Night Photo

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#enable-night-photo-177)"""

        self.wireless_band: HttpSetting[settings.WirelessBand] = HttpSetting[settings.WirelessBand](
            communicator, SettingId.WIRELESS_BAND
        )

        """Wireless Band

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#wireless-band-178)"""

        self.star_trails_length: HttpSetting[settings.StarTrailsLength] = HttpSetting[settings.StarTrailsLength](
            communicator, SettingId.STAR_TRAILS_LENGTH
        )

        """Star Trails Length

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#star-trails-length-179)"""

        self.system_video_mode: HttpSetting[settings.SystemVideoMode] = HttpSetting[settings.SystemVideoMode](
            communicator, SettingId.SYSTEM_VIDEO_MODE
        )

        """System Video Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#system-video-mode-180)"""

        self.video_bit_rate: HttpSetting[settings.VideoBitRate] = HttpSetting[settings.VideoBitRate](
            communicator, SettingId.VIDEO_BIT_RATE
        )

        """Video Bit Rate

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-bit-rate-182)"""

        self.bit_depth: HttpSetting[settings.BitDepth] = HttpSetting[settings.BitDepth](
            communicator, SettingId.BIT_DEPTH
        )

        """Bit Depth

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#bit-depth-183)"""

        self.profiles: HttpSetting[settings.Profiles] = HttpSetting[settings.Profiles](communicator, SettingId.PROFILES)

        """Profiles

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#profiles-184)"""

        self.video_easy_mode: HttpSetting[settings.VideoEasyMode] = HttpSetting[settings.VideoEasyMode](
            communicator, SettingId.VIDEO_EASY_MODE
        )

        """Video Easy Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-easy-mode-186)"""

        self.lapse_mode: HttpSetting[settings.LapseMode] = HttpSetting[settings.LapseMode](
            communicator, SettingId.LAPSE_MODE
        )

        """Lapse Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#lapse-mode-187)"""

        self.max_lens_mod: HttpSetting[settings.MaxLensMod] = HttpSetting[settings.MaxLensMod](
            communicator, SettingId.MAX_LENS_MOD
        )

        """Max Lens Mod

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-189)"""

        self.max_lens_mod_enable: HttpSetting[settings.MaxLensModEnable] = HttpSetting[settings.MaxLensModEnable](
            communicator, SettingId.MAX_LENS_MOD_ENABLE
        )

        """Max Lens Mod Enable

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#max-lens-mod-enable-190)"""

        self.easy_night_photo: HttpSetting[settings.EasyNightPhoto] = HttpSetting[settings.EasyNightPhoto](
            communicator, SettingId.EASY_NIGHT_PHOTO
        )

        """Easy Night Photo

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#easy-night-photo-191)"""

        self.multi_shot_aspect_ratio: HttpSetting[settings.MultiShotAspectRatio] = HttpSetting[
            settings.MultiShotAspectRatio
        ](communicator, SettingId.MULTI_SHOT_ASPECT_RATIO)

        """Multi Shot Aspect Ratio

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-aspect-ratio-192)"""

        self.framing: HttpSetting[settings.Framing] = HttpSetting[settings.Framing](communicator, SettingId.FRAMING)

        """Framing

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#framing-193)"""

        self.camera_volume: HttpSetting[settings.CameraVolume] = HttpSetting[settings.CameraVolume](
            communicator, SettingId.CAMERA_VOLUME
        )

        """Camera Volume

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#camera-volume-216)"""

        self.setup_screen_saver: HttpSetting[settings.SetupScreenSaver] = HttpSetting[settings.SetupScreenSaver](
            communicator, SettingId.SETUP_SCREEN_SAVER
        )

        """Setup Screen Saver

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-screen-saver-219)"""

        self.setup_language: HttpSetting[settings.SetupLanguage] = HttpSetting[settings.SetupLanguage](
            communicator, SettingId.SETUP_LANGUAGE
        )

        """Setup Language

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#setup-language-223)"""

        self.photo_mode: HttpSetting[settings.PhotoMode] = HttpSetting[settings.PhotoMode](
            communicator, SettingId.PHOTO_MODE
        )

        """Photo Mode

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#photo-mode-227)"""

        self.video_framing: HttpSetting[settings.VideoFraming] = HttpSetting[settings.VideoFraming](
            communicator, SettingId.VIDEO_FRAMING
        )

        """Video Framing

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#video-framing-232)"""

        self.multi_shot_framing: HttpSetting[settings.MultiShotFraming] = HttpSetting[settings.MultiShotFraming](
            communicator, SettingId.MULTI_SHOT_FRAMING
        )

        """Multi Shot Framing

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#multi-shot-framing-233)"""

        self.frame_rate: HttpSetting[settings.FrameRate] = HttpSetting[settings.FrameRate](
            communicator, SettingId.FRAME_RATE
        )

        """Frame Rate

        @see [Open GoPro Spec](https://gopro.github.io/OpenGoPro/ble/features/settings.html#frame-rate-234)"""

        super().__init__(communicator)
