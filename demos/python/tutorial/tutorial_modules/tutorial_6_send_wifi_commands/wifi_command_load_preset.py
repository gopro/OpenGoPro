# wifi_command_load_preset.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:51 UTC 2021

import json
import logging
import argparse

import requests

from tutorial_modules import GOPRO_BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    # Build the HTTP GET request
    url = GOPRO_BASE_URL + "/gopro/camera/presets/load?id=2"
    logger.info(f"Loading the cinematic preset: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load the cinematic preset.")
    parser.parse_args()
    main()
