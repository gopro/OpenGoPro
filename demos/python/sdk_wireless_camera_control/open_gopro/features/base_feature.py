import asyncio
from abc import ABC, abstractmethod

from open_gopro.api.api import WirelessApi
from open_gopro.gopro_base import GoProBase


class BaseFeature(ABC):
    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self._gopro = gopro
        self._loop = loop

    @property
    @abstractmethod
    def is_ready(self) -> bool: ...

    @abstractmethod
    async def wait_for_ready(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
