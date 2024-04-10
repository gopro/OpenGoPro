# protobuf_example.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:49 UTC 2024

import sys
import argparse

from tutorial_modules import logger, proto


def main() -> None:
    request = proto.RequestSetTurboActive(active=False)
    logger.info(f"Sending ==> {request}")
    logger.info(request.SerializeToString().hex(":"))

    # We're not hard-coding serialized bytes here since it may not be constant across Protobuf versions
    response_bytes = proto.ResponseGeneric(result=proto.EnumResultGeneric.RESULT_SUCCESS).SerializeToString()
    logger.info(f"Received bytes ==> {response_bytes.hex(':')}")
    response = proto.ResponseGeneric.FromString(response_bytes)
    logger.info(f"Received ==> {response}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perform some basic protobuf manipulation.")
    args = parser.parse_args()

    try:
        main()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)
    else:
        sys.exit(0)
