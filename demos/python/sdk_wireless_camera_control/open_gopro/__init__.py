# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:51 PM

# pylint: disable=wrong-import-position

"""All GoPro exports that the the user will want should be exported here."""

import sys

if sys.version_info.major != 3 or not 9 <= sys.version_info.minor < 11:
    raise RuntimeError("Python >= 3.9 and < 3.11 must be used")

import logging

from open_gopro.util import Logger

Logger.addLoggingLevel("TRACE", logging.DEBUG - 5)

from open_gopro.gopro import WirelessGoPro, WiredGoPro
from open_gopro.api import Params
from open_gopro.responses import GoProResp
