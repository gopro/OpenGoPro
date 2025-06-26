# stream_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu May 15 16:57:27 UTC 2025

"""Combined stream functionality for all type of video streams."""

from __future__ import annotations

import logging

from returns.result import Failure, ResultE, Success

from open_gopro.domain.exceptions import GoProError
from open_gopro.features.base_feature import BaseFeature
from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.features.streaming.livestream import (
    LiveStreamController,
    LivestreamOptions,
)
from open_gopro.features.streaming.preview_stream import (
    PreviewStreamController,
    PreviewStreamOptions,
)
from open_gopro.features.streaming.webcam_stream import (
    WebcamStreamController,
    WebcamStreamOptions,
)
from open_gopro.models.types import StreamOptions

logger = logging.getLogger(__name__)


class StreamFeature(BaseFeature):
    """Abstracted stream functionality for all type of video streams.

    There can only ever be one stream open at a time.
    """

    def __init__(self) -> None:
        super().__init__()
        self._current: StreamController | None = None

    @property
    def is_supported(self) -> bool:  # noqa: D102
        # Streaming is always supported
        return True

    @property
    def current_stream(self) -> StreamType | None:
        """Get the current stream type.

        Returns:
            StreamType | None: stream type if a stream is active, None otherwise.
        """
        return self._current.stream_type if self._current else None

    @property
    def is_streaming(self) -> bool:
        """Check if a stream is currently active.

        Returns:
            bool: True if a stream is active, False otherwise.
        """
        return self._current is not None and self._current.status == StreamController.StreamStatus.STARTED

    @property
    def url(self) -> str | None:
        """Get the URL of the current stream.

        Returns:
            str | None: The URL of the current stream, or None if no stream is active.
        """
        return self._current.url if self._current else None

    async def start_stream(
        self,
        stream_type: StreamType,
        options: StreamOptions,
    ) -> ResultE[None]:
        """Start a stream of the specified type.

        Args:
            stream_type (StreamType): stream type to start
            options (StreamOptions): stream-specific options

        Returns:
            ResultE[None]: Result of the operation including failure reason if any.
        """
        if self.is_streaming:
            return ResultE.from_failure(GoProError(f"Stream {self.current_stream} is already active"))

        controller: StreamController
        match stream_type:
            case StreamType.WEBCAM:
                controller = WebcamStreamController(self._gopro)
            case StreamType.LIVE:
                controller = LiveStreamController(self._gopro)
            case StreamType.PREVIEW:
                controller = PreviewStreamController(self._gopro)

        if not controller.is_available:
            return ResultE.from_failure(GoProError(f"{stream_type} is not available"))

        match stream_type:
            case StreamType.WEBCAM:
                if not isinstance(options, WebcamStreamOptions):
                    return ResultE.from_failure(GoProError("Invalid options for webcam stream"))
            case StreamType.LIVE:
                if not isinstance(options, LivestreamOptions):
                    return ResultE.from_failure(GoProError("Invalid options for livestream"))
            case StreamType.PREVIEW:
                if not isinstance(options, PreviewStreamOptions):
                    return ResultE.from_failure(GoProError("Invalid options for preview stream"))

        self._current = controller
        logger.info(f"Starting {stream_type.name.title()} stream")
        match (result := await self._current.start(options)):
            case Success():
                logger.info("Stream started successfully.")
            case Failure():
                logger.error(f"Stream failed to start: {result.failure()}")
        return result

    async def stop_active_stream(self) -> ResultE[None]:
        """Stop the currently active stream.

        Returns:
            ResultE[None]: Result of the operation.
        """
        if self.is_streaming:
            assert self._current
            await self._current.stop()

        return ResultE.from_value(None)

    async def close(self) -> None:  # noqa: D102
        await self.stop_active_stream()
