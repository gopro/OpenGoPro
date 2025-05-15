# webcam_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu May 15 16:57:27 UTC 2025

"""Webcam stream controller implementation."""

from __future__ import annotations

import asyncio
import logging

from returns.result import ResultE

from open_gopro.domain.exceptions import GoProError
from open_gopro.domain.observable import Observable
from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants import Toggle
from open_gopro.models.streaming import (
    WebcamError,
    WebcamProtocol,
    WebcamStatus,
    WebcamStreamOptions,
)

logger = logging.getLogger(__name__)


class WebcamStreamController(StreamController[WebcamStreamOptions]):
    """Livestream stream controller

    Args:
        gopro (GoProBase): GoPro device to operate on
    """

    def __init__(self, gopro: GoProBase) -> None:
        super().__init__(gopro)
        self.status_observable = Observable[StreamController.StreamStatus](
            debug_id="webcam stream controller status tracker"
        )
        self.current_options: WebcamStreamOptions | None = None
        self._status_task: asyncio.Task | None = None

    async def _track_status(self) -> None:
        """Track the webcam, converting it to a stream status observable"""
        # Poll until status is received
        # TODO cleanup?
        while True:
            response = (await self.gopro.http_command.webcam_status()).data
            if response.error != WebcamError.SUCCESS:
                # Something bad happened
                logger.error(f"Received webcam error: {response.error}")
                return  # TODO throw instead?
            logger.debug(f"Webcam stream controller received status: {response.status}")
            match response.status:
                case WebcamStatus.OFF:
                    await self.status_observable.emit(StreamController.StreamStatus.STOPPED)
                case WebcamStatus.IDLE:
                    await self.status_observable.emit(StreamController.StreamStatus.STOPPED)
                case WebcamStatus.HIGH_POWER_PREVIEW:
                    await self.status_observable.emit(StreamController.StreamStatus.STARTED)
                case WebcamStatus.LOW_POWER_PREVIEW:
                    await self.status_observable.emit(StreamController.StreamStatus.STARTED)
            await asyncio.sleep(1)

    @property
    def is_available(self) -> bool:  # noqa: D102
        return self.gopro.is_http_connected

    async def start(self, options: WebcamStreamOptions) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Webcam is not available")
            return ResultE.from_failure(GoProError("Webcam is not available"))
        if self.status in (StreamController.StreamStatus.STARTED, StreamController.StreamStatus.STARTING):
            logger.warning("Webcam is already started / starting")
            return ResultE.from_failure(GoProError("Webcam is already started / starting"))

        self._status_task = asyncio.create_task(self._track_status())
        self.current_options = options
        await self.status_observable.emit(StreamController.StreamStatus.STARTING)

        await self.gopro.http_command.set_shutter(shutter=Toggle.DISABLE)
        if (await self.gopro.http_command.webcam_status()).data.status not in {
            WebcamStatus.OFF,
            WebcamStatus.IDLE,
        }:
            logger.warning("Webcam is currently on. Turning if off.")
            assert (await self.gopro.http_command.webcam_stop()).ok
            await self.status_observable.observe().first(lambda s: s == StreamController.StreamStatus.STOPPED)

        logger.info("Starting webcam...")
        if (
            status := (await self.gopro.http_command.webcam_start(protocol=self.current_options.protocol)).data.error
        ) != WebcamError.SUCCESS:
            logger.error(f"Couldn't start webcam: {status}")
            self._cleanup()
            return ResultE.from_failure(GoProError(f"Couldn't start webcam: {status}"))
        await self.status_observable.observe().first(lambda s: s == StreamController.StreamStatus.STARTED)
        return ResultE.from_value(None)

    async def stop(self) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Webcam is not available")
            return ResultE.from_failure(GoProError("Webcam is not available"))
        if self.status == StreamController.StreamStatus.STOPPED:
            logger.warning("Webcam is already stopped")
            return ResultE.from_failure(GoProError("Webcam is already stopped"))

        await self.status_observable.emit(StreamController.StreamStatus.STOPPING)
        logger.info("Stopping webcam...")
        # First wait for it top stop
        assert (await self.gopro.http_command.webcam_stop()).ok
        await self.status_observable.observe().first(lambda s: s == StreamController.StreamStatus.STOPPED)
        # Now just tell it to exit
        await self.gopro.http_command.webcam_exit()
        self._cleanup()
        return ResultE.from_value(None)

    def _cleanup(self) -> None:
        """Cleanup after a stream has stopped or failed to start."""
        if self._status_task:
            self._status_task.cancel()
            self._status_task = None
        self.current_options = None

    @property
    def status(self) -> StreamController.StreamStatus:  # noqa: D102
        return self.status_observable.current or StreamController.StreamStatus.STOPPED

    @property
    def stream_type(self) -> StreamType:  # noqa: D102
        return StreamType.WEBCAM

    @property
    def url(self) -> str:  # noqa: D102
        assert self.current_options is not None, "Stream options not set"
        match self.current_options.protocol:
            case WebcamProtocol.RTSP:
                return f"rtsp://{self.gopro.ip_address}:554/live"
            case WebcamProtocol.TS | None:
                return r"udp://0.0.0.0:8554"

    async def close(self) -> ResultE[None]:  # noqa: D102
        if self._status_task:
            self._status_task.cancel()
        return ResultE.from_value(None)
