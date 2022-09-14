# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:49 PM

"""All Protobuf defnitions."""

from open_gopro.proto.turbo_transfer_pb2 import RequestSetTurboActive
from open_gopro.proto.response_generic_pb2 import ResponseGeneric
from open_gopro.proto.request_get_preset_status_pb2 import RequestGetPresetStatus
from open_gopro.proto.preset_status_pb2 import NotifyPresetStatus
from open_gopro.proto.set_camera_control_status_pb2 import RequestSetCameraControlStatus
from open_gopro.proto.live_streaming_pb2 import (
    RequestSetLiveStreamMode,
    RequestGetLiveStreamStatus,
    NotifyLiveStreamStatus,
)
from open_gopro.proto.network_management_pb2 import (
    RequestConnectNew,
    ResponseConnectNew,
    NotifProvisioningState,
)
