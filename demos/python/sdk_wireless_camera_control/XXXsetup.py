# setup.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

"""Package definition"""

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


entry_points = {
    "console_scripts": [
        "gopro-demo=open_gopro.demos.demo:main",
        "gopro-photo=open_gopro.demos.photo:entrypoint",
        "gopro-video=open_gopro.demos.video:main",
        "gopro-stream=open_gopro.demos.stream:main",
        "gopro-log-battery=open_gopro.demos.log_battery:main",
        "gopro-wifi=open_gopro.demos.connect_wifi:main",
        "gopro-ble-write=open_gopro.demos.ble_write:main",
    ]
}
classifiers = [
    # Trove classifiers
    # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Intended Audience :: Developers",
    "Topic :: Communications",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
]
# setup.py publish support.
cmdclass = {"upload": UploadCommand}
