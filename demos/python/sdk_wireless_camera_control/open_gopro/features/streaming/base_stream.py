# base_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu May 15 16:57:27 UTC 2025

"""Base class for all stream controllers."""

from __future__ import annotations

import enum
import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from returns.result import ResultE

from open_gopro.gopro_base import GoProBase
from open_gopro.models.streaming import StreamType

logger = logging.getLogger(__name__)

T = TypeVar("T")


class StreamController(ABC, Generic[T]):
    """Interface for stream controllers."""

    class StreamStatus(enum.Enum):
        """Enum for the different types of stream status."""

        STARTING = enum.auto()
        STARTED = enum.auto()
        STOPPING = enum.auto()
        STOPPED = enum.auto()

    def __init__(self, gopro: GoProBase) -> None:
        self.gopro = gopro

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the stream is available.

        Returns:
            bool: True if the stream is available, False otherwise.
        """

    @property
    @abstractmethod
    def stream_type(self) -> StreamType:
        """Get the type of the stream.

        Returns:
            StreamType: The type of the stream.
        """

    @property
    @abstractmethod
    def url(self) -> str:
        """Get the URL that can be used to view the stream

        Returns:
            str: The URL of the stream.
        """

    @property
    @abstractmethod
    def status(self) -> StreamStatus:
        """Get the current status of the stream.

        Returns:
            StreamStatus: The current status of the stream.
        """

    @abstractmethod
    async def start(self, options: T) -> ResultE[None]:
        """Start the stream.

        Args:
            options (T): The options to use for the stream.

        Returns:
            ResultE[None]: Result container with failure if it exists.
        """

    @abstractmethod
    async def stop(self) -> ResultE[None]:
        """Stop the stream."""

    @abstractmethod
    async def close(self) -> ResultE[None]:
        """Close the stream controller, gracefully cancelling tasks and releasing resources.

        Returns:
            ResultE[None]: Result container with failure if it exists.
        """
