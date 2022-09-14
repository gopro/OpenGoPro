# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:55 PM

# Open GoPro API Versions to test
versions = ["2.0"]

from open_gopro.api import Api

# The global parser map only gets set when API is instantiated. So ensure this is done.
Api(None)  # type: ignore
