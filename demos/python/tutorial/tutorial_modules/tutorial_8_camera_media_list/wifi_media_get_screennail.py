# wifi_media_get_screennail.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:06 PM

import sys
import argparse

import requests

from tutorial_modules import GOPRO_BASE_URL, get_media_list, logger


def main() -> None:
    # Get the media list
    media_list = get_media_list()

    # Find a photo. We're just taking the first one we find.
    photo: str | None = None
    directory: str | None = None
    found_photo = False
    # TODO update tutorial docs to get directory
    for media in media_list["media"]:
        for media_file in [x["n"] for x in media["fs"]]:
            if media_file.lower().endswith(".jpg"):
                logger.info(f"found a photo: {media_file}")
                photo = media_file
                directory = media["d"]
                found_photo = True
                break
        if found_photo:
            break
    else:
        raise RuntimeError("Couldn't find a photo on the GoPro")

    assert photo
    assert directory
    # Build the url to get the screennail data for the photo
    logger.info(f"Getting the screennail for {photo}")
    url = GOPRO_BASE_URL + f"/gopro/media/screennail?path={directory}/{photo}"
    logger.info(f"Sending: {url}")
    with requests.get(url, stream=True, timeout=10) as request:
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
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
