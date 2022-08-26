# reconnect_test.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Aug 26 22:44:36 UTC 2022

import logging

from open_gopro import GoPro
from open_gopro.util import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    global logger
    logger = setup_logging(logger)

    while True:
        with GoPro(enable_wifi=False) as gopro:
            pass


def entrypoint() -> None:
    main()


if __name__ == "__main__":
    entrypoint()
