# wifi_command_load_preset.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:03 PM

import sys
import json
import logging
import argparse

import requests

from tutorial_modules import GOPRO_BASE_URL

from tutorial_modules import logger


def main(preset_id: int) -> None:
    # Build the HTTP GET request
    url = GOPRO_BASE_URL + "/gopro/camera/presets/load?id={preset_id}"
    logger.info(f"Loading preset id {preset_id}: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load a preset by ID.")
    parser.add_argument(
        "-i",
        "--identifier",
        type=int,
        help="Preset ID to load. Default to 2 (Cinematic)",
        default=2,
    )
    args = parser.parse_args()

    try:
        main(args.identifier)
    except Exception as e:
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
