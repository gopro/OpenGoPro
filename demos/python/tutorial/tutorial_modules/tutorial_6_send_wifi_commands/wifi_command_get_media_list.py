# wifi_command_get_media_list.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:01 PM

import sys
import json
import argparse
from typing import Dict, Any

import requests

from tutorial_modules import GOPRO_BASE_URL, logger


def get_media_list() -> Dict[str, Any]:
    """Read the media list from the camera and return as JSON

    Returns:
        Dict[str, Any]: complete media list as JSON
    """
    # Build the HTTP GET request
    url = GOPRO_BASE_URL + "/gopro/media/list"
    logger.info(f"Getting the media list: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url, timeout=10)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")

    return response.json()


def main() -> None:
    get_media_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the media list.")
    parser.parse_args()
    main()

    try:
        main()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
