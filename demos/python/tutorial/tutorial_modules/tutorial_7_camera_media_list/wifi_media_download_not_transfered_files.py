# wifi_media_download_file.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:05 PM

import json
import logging
import argparse
from typing import Dict, Any, Optional

import requests

from tutorial_modules import GOPRO_BASE_URL, get_media_list
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    # Get the media list
    media_list = get_media_list()

    # Find a photo. We're just taking the first one we find.
    photo: Optional[str] = []
    hero_video: Optional[str] = []
    sphere_video: Optional[str] = []
    for media_file in [x["n"] for x in media_list["media"][0]["fs"]]:
        if media_file.lower().endswith(".jpg"):
            logger.info(f"found a photo: {media_file}")
            photo.append(media_file)
        elif media_file.lower().endswith(".mp4"):
            logger.info(f"found a hero video: {media_file}")
            hero_video.append(media_file)
        elif media_file.lower().endswith(".360"):
            logger.info(f"found a sphere video: {media_file}")
            sphere_video.append(media_file)

    # if len(photo) == len(hero_video) == len(sphere_video) == 0:
    #     raise Exception("Couldn't find a any media on the GoPro")

    # ディレクトリ内のファイル一覧取得
    


    # Build the url to get the thumbnail data for the photo
    for media_list, file_ext in zip([sphere_video], [".360"]):
        for media_file in media_list:
            logger.info(f"Downloading {media_file}")
            url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{media_file}"
            logger.info(f"Sending: {url}")
            with requests.get(url, stream=True) as request:
                request.raise_for_status()
                file = media_file.split(".")[0] + file_ext
                with open(file, "wb") as f:
                    logger.info(f"receiving binary stream to {file}...")
                    for chunk in request.iter_content(chunk_size=8192):
                        f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find a media on the camera and download it to the computer.")
    parser.add_argument("--dir_path", type=str)
    parser.parse_args()
    main()
