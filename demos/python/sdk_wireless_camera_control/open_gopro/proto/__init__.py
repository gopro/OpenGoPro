# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""Protobufs that will be needed by the user.

They are imported here so they can be imported from open_gopro.proto
"""

from open_gopro.proto.live_streaming_pb2 import (
    EnumLens,
    EnumLiveStreamStatus,
    EnumRegisterLiveStreamStatus,
    EnumWindowSize,
    NotifyLiveStreamStatus,
    RequestGetLiveStreamStatus,
    RequestSetLiveStreamMode,
)
from open_gopro.proto.network_management_pb2 import (
    EnumNetworkOwner,
    EnumProvisioning,
    EnumScanEntryFlags,
    EnumScanning,
    NotifProvisioningState,
    NotifStartScanning,
    RequestConnect,
    RequestConnectNew,
    RequestGetApEntries,
    RequestReleaseNetwork,
    RequestStartScan,
    ResponseConnect,
    ResponseConnectNew,
    ResponseGetApEntries,
    ResponseStartScanning,
    ScanEntry,
)
from open_gopro.proto.preset_status_pb2 import (
    EnumPresetGroup,
    NotifyPresetStatus,
    Preset,
    PresetGroup,
    PresetSetting,
)
from open_gopro.proto.request_get_preset_status_pb2 import (
    EnumRegisterPresetStatus,
    RequestGetPresetStatus,
)
from open_gopro.proto.response_generic_pb2 import EnumResultGeneric, ResponseGeneric
from open_gopro.proto.set_camera_control_status_pb2 import (
    EnumCameraControlStatus,
    RequestSetCameraControlStatus,
)
from open_gopro.proto.turbo_transfer_pb2 import RequestSetTurboActive
