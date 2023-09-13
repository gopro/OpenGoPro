# __init__.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 23 22:43:52 UTC 2023

"""Common GUI demos. Ensure that additional GUI options were installed before continuing"""

import sys

try:
    import tkinter

    import cv2
    import PIL

except ModuleNotFoundError:
    print(
        "Required GUI dependencies not found. See the installation steps: https://gopro.github.io/OpenGoPro/python_sdk/installation.html"
    )
    sys.exit(1)
