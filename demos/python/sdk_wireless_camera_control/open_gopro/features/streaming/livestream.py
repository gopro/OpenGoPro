# livestream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu May 15 16:57:27 UTC 2025

"""Livestream stream controller implementation."""

from __future__ import annotations

import asyncio
import logging

from returns.result import ResultE

from open_gopro.domain.exceptions import GoProError
from open_gopro.domain.gopro_observable import GoProObservable
from open_gopro.domain.observable import Observable
from open_gopro.features.streaming.base_stream import StreamController, StreamType
from open_gopro.gopro_base import GoProBase
from open_gopro.models.constants import ActionId, Toggle
from open_gopro.models.constants.constants import FeatureId
from open_gopro.models.proto import (
    EnumLiveStreamStatus,
    EnumRegisterLiveStreamStatus,
    NotifyLiveStreamStatus,
)
from open_gopro.models.streaming import LivestreamOptions
from open_gopro.models.types import ProtobufId

logger = logging.getLogger(__name__)


class LiveStreamController(StreamController[LivestreamOptions]):
    """Livestream stream controller

    Args:
        gopro (GoProBase): GoPro device to operate on
    """

    def __init__(self, gopro: GoProBase) -> None:
        super().__init__(gopro)
        self.status_observable = Observable[StreamController.StreamStatus](
            debug_id="livestream controller status tracker"
        )
        self.current_options: LivestreamOptions | None = None
        self._status_task = asyncio.create_task(self._track_status())

    async def _track_status(self) -> None:
        """Track the status of the livestream status observable, converting it to a stream status observable."""
        async for status in (await self.get_livestream_status_observable()).observe(
            debug_id="Livestream Status Tracker"
        ):
            logger.debug(f"Livestream controller received status: {status}")
            match status.live_stream_status:
                case (
                    EnumLiveStreamStatus.LIVE_STREAM_STATE_IDLE
                    | EnumLiveStreamStatus.LIVE_STREAM_STATE_FAILED_STAY_ON
                    | EnumLiveStreamStatus.LIVE_STREAM_STATE_UNAVAILABLE
                ):
                    logger.debug(f"Livestream controller emitting state {StreamController.StreamStatus.STOPPED}")
                    await self.status_observable.emit(StreamController.StreamStatus.STOPPED)
                case EnumLiveStreamStatus.LIVE_STREAM_STATE_READY | EnumLiveStreamStatus.LIVE_STREAM_STATE_RECONNECTING:
                    logger.debug(f"Livestream controller emitting state {StreamController.StreamStatus.STARTING}")
                    await self.status_observable.emit(StreamController.StreamStatus.STARTING)
                case (
                    EnumLiveStreamStatus.LIVE_STREAM_STATE_STREAMING
                    | EnumLiveStreamStatus.LIVE_STREAM_STATE_COMPLETE_STAY_ON
                ):
                    logger.debug(f"Livestream controller emitting state {StreamController.StreamStatus.STARTED}")
                    await self.status_observable.emit(StreamController.StreamStatus.STARTED)
                case _:
                    logger.warning(f"Livestream controller received unknown status: {status}")

    async def get_livestream_status_observable(
        self,
    ) -> GoProObservable[NotifyLiveStreamStatus]:
        """Get an API-level observable for the livestream status protobuf operation.

        Returns:
            GoProObservable[NotifyLiveStreamStatus]: live stream status observable
        """
        return await GoProObservable[NotifyLiveStreamStatus](
            gopro=self.gopro,
            register_command=self.gopro.ble_command.register_livestream_status(
                register=[EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS]
            ),
            unregister_command=self.gopro.ble_command.register_livestream_status(
                unregister=[EnumRegisterLiveStreamStatus.REGISTER_LIVE_STREAM_STATUS_STATUS]
            ),
            update=ProtobufId(FeatureId.QUERY, ActionId.LIVESTREAM_STATUS_NOTIF),
        ).start()

    @property
    def is_available(self) -> bool:  # noqa: D102
        # TODO can we check if the camera is connected to an access point? We probably need to update the AP feature.
        return self.gopro.is_ble_connected

    async def start(self, options: LivestreamOptions) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Livestream is not available")
            return ResultE.from_failure(GoProError("Livestream is not available"))
        if self.status in (StreamController.StreamStatus.STARTED, StreamController.StreamStatus.STARTING):
            logger.warning("Livestream is already started / starting")
            return ResultE.from_failure(GoProError("Livestream is already started / starting"))

        logger.info("Starting livestream")
        self.current_options = options
        # Disable shutter before starting livestream
        # TODO error handling
        await self.gopro.ble_command.set_shutter(shutter=Toggle.DISABLE)
        assert (
            await self.gopro.ble_command.set_livestream_mode(
                url=self.current_options.url,
                window_size=self.current_options.resolution,
                minimum_bitrate=self.current_options.minimum_bitrate,
                maximum_bitrate=self.current_options.maximum_bitrate,
                starting_bitrate=self.current_options.starting_bitrate,
                encode=self.current_options.encode,
                lens=self.current_options.fov,
            )
        ).ok
        logger.info("Waiting for livestream to begin starting...")
        await self.status_observable.observe(debug_id="Livestream Controller Wait For Ready").first(
            lambda s: s == StreamController.StreamStatus.STARTING
        )
        await asyncio.sleep(2)  # TODO Is this still needed?
        logger.info("Setting shutter to start livestream")
        await self.gopro.ble_command.set_shutter(shutter=Toggle.ENABLE)
        return ResultE.from_value(None)

    async def stop(self) -> ResultE[None]:  # noqa: D102
        if not self.is_available:
            logger.error("Livestream is not available")
            return ResultE.from_failure(GoProError("Livestream is not available"))
        if self.status == StreamController.StreamStatus.STOPPED:
            logger.warning("Livestream is already stopped")
            return ResultE.from_failure(GoProError("Livestream is already stopped"))

        logger.info("Stopping livestream")
        # TODO error handling
        await self.gopro.ble_command.set_shutter(shutter=Toggle.DISABLE)
        return ResultE.from_value(None)

    @property
    def status(self) -> StreamController.StreamStatus:  # noqa: D102
        return self.status_observable.current or StreamController.StreamStatus.STOPPED

    @property
    def stream_type(self) -> StreamType:  # noqa: D102
        return StreamType.LIVE

    @property
    def url(self) -> str:  # noqa: D102
        if self.current_options is None:
            raise GoProError("Livestream is not started")
        return self.current_options.url

    def _cleanup(self) -> None:
        """Cleanup after a stream has stopped or failed to start."""
        self.current_options = None

    async def close(self) -> ResultE[None]:  # noqa: D102
        self._status_task.cancel()
        return ResultE.from_value(None)
