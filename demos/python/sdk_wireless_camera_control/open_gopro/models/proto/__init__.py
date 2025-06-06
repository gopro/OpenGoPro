# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Protobufs that will be needed by the user.

They are imported here so they can be imported from
"""
from .cohn_pb2 import (
    EnumCOHNNetworkState,
    EnumCOHNStatus,
    NotifyCOHNStatus,
    RequestClearCOHNCert,
    RequestCOHNCert,
    RequestCreateCOHNCert,
    RequestGetCOHNStatus,
    RequestSetCOHNSetting,
    ResponseCOHNCert,
)
from .live_streaming_pb2 import (
    EnumLens,
    EnumLiveStreamStatus,
    EnumRegisterLiveStreamStatus,
    EnumWindowSize,
    NotifyLiveStreamStatus,
    RequestGetLiveStreamStatus,
    RequestSetLiveStreamMode,
)
from .media_pb2 import (
    RequestGetLastCapturedMedia,
    ResponseLastCapturedMedia,
)
from .network_management_pb2 import (
    EnumProvisioning,
    EnumScanEntryFlags,
    EnumScanning,
    NotifProvisioningState,
    NotifStartScanning,
    RequestConnect,
    RequestConnectNew,
    RequestGetApEntries,
    RequestPairingFinish,
    RequestReleaseNetwork,
    RequestStartScan,
    ResponseConnect,
    ResponseConnectNew,
    ResponseGetApEntries,
    ResponseStartScanning,
)
from .preset_status_pb2 import (
    EnumPresetGroup,
    EnumPresetIcon,
    EnumPresetTitle,
    NotifyPresetStatus,
    Preset,
    PresetGroup,
    PresetSetting,
    RequestCustomPresetUpdate,
)
from .request_get_preset_status_pb2 import (
    EnumRegisterPresetStatus,
    RequestGetPresetStatus,
)
from .response_generic_pb2 import (
    EnumResultGeneric,
    Media,
    ResponseGeneric,
)
from .set_camera_control_status_pb2 import (
    EnumCameraControlStatus,
    RequestSetCameraControlStatus,
)
from .turbo_transfer_pb2 import RequestSetTurboActive
