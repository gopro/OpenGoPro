from __future__ import annotations

import logging

from returns.result import ResultE

from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.gopro_base import GoProBase
from open_gopro.models.streaming import PreviewStreamOptions

logger = logging.getLogger(__name__)


class PreviewStreamController(StreamController[PreviewStreamOptions]):
    def __init__(self, gopro: GoProBase) -> None:
        super().__init__(gopro)
        self._status = StreamController.StreamStatus.NOT_READY

    @property
    def is_available(self) -> bool:  # noqa: D102
        raise NotImplementedError

    async def start(self, options: PreviewStreamOptions) -> ResultE[None]:  # noqa: D102
        raise NotImplementedError

    async def stop(self) -> ResultE[None]:  # noqa: D102
        raise NotImplementedError

    @property
    def status(self) -> StreamController.StreamStatus:  # noqa: D102
        return self._status

    @property
    def stream_type(self) -> StreamType:  # noqa: D102
        return StreamType.PREVIEW

    @property
    def url(self) -> str:  # noqa: D102
        raise NotImplementedError
