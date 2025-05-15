# base_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Functionality common to all features."""

import asyncio
from abc import ABC, abstractmethod

from open_gopro.api.api import WirelessApi
from open_gopro.gopro_base import GoProBase


class BaseFeature(ABC):
    """Base Feature definition / interface

    Args:
        gopro (GoProBase[WirelessApi]): camera to operate on
        loop (asyncio.AbstractEventLoop): asyncio loop to use for this feature
    """

    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self._gopro = gopro
        self._loop = loop

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        """Is the feature ready to use?

        No other methods (besides wait_for_ready) should be used until the feature is ready

        Returns:
            bool: True if ready, False otherwise
        """

    @abstractmethod
    async def wait_for_ready(self) -> None:
        """Wait until the feature is ready to use"""

    @abstractmethod
    async def close(self) -> None:
        """Close the feature for use."""
