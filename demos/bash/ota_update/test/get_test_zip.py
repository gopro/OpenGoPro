# get_test_zip.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Oct 19 15:33:20 UTC 2022

import sys
import json
import enum
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Final, Optional

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Camera(enum.Enum):
    HERO_9 = "HERO9 Black"
    HERO_10 = "HERO10 Black"
    HERO_11 = "HERO11 Black"


cameras: Final[list[str]] = [camera.name for camera in Camera]

FW_CATALOG: Final = r"https://api.gopro.com/firmware/v2/catalog"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get the firmware catalog JSON, extract the camera OTA URL, and download the .zip"
    )
    parser.add_argument("camera", type=str, choices=cameras, help=f"Camera to get FW for")
    parser.add_argument("-d", "--debug", action="store_true", help="Set to output debug information")
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    # Configure logging
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Get firmware catalog
    target = eval(f"Camera.{args.camera}").value
    logger.info(f"Getting .zip for camera: {target}")
    with requests.get(FW_CATALOG, timeout=10) as response:
        response.raise_for_status()
        catalog = json.loads(response.text)
        if logger.level == logging.DEBUG:
            logger.debug(json.dumps(catalog, indent=4))

    # Extract link for camera-specific firmware
    fw_url: Optional[str] = None
    for camera in catalog["cameras"]:
        if camera["name"] == target:
            fw_url = camera["url"]
            logger.info(f"FW URL is: {fw_url}")
            break
    else:
        raise RuntimeError("Firmware URL not found in firmware catalog")

    # Download zip
    assert fw_url
    local_filename = Path("UPDATE.zip")
    logger.info(f"Downloading zip to {local_filename}")
    with requests.get(fw_url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, "wb") as fp:
            for chunk in response.iter_content(chunk_size=8192):
                fp.write(chunk)

if __name__ == "__main__":
    main(parse_arguments())
