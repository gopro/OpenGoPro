# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:51 PM

"""All GoPro exports that the the user will want should be exported here."""

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version(__name__)

from open_gopro.gopro import GoPro
from open_gopro.api import Params
from open_gopro.responses import GoProResp
