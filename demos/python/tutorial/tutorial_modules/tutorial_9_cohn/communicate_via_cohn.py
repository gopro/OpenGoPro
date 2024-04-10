# communicate_via_cohn.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

import sys
import json
import argparse
import asyncio
from base64 import b64encode
from pathlib import Path

import requests

from tutorial_modules import logger


async def main(ip_address: str, username: str, password: str, certificate: Path) -> None:
    url = f"https://{ip_address}" + "/gopro/camera/state"
    logger.debug(f"Sending:  {url}")

    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    response = requests.get(
        url,
        timeout=10,
        headers={"Authorization": f"Basic {token}"},
        verify=str(certificate),
    )
    # Check for errors (if an error is found, an exception will be raised)
    response.raise_for_status()
    logger.info("Command sent successfully")
    # Log response as json
    logger.info(f"Response: {json.dumps(response.json(), indent=4)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate HTTPS communication via COHN.")
    parser.add_argument("ip_address", type=str, help="IP Address of camera on the home network")
    parser.add_argument("username", type=str, help="COHN username")
    parser.add_argument("password", type=str, help="COHN password")
    parser.add_argument("certificate", type=Path, help="Path to read COHN cert from.", default=Path("cohn.crt"))
    args = parser.parse_args()

    try:
        asyncio.run(main(args.ip_address, args.username, args.password, args.certificate))
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
