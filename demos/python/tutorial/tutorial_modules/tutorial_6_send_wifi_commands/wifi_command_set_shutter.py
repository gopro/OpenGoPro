# wifi_command_set_shutter.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:04 PM

import sys
import time
import logging
import argparse

import requests

from tutorial_modules import GOPRO_BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main() -> None:
    # Build the HTTP GET request
    shutter_on_url = GOPRO_BASE_URL + "/gopro/camera/shutter/start"
    logger.info(f"Turning the shutter on: sending {shutter_on_url}")

    # Send the GET request and retrieve the response
    response = requests.get(shutter_on_url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")

    time.sleep(3)

    # Build the HTTP GET request
    shutter_off_url = GOPRO_BASE_URL + "/gopro/camera/shutter/stop"
    logger.info(f"Turning the shutter off: sending {shutter_off_url}")

    # Send the GET request and retrieve the response
    response = requests.get(shutter_off_url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a 3 second video.")
    parser.parse_args()

    try:
        main()
    except:
        sys.exit(-1)
    else:
        sys.exit(0)
