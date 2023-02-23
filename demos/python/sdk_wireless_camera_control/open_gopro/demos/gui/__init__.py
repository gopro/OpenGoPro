"""Common GUI demos. Ensure that additional GUI options were installed before continuing"""

import sys

try:
    import tkinter
    import PIL
    import cv2

except ModuleNotFoundError:
    print(
        "Required GUI dependencies not found. See the installation steps; https://gopro.github.io/OpenGoPro/python_sdk/installation.html"
    )
    sys.exit(1)
