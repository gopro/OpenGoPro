# wifi_command_get_media_list.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:01 PM

import sys
import json
import logging
import argparse
from typing import Dict, Any

import requests

from tutorial_modules import GOPRO_BASE_URL, GOPRO_MAX
import datetime
import copy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_media_list() -> Dict[str, Any]:
    # Build the HTTP GET request
    if GOPRO_MAX:
        url = GOPRO_BASE_URL + "/gp/gpMediaList"
    else:
        url = GOPRO_BASE_URL + "/gopro/media/list"
    logger.info(f"Getting the media list: sending {url}")

    # Send the GET request and retrieve the response
    response = requests.get(url)
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    response_dict = response.json()
    """
    example of response_dict:
        {'id': '493867230981820640', 'media': [{'d': '100GOPRO', 'fs':
             [{'n': 'GH010047.MP4', 'cre': '1452234910', 'mod': '1452234910', 'glrv': '1150765', 'ls': '-1', 's': '11948174'},
             {'n': 'GS010048.360', 'cre': '1452240700', 'mod': '1452240700', 'ls': '1677571', 's': '39469556'},
             {'n': 'GS__0049.JPG', 'cre': '1452246178', 'mod': '1452246178', 's': '4753116'},
             {'n': 'GS010050.360', 'cre': '1452246186', 'mod': '1452246186', 'ls': '3520002', 's': '82411500'},
             {'n': 'GS010051.360', 'cre': '1642554304', 'mod': '1642554304', 'ls': '1269840', 's': '27133372'},
             {'n': 'GS010052.360', 'cre': '1642691456', 'mod': '1642691456', 'ls': '1155460', 's': '23906619'}]}]}
    """
    modified_response_dict = copy.deepcopy(response_dict)
    medias = response_dict["media"]
    for media_idx, media in enumerate(medias):
        for file_idx, file in enumerate(media["fs"]):
            creation_unix_time = file["cre"]
            creation_dt_jst_aware = datetime.datetime.fromtimestamp(float(creation_unix_time))
            modified_response_dict["media"][media_idx]["fs"][file_idx]["creation_datetime"] = creation_dt_jst_aware.isoformat()

    # Log response as json
    logger.info(f"Response: {json.dumps(modified_response_dict, indent=4)}")

    return response.json()


def main() -> None:
    get_media_list()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the media list.")
    parser.parse_args()
    main()

    try:
        main()
    except:
        sys.exit(-1)
    else:
        sys.exit(0)
