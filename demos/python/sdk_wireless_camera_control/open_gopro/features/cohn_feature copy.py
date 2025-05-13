# cohn_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Camera on the home network (COHN) feature abstraction."""

from __future__ import annotations

import asyncio
import logging

from returns.pipeline import is_successful
from returns.result import Result
from tinydb import TinyDB

from open_gopro.api import WirelessApi
from open_gopro.database.cohn_db import CohnDb
from open_gopro.domain.exceptions import GoProNotOpened
from open_gopro.domain.gopro_observable import GoProObservable
from open_gopro.features.base_feature import BaseFeature
from open_gopro.gopro_base import GoProBase
from open_gopro.models import proto
from open_gopro.models.constants import ActionId
from open_gopro.models.general import CohnInfo
from open_gopro.models.proto import EnumCOHNNetworkState, EnumCOHNStatus

logger = logging.getLogger(__name__)


class StreamFeature(BaseFeature):
    """Abstracted stream functionality for all type of video streams.

    There can only ever be one stream open at a time.
    """

    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        super().__init__(gopro, loop)

    @property
    def is_ready(self) -> bool:  # noqa: D102
        # Always ready. We'll track stream status when they are requested to be opened
        return True

    async def wait_for_ready(self, timeout: float = 60) -> None:  # noqa: D102
        return

    def close(self) -> None:  # noqa: D102
        # TODO
        ...
