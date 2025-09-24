# test_get_all_media_metadata.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 24 20:06:46 UTC 2025

import logging
from pathlib import Path
from typing import AsyncGenerator

import pytest

from open_gopro import WiredGoPro
from open_gopro.util.logger import set_logging_level, setup_logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
async def gopro() -> AsyncGenerator[WiredGoPro, None]:
    async with WiredGoPro() as gopro:
        yield gopro


async def test_get_metadata_for_all_existing_media(gopro: WiredGoPro) -> None:
    response = await gopro.http_command.get_media_list()
    assert response.ok

    for media in response.data.files:
        assert (await gopro.http_command.get_media_metadata(path=media.filename)).ok
