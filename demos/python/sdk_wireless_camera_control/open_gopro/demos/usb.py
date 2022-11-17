import argparse

from rich.console import Console

from open_gopro import WiredGoPro, Params
from open_gopro.util import setup_logging, add_cli_args_and_parse

console = Console()  # rich consoler printer


def main(args: argparse.Namespace) -> None:
    logger = setup_logging(__name__, args.log)

    with WiredGoPro(args.identifier) as gopro:
        # Get media list
        logger.critical("Testing a command")
        gopro.http_command.get_webcam_version()

    gopro.close()
    console.print("Exiting...")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exercise the GoPro's USB interface.")
    return add_cli_args_and_parse(parser, wifi=False)


# Needed for poetry scripts defined in pyproject.toml
def entrypoint() -> None:
    main(parse_arguments())


if __name__ == "__main__":
    entrypoint()
