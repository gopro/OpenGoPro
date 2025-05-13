from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from returns.result import ResultE

from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.domain.exceptions import GoProError
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants import Toggle
from open_gopro.models.streaming import (
    WebcamError,
    WebcamFOV,
    WebcamProtocol,
    WebcamResolution,
    WebcamStatus,
    WebcamStreamOptions,
)

logger = logging.getLogger(__name__)


class WebcamStreamController(StreamController[WebcamStreamOptions]):
    def __init__(self, gopro: GoProBase) -> None:
        super().__init__(gopro)
        self._status = StreamController.StreamStatus.NOT_READY
        self.current_options: WebcamStreamOptions | None = None

    def is_available(self) -> bool:
        return True if self.gopro.is_http_connected else False

    # TODO check if webcam is available, or if already started
    async def start(self, options: WebcamStreamOptions) -> ResultE[None]:
        self.current_options = options
        self._status = StreamController.StreamStatus.STARTING
        await self.gopro.http_command.wired_usb_control(control=Toggle.DISABLE)

        await self.gopro.http_command.set_shutter(shutter=Toggle.DISABLE)
        if (await self.gopro.http_command.webcam_status()).data.status not in {
            WebcamStatus.OFF,
            WebcamStatus.IDLE,
        }:
            logger.warning("Webcam is currently on. Turning if off.")
            assert (await self.gopro.http_command.webcam_stop()).ok
            await self._wait_for_webcam_status({WebcamStatus.OFF})

        logger.info("Starting webcam...")
        if (
            status := (await self.gopro.http_command.webcam_start(protocol=self.current_options.protocol)).data.error
        ) != WebcamError.SUCCESS:
            logger.error(f"Couldn't start webcam: {status}")
            return ResultE.from_failure(GoProError(f"Couldn't start webcam: {status}"))
        await self._wait_for_webcam_status({WebcamStatus.HIGH_POWER_PREVIEW})
        self._status = StreamController.StreamStatus.STARTED
        return ResultE.from_value(None)

    # TODO check if webcam is available, or if already stopped
    async def stop(self) -> ResultE[None]:
        self._status = StreamController.StreamStatus.STOPPING
        logger.info("Stopping webcam...")
        assert (await self.gopro.http_command.webcam_stop()).ok
        await self._wait_for_webcam_status({WebcamStatus.OFF, WebcamStatus.IDLE})
        assert (await self.gopro.http_command.webcam_exit()).ok
        await self._wait_for_webcam_status({WebcamStatus.OFF})
        self._status = StreamController.StreamStatus.STOPPED
        self.current_options = None
        return ResultE.from_value(None)

    @property
    def status(self) -> StreamController.StreamStatus:
        return self._status

    @status.setter
    def status(self, value: StreamController.StreamStatus) -> None:
        if value in (StreamController.StreamStatus.STOPPED, StreamController.StreamStatus.NOT_READY):
            if self.is_available():
                self._status = StreamController.StreamStatus.READY
        else:
            self._status = value

    @property
    def stream_type(self) -> StreamType:
        return StreamType.WEBCAM

    async def _wait_for_webcam_status(self, statuses: set[WebcamStatus], timeout: int = 10) -> bool:
        """Wait for specified webcam status(es) for a given timeout

        Args:
            statuses (set[WebcamStatus]): statuses to wait for
            timeout (int): timeout in seconds. Defaults to 10.

        Returns:
            bool: True if status was received before timing out, False if timed out or received error
        """

        async def poll_for_status() -> bool:
            # Poll until status is received
            while True:
                response = (await self.gopro.http_command.webcam_status()).data
                if response.error != WebcamError.SUCCESS:
                    # Something bad happened
                    logger.error(f"Received webcam error: {response.error}")
                    return False
                if response.status in statuses:
                    # We found the desired status
                    return True

        # Wait for either status or timeout
        try:
            return await asyncio.wait_for(poll_for_status(), timeout)
        except TimeoutError:
            return False

    @property
    def url(self) -> str:
        assert self.current_options is not None, "Stream options not set"
        match self.current_options.protocol:
            case WebcamProtocol.RTSP:
                return f"rtsp://{self.gopro.ip_address}:554/live"
            case WebcamProtocol.TS | None:
                return r"udp://0.0.0.0:8554"
