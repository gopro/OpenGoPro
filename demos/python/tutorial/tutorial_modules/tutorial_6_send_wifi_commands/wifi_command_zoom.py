# wifi_command_zoom.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:04 PM

import sys
import json
import logging
import argparse

import requests

from tutorial_modules import GOPRO_BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main(zoom: int) -> None:
    # Build the HTTP GET request
    url = GOPRO_BASE_URL + f"/gopro/camera/digital_zoom?percent={zoom}"
    logger.info(f"Setting digital zoom to {zoom}%: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set the digital zoom level.")
    parser.add_argument(
        "-z",
        "--zoom",
        type=int,
        help="Zoom percentage (0-100)",
        default=50,
    )
    args = parser.parse_args()

    try:
        main(args.zoom)
    except:
        sys.exit(-1)
    else:
        sys.exit(0)
