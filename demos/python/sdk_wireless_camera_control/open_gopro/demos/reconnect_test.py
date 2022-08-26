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
