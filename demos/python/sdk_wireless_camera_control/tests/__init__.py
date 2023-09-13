# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

# Open GoPro API Versions to test
versions = ["2.0"]

from open_gopro import GoProResp, constants
from open_gopro.api import WirelessApi

# The global parser map only gets set when API is instantiated. So ensure this is done.
WirelessApi(None)  # type: ignore

mock_good_response = GoProResp(
    protocol=GoProResp.Protocol.BLE,
    status=constants.ErrorCode.SUCCESS,
    identifier="test response",
    data=None,
)
