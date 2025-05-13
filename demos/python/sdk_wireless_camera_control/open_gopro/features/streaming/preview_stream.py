from __future__ import annotations

import logging

from returns.result import ResultE

from open_gopro.domain.exceptions import GoProError
from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.gopro_base import GoProBase
from open_gopro.models.streaming import PreviewStreamOptions
from open_gopro.models.constants import Toggle

logger = logging.getLogger(__name__)


# TODO is there a status we can track?
class PreviewStreamController(StreamController[PreviewStreamOptions]):
    def __init__(self, gopro: GoProBase) -> None:
        super().__init__(gopro)
        self._status = StreamController.StreamStatus.STOPPED
        self._current_options: PreviewStreamOptions | None = None

    @property
    def is_available(self) -> bool:
        return True if self.gopro.is_http_connected else False

    async def start(self, options: PreviewStreamOptions) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Preview Stream is not available")
            return ResultE.from_failure(GoProError("Preview Stream is not available"))
        if self.status in (StreamController.StreamStatus.STARTED, StreamController.StreamStatus.STARTING):
            logger.warning("Preview Stream is already started / starting")
            return ResultE.from_failure(GoProError("Preview Stream is already started / starting"))

        self._current_options = options
        self._status = StreamController.StreamStatus.STARTING
        logger.info(f"Starting preview stream on port {self._current_options.port}")
        # Stop the preview stream if it is already running
        await self.gopro.http_command.set_preview_stream(mode=Toggle.DISABLE)
        await self.gopro.ble_command.set_shutter(shutter=Toggle.DISABLE)
        # Now start the preview stream
        response = await self.gopro.http_command.set_preview_stream(mode=Toggle.ENABLE, port=self._current_options.port)
        if response.ok:
            self._status = StreamController.StreamStatus.STARTED
            return ResultE.from_value(None)
        else:
            logger.error(f"Failed to start preview stream: {response.status}")
            self._status = StreamController.StreamStatus.STOPPED
            self._cleanup()
            return ResultE.from_failure(GoProError(f"Failed to start preview stream : {response.status}"))

    async def stop(self) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Preview Stream is not available")
            return ResultE.from_failure(GoProError("Preview Stream is not available"))
        if self.status == StreamController.StreamStatus.STOPPED:
            logger.warning("Preview Stream is already stopped")
            return ResultE.from_failure(GoProError("Preview Stream is already stopped"))

        self._status = StreamController.StreamStatus.STOPPING
        logger.info("Stopping preview stream")
        response = await self.gopro.http_command.set_preview_stream(mode=Toggle.DISABLE)
        self._cleanup()
        if response.ok:
            self._status = StreamController.StreamStatus.STOPPED
            return ResultE.from_value(None)
        else:
            logger.error(f"Failed to stop preview stream: {response.status}")
            return ResultE.from_failure(GoProError(f"Failed to stop preview stream : {response.status}"))

    def _cleanup(self) -> None:
        """Cleanup the stream controller.

        This is called when the stream is stopped or fails to start.
        """
        self._current_options = None

    @property
    def status(self) -> StreamController.StreamStatus:  # noqa: D102
        return self._status

    @property
    def stream_type(self) -> StreamType:  # noqa: D102
        return StreamType.PREVIEW

    @property
    def url(self) -> str:  # noqa: D102
        assert self._current_options is not None, "Preview stream options not set"
        return f"udp://127.0.0.1:{self._current_options.port}"
