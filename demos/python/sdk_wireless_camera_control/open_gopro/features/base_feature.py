"""Functionality common to all features."""

import asyncio
from abc import ABC, abstractmethod

from open_gopro.api.api import WirelessApi
from open_gopro.domain.gopro_base import GoProBase


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
    def close(self) -> None:
        """Close the feature for use."""
