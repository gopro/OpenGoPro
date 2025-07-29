from typing import AsyncGenerator
import logging
from pathlib import Path

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
