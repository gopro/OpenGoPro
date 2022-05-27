# wifi_media_get_screennail.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:06 PM

import sys
import logging
import argparse
from typing import Optional

import requests

from tutorial_modules import GOPRO_BASE_URL, get_media_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main() -> None:
    # Get the media list
    media_list = get_media_list()

    # Find a photo. We're just taking the first one we find.
    photo: Optional[str] = None
    for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
        if media_file.lower().endswith(".jpg"):
            logger.info(f"found a photo: {media_file}")
            photo = media_file
            break
    else:
        raise Exception("Couldn't find a photo on the GoPro")

    assert photo is not None
    # Build the url to get the screennail data for the photo
    logger.info(f"Getting the screennail for {photo}")
    url = GOPRO_BASE_URL + f"/gopro/media/screennail?path=100GOPRO/{photo}"
    logger.info(f"Sending: {url}")
    with requests.get(url, stream=True) as request:
        request.raise_for_status()
        file = photo.split(".")[0] + "_screennail.jpg"
        with open(file, "wb") as f:
            logger.info(f"receiving binary stream to {file}...")
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the screennail for a media file.")
    parser.parse_args()

    try:
        main()
    except:
        sys.exit(-1)
    else:
        sys.exit(0)