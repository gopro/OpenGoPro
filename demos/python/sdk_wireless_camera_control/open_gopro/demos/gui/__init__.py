# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 17 20:05:18 UTC 2022

"""Common GUI functionality"""

import platform
from typing import Union

from open_gopro.api.builders import BleCommand, WifiCommand
from open_gopro.api import BleSettings, BleCommands, BleStatuses, WifiCommands, WifiSettings

if (OS := platform.system().lower()) == "windows":
    THEME = "vista"
elif OS == "darwin":
    THEME = "aqua"
else:
    THEME = "default"
