"""HTTP Settings"""

from open_gopro.api.builders import HttpSetting
from open_gopro.communicator_interface import GoProHttp, HttpMessages
from open_gopro.constants import SettingId

from . import params as Params


class HttpSettings(HttpMessages[HttpSetting]):
    # pylint: disable=missing-class-docstring, unused-argument
    """The collection of all HTTP Settings

    Args:
        communicator (GoProHttp): Adapter to read / write settings
    """

    def __init__(self, communicator: GoProHttp):
        self.resolution: HttpSetting[Params.Resolution] = HttpSetting[Params.Resolution](
            communicator, SettingId.RESOLUTION
        )
        """Resolution."""

        self.fps: HttpSetting[Params.FPS] = HttpSetting[Params.FPS](communicator, SettingId.FPS)
        """Frames per second."""

        self.auto_off: HttpSetting[Params.AutoOff] = HttpSetting[Params.AutoOff](communicator, SettingId.AUTO_OFF)
        """Set the auto off time."""

        self.video_field_of_view: HttpSetting[Params.VideoFOV] = HttpSetting[Params.VideoFOV](
            communicator, SettingId.VIDEO_FOV
        )
        """Video FOV."""

        self.photo_field_of_view: HttpSetting[Params.PhotoFOV] = HttpSetting[Params.PhotoFOV](
            communicator, SettingId.PHOTO_FOV
        )
        """Photo FOV."""

        self.multi_shot_field_of_view: HttpSetting[Params.MultishotFOV] = HttpSetting[Params.MultishotFOV](
            communicator, SettingId.MULTI_SHOT_FOV
        )
        """Multi-shot FOV."""

        self.max_lens_mode: HttpSetting[Params.MaxLensMode] = HttpSetting[Params.MaxLensMode](
            communicator, SettingId.MAX_LENS_MOD
        )
        """Enable / disable max lens mod."""

        self.hypersmooth: HttpSetting[Params.HypersmoothMode] = HttpSetting[Params.HypersmoothMode](
            communicator, SettingId.HYPERSMOOTH
        )
        """Set / disable hypersmooth."""

        self.video_performance_mode: HttpSetting[Params.PerformanceMode] = HttpSetting[Params.PerformanceMode](
            communicator, SettingId.VIDEO_PERFORMANCE_MODE
        )
        """Video Performance Mode (extended battery, tripod, etc)."""

        self.media_format: HttpSetting[Params.MediaFormat] = HttpSetting[Params.MediaFormat](
            communicator, SettingId.MEDIA_FORMAT
        )
        """Set the media format."""

        self.anti_flicker: HttpSetting[Params.AntiFlicker] = HttpSetting[Params.AntiFlicker](
            communicator, SettingId.ANTI_FLICKER
        )
        """Anti Flicker frequency."""

        self.camera_ux_mode: HttpSetting[Params.CameraUxMode] = HttpSetting[Params.CameraUxMode](
            communicator, SettingId.CAMERA_UX_MODE
        )
        """Camera controls configuration."""

        self.video_easy_mode: HttpSetting[int] = HttpSetting[int](communicator, SettingId.VIDEO_EASY_MODE)
        """Video easy mode speed."""

        self.photo_easy_mode: HttpSetting[Params.PhotoEasyMode] = HttpSetting[Params.PhotoEasyMode](
            communicator, SettingId.PHOTO_EASY_MODE
        )
        """Night Photo easy mode."""

        self.wifi_band: HttpSetting[Params.WifiBand] = HttpSetting[Params.WifiBand](communicator, SettingId.WIFI_BAND)
        """Current WiFi band being used."""

        self.star_trail_length: HttpSetting[Params.StarTrailLength] = HttpSetting[Params.StarTrailLength](
            communicator, SettingId.STAR_TRAIL_LENGTH
        )
        """Multi shot star trail length."""

        self.system_video_mode: HttpSetting[Params.SystemVideoMode] = HttpSetting[Params.SystemVideoMode](
            communicator, SettingId.SYSTEM_VIDEO_MODE
        )
        """System video mode."""

        self.video_horizon_leveling: HttpSetting[Params.HorizonLeveling] = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.VIDEO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for video."""

        self.photo_horizon_leveling: HttpSetting[Params.HorizonLeveling] = HttpSetting[Params.HorizonLeveling](
            communicator, SettingId.PHOTO_HORIZON_LEVELING
        )
        """Lock / unlock horizon leveling for photo."""

        self.bit_rate: HttpSetting[Params.BitRate] = HttpSetting[Params.BitRate](
            communicator,
            SettingId.BIT_RATE,
        )
        """System Video Bit Rate."""

        self.bit_depth: HttpSetting[Params.BitDepth] = HttpSetting[Params.BitDepth](
            communicator,
            SettingId.BIT_DEPTH,
        )
        """System Video Bit depth."""

        self.video_profile: HttpSetting[Params.VideoProfile] = HttpSetting[Params.VideoProfile](
            communicator,
            SettingId.VIDEO_PROFILE,
        )
        """Video Profile (hdr, etc.)"""

        self.video_aspect_ratio: HttpSetting[Params.VideoAspectRatio] = HttpSetting[Params.VideoAspectRatio](
            communicator,
            SettingId.VIDEO_ASPECT_RATIO,
        )
        """Video aspect ratio"""

        self.video_easy_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.VIDEO_EASY_ASPECT_RATIO,
        )
        """Video easy aspect ratio"""

        self.multi_shot_easy_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_EASY_ASPECT_RATIO,
        )
        """Multi shot easy aspect ratio"""

        self.multi_shot_nlv_aspect_ratio: HttpSetting[Params.EasyAspectRatio] = HttpSetting[Params.EasyAspectRatio](
            communicator,
            SettingId.MULTI_SHOT_NLV_ASPECT_RATIO,
        )
        """Multi shot NLV aspect ratio"""

        self.video_mode: HttpSetting[Params.VideoMode] = HttpSetting[Params.VideoMode](
            communicator,
            SettingId.VIDEO_MODE,
        )
        """Video Mode (i.e. quality)"""

        self.timelapse_mode: HttpSetting[Params.TimelapseMode] = HttpSetting[Params.TimelapseMode](
            communicator,
            SettingId.TIMELAPSE_MODE,
        )
        """Timelapse Mode"""

        self.maxlens_mod_type: HttpSetting[Params.MaxLensModType] = HttpSetting[Params.MaxLensModType](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD,
        )
        """Max lens mod? If so, what type?"""

        self.maxlens_status: HttpSetting[Params.Toggle] = HttpSetting[Params.Toggle](
            communicator,
            SettingId.ADDON_MAX_LENS_MOD_ENABLE,
        )
        """Enable / disable max lens mod"""

        self.photo_mode: HttpSetting[Params.PhotoMode] = HttpSetting[Params.PhotoMode](
            communicator,
            SettingId.PHOTO_MODE,
        )
        """Photo Mode"""

        self.framing: HttpSetting[Params.Framing] = HttpSetting[Params.Framing](
            communicator,
            SettingId.FRAMING,
        )
        """Video Framing Mode"""

        self.hindsight: HttpSetting[Params.Hindsight] = HttpSetting[Params.Hindsight](
            communicator,
            SettingId.HINDSIGHT,
        )
        """Hindsight time / disable"""

        self.photo_interval: HttpSetting[Params.PhotoInterval] = HttpSetting[Params.PhotoInterval](
            communicator,
            SettingId.PHOTO_INTERVAL,
        )
        """Interval between photo captures"""

        self.photo_duration: HttpSetting[Params.PhotoDuration] = HttpSetting[Params.PhotoDuration](
            communicator,
            SettingId.PHOTO_INTERVAL_DURATION,
        )
        """Interval between photo captures"""

        self.photo_output: HttpSetting[Params.PhotoOutput] = HttpSetting[Params.PhotoOutput](
            communicator,
            SettingId.PHOTO_OUTPUT,
        )
        """File type of photo output"""

        self.video_duration: HttpSetting[Params.VideoDuration] = HttpSetting[Params.VideoDuration](
            communicator, SettingId.VIDEO_DURATION
        )
        """If set, a video will automatically be stopped after recording for this long."""

        self.regional_format: HttpSetting[Params.RegionalFormat] = HttpSetting[Params.RegionalFormat](
            communicator, SettingId.REGIONAL_FORMAT
        )

        self.quality_control: HttpSetting[Params.QualityControl] = HttpSetting[Params.QualityControl](
            communicator, SettingId.QUALITY_CONTROL
        )

        self.camera_volume: HttpSetting[Params.Volume] = HttpSetting[Params.Volume](
            communicator, SettingId.CAMERA_VOLUME
        )

        self.lens_attachment: HttpSetting[Params.LensAttachment] = HttpSetting[Params.LensAttachment](
            communicator, SettingId.LENS_ATTACHMENT
        )

        self.setup_screensaver: HttpSetting[Params.ScreenSaverTimeout] = HttpSetting[Params.ScreenSaverTimeout](
            communicator, SettingId.SETUP_SCREEN_SAVER
        )

        self.setup_language: HttpSetting[Params.SetupLanguage] = HttpSetting[Params.SetupLanguage](
            communicator, SettingId.SETUP_LANGUAGE
        )

        self.auto_power_off: HttpSetting[Params.AutoPowerOff] = HttpSetting[Params.AutoPowerOff](
            communicator, SettingId.AUTO_POWER_OFF
        )

        self.photo_mode_v2: HttpSetting[Params.PhotoModeV2] = HttpSetting[Params.PhotoModeV2](
            communicator, SettingId.PHOTO_MODE_V2
        )

        self.video_digital_lens_v2: HttpSetting[Params.VideoLensV2] = HttpSetting[Params.VideoLensV2](
            communicator, SettingId.VIDEO_DIGITAL_LENSES_V2
        )

        self.photo_digital_lens_v2: HttpSetting[Params.PhotoLensV2] = HttpSetting[Params.PhotoLensV2](
            communicator, SettingId.PHOTO_DIGITAL_LENSES_V2
        )

        self.timelapse_digital_lens_v2: HttpSetting[Params.TimelapseLensV2] = HttpSetting[Params.TimelapseLensV2](
            communicator, SettingId.TIMELAPSE_DIGITAL_LENSES_V2
        )

        self.video_framing: HttpSetting[Params.VideoFraming] = HttpSetting[Params.VideoFraming](
            communicator, SettingId.VIDEO_FRAMING
        )

        self.multi_shot_framing: HttpSetting[Params.MultishotFraming] = HttpSetting[Params.MultishotFraming](
            communicator, SettingId.MULTI_SHOT_FRAMING
        )

        self.frame_rate: HttpSetting[Params.FrameRate] = HttpSetting[Params.FrameRate](
            communicator, SettingId.FRAME_RATE
        )

        super().__init__(communicator)
