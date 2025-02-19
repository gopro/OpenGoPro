"""BLE Settings"""

from construct import Int8ub

from open_gopro.api.builders import BleSettingFacade as BleSetting
from open_gopro.communicator_interface import BleMessages, GoProBle
from open_gopro.constants import SettingId

from . import params as Params


class BleSettings(BleMessages[BleSetting.BleSettingMessageBase]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all BLE Settings.

    To be used by a GoProBle delegate to build setting messages.

    Args:
        communicator (GoProBle): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProBle):
        self.resolution: BleSetting[Params.Resolution] = BleSetting[Params.Resolution](
            communicator, SettingId.RESOLUTION, Params.Resolution
        )
        """Resolution."""

        self.fps: BleSetting[Params.FPS] = BleSetting[Params.FPS](communicator, SettingId.FPS, Params.FPS)
        """Frames per second."""

        self.auto_off: BleSetting[Params.AutoOff] = BleSetting[Params.AutoOff](
            communicator, SettingId.AUTO_OFF, Params.AutoOff
        )
        """Set the auto off time."""

        self.video_field_of_view: BleSetting[Params.VideoFOV] = BleSetting[Params.VideoFOV](
            communicator, SettingId.VIDEO_FOV, Params.VideoFOV
        )
        """Video FOV."""

        self.photo_field_of_view: BleSetting[Params.PhotoFOV] = BleSetting[Params.PhotoFOV](
            communicator, SettingId.PHOTO_FOV, Params.PhotoFOV
        )
        """Photo FOV."""

        self.multi_shot_field_of_view: BleSetting[Params.MultishotFOV] = BleSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV, Params.MultishotFOV
        )
        """Multi-shot FOV."""

        self.led: BleSetting[Params.LED] = BleSetting[Params.LED](communicator, SettingId.LED, Params.LED)
        """Set the LED options (or also send the BLE keep alive signal)."""

        self.max_lens_mode: BleSetting[Params.MaxLensMode] = BleSetting[Params.MaxLensMode](
            communicator, SettingId.MAX_LENS_MOD, Params.MaxLensMode
        )
        """Enable / disable max lens mod."""

        self.hypersmooth: BleSetting[Params.HypersmoothMode] = BleSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH, Params.HypersmoothMode
        )
        """Set / disable hypersmooth."""

        self.video_performance_mode: BleSetting[Params.PerformanceMode] = BleSetting[Params.PerformanceMode](
            communicator,
            SettingId.VIDEO_PERFORMANCE_MODE,
            Params.PerformanceMode,
        )
        """Video Performance Mode."""

        self.media_format: BleSetting[Params.MediaFormat] = BleSetting[Params.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT, Params.MediaFormat
        )
        """Set the media format."""

        self.anti_flicker: BleSetting[Params.AntiFlicker] = BleSetting[Params.AntiFlicker](
            communicator,
            SettingId.ANTI_FLICKER,
            Params.AntiFlicker,
        )
        """Anti Flicker frequency."""

        self.camera_ux_mode: BleSetting[Params.CameraUxMode] = BleSetting[Params.CameraUxMode](
            communicator,
            SettingId.CAMERA_UX_MODE,
            Params.CameraUxMode,
        )
        """Camera controls configuration."""

        self.video_easy_mode: BleSetting[int] = BleSetting[int](
            communicator,
            SettingId.VIDEO_EASY_MODE,
            Int8ub,
        )
        """Video easy mode speed. It is not feasible to maintain this setting without code generation so just read as int."""

        self.photo_easy_mode: BleSetting[Params.PhotoEasyMode] = BleSetting[Params.PhotoEasyMode](
            communicator,
            SettingId.PHOTO_EASY_MODE,
            Params.PhotoEasyMode,
        )
        """Night Photo easy mode."""

        self.wifi_band: BleSetting[Params.WifiBand] = BleSetting[Params.WifiBand](
            communicator,
            SettingId.WIFI_BAND,
            Params.WifiBand,
        )
        """Current WiFi band being used."""

        self.star_trail_length: BleSetting[Params.StarTrailLength] = BleSetting[Params.StarTrailLength](
            communicator,
            SettingId.STAR_TRAIL_LENGTH,
            Params.StarTrailLength,
        )
        """Multi shot star trail length."""

        self.system_video_mode: BleSetting[Params.SystemVideoMode] = BleSetting[Params.SystemVideoMode](
            communicator,
            SettingId.SYSTEM_VIDEO_MODE,
            Params.SystemVideoMode,
        )
        """System video mode."""

        self.video_horizon_leveling: BleSetting[Params.HorizonLeveling] = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.VIDEO_HORIZON_LEVELING,
            Params.HorizonLeveling,
        )
        """Lock / unlock horizon leveling for video."""

        self.photo_horizon_leveling: BleSetting[Params.HorizonLeveling] = BleSetting[Params.HorizonLeveling](
            communicator,
            SettingId.PHOTO_HORIZON_LEVELING,
            Params.HorizonLeveling,
        )
        """Lock / unlock horizon leveling for photo."""

        self.bit_rate: BleSetting[Params.BitRate] = BleSetting[Params.BitRate](
            communicator,
            SettingId.BIT_RATE,
            Params.BitRate,
        )
        """System Video Bit Rate."""

        self.bit_depth: BleSetting[Params.BitDepth] = BleSetting[Params.BitDepth](
            communicator,
            SettingId.BIT_DEPTH,
            Params.BitDepth,
        )
        """System Video Bit depth."""

        self.video_profile: BleSetting[Params.VideoProfile] = BleSetting[Params.VideoProfile](
            communicator,
            SettingId.VIDEO_PROFILE,
            Params.VideoProfile,
        )
        """Video Profile (hdr, etc.)"""

        self.video_aspect_ratio: BleSetting[Params.VideoAspectRatio] = BleSetting[Params.VideoAspectRatio](
            communicator,
            SettingId.VIDEO_ASPECT_RATIO,
            Params.VideoAspectRatio,
        )
        """Video aspect ratio"""

        self.video_easy_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.VIDEO_EASY_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Video easy aspect ratio"""

        self.multi_shot_easy_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_EASY_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Multi shot easy aspect ratio"""

        self.multi_shot_nlv_aspect_ratio: BleSetting[Params.EasyAspectRatio] = BleSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_NLV_ASPECT_RATIO,
            Params.EasyAspectRatio,
        )
        """Multi shot NLV aspect ratio"""

        self.video_mode: BleSetting[Params.VideoMode] = BleSetting[Params.VideoMode](
            communicator,
            SettingId.VIDEO_MODE,
            Params.VideoMode,
        )
        """Video Mode (i.e. quality)"""

        self.timelapse_mode: BleSetting[Params.TimelapseMode] = BleSetting[Params.TimelapseMode](
            communicator,
            SettingId.TIMELAPSE_MODE,
            Params.TimelapseMode,
        )
        """Timelapse Mode"""

        self.maxlens_mod_type: BleSetting[Params.MaxLensModType] = BleSetting[Params.MaxLensModType](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD,
            Params.MaxLensModType,
        )
        """Max lens mod? If so, what type?"""

        self.maxlens_status: BleSetting[Params.Toggle] = BleSetting[Params.Toggle](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD_ENABLE,
            Params.Toggle,
        )
        """Enable / disable max lens mod"""

        self.photo_mode: BleSetting[Params.PhotoMode] = BleSetting[Params.PhotoMode](
            communicator,
            SettingId.PHOTO_MODE,
            Params.PhotoMode,
        )
        """Photo Mode"""

        self.framing: BleSetting[Params.Framing] = BleSetting[Params.Framing](
            communicator,
            SettingId.FRAMING,
            Params.Framing,
        )
        """Video Framing Mode"""

        self.hindsight: BleSetting[Params.Hindsight] = BleSetting[Params.Hindsight](
            communicator,
            SettingId.HINDSIGHT,
            Params.Hindsight,
        )
        """Hindsight time / disable"""

        self.photo_interval: BleSetting[Params.PhotoInterval] = BleSetting[Params.PhotoInterval](
            communicator,
            SettingId.PHOTO_INTERVAL,
            Params.PhotoInterval,
        )
        """Interval between photo captures"""

        self.photo_duration: BleSetting[Params.PhotoDuration] = BleSetting[Params.PhotoDuration](
            communicator,
            SettingId.PHOTO_INTERVAL_DURATION,
            Params.PhotoDuration,
        )
        """Interval between photo captures"""

        self.photo_output: BleSetting[Params.PhotoOutput] = BleSetting[Params.PhotoOutput](
            communicator,
            SettingId.PHOTO_OUTPUT,
            Params.PhotoOutput,
        )
        """File type of photo output"""

        self.video_duration: BleSetting[Params.VideoDuration] = BleSetting[Params.VideoDuration](
            communicator, SettingId.VIDEO_DURATION, Params.VideoDuration
        )
        """If set, a video will automatically be stopped after recording for this long."""

        self.regional_format: BleSetting[Params.RegionalFormat] = BleSetting[Params.RegionalFormat](
            communicator, SettingId.REGIONAL_FORMAT, Params.RegionalFormat
        )

        self.quality_control: BleSetting[Params.QualityControl] = BleSetting[Params.QualityControl](
            communicator, SettingId.QUALITY_CONTROL, Params.QualityControl
        )

        self.camera_volume: BleSetting[Params.Volume] = BleSetting[Params.Volume](
            communicator, SettingId.CAMERA_VOLUME, Params.Volume
        )

        self.lens_attachment: BleSetting[Params.LensAttachment] = BleSetting[Params.LensAttachment](
            communicator, SettingId.LENS_ATTACHMENT, Params.LensAttachment
        )

        self.setup_screensaver: BleSetting[Params.ScreenSaverTimeout] = BleSetting[Params.ScreenSaverTimeout](
            communicator, SettingId.SETUP_SCREEN_SAVER, Params.ScreenSaverTimeout
        )

        self.setup_language: BleSetting[Params.SetupLanguage] = BleSetting[Params.SetupLanguage](
            communicator, SettingId.SETUP_LANGUAGE, Params.SetupLanguage
        )

        self.auto_power_off: BleSetting[Params.AutoPowerOff] = BleSetting[Params.AutoPowerOff](
            communicator, SettingId.AUTO_POWER_OFF, Params.AutoPowerOff
        )

        self.photo_mode_v2: BleSetting[Params.PhotoModeV2] = BleSetting[Params.PhotoModeV2](
            communicator, SettingId.PHOTO_MODE_V2, Params.PhotoModeV2
        )

        self.video_digital_lens_v2: BleSetting[Params.VideoLensV2] = BleSetting[Params.VideoLensV2](
            communicator, SettingId.VIDEO_DIGITAL_LENSES_V2, Params.VideoLensV2
        )

        self.photo_digital_lens_v2: BleSetting[Params.PhotoLensV2] = BleSetting[Params.PhotoLensV2](
            communicator, SettingId.PHOTO_DIGITAL_LENSES_V2, Params.PhotoLensV2
        )

        self.timelapse_digital_lens_v2: BleSetting[Params.TimelapseLensV2] = BleSetting[Params.TimelapseLensV2](
            communicator, SettingId.TIMELAPSE_DIGITAL_LENSES_V2, Params.TimelapseLensV2
        )

        self.video_framing: BleSetting[Params.VideoFraming] = BleSetting[Params.VideoFraming](
            communicator, SettingId.VIDEO_FRAMING, Params.VideoFraming
        )

        self.multi_shot_framing: BleSetting[Params.MultishotFraming] = BleSetting[Params.MultishotFraming](
            communicator, SettingId.MULTI_SHOT_FRAMING, Params.MultishotFraming
        )

        self.frame_rate: BleSetting[Params.FrameRate] = BleSetting[Params.FrameRate](
            communicator, SettingId.FRAME_RATE, Params.FrameRate
        )

        super().__init__(communicator)
