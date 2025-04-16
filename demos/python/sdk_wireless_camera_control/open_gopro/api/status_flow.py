from __future__ import annotations

from types import TracebackType
from typing import Any, Callable, Coroutine, TypeVar

from open_gopro.api.api import WirelessApi
from open_gopro.flow import Flow, FlowManager
from open_gopro.gopro_base import GoProBase
from open_gopro.models.response import GoProResp
from open_gopro.types import UpdateType

T = TypeVar("T")
I = TypeVar("I")


class StatusFlowSeparateInitial[I, T](Flow[T]):
    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        update: UpdateType,
        register_command: Coroutine[Any, Any, GoProResp[I]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        self._gopro = gopro
        self._flow_manager: FlowManager[T] = FlowManager()
        self._update = update
        self._register_command = register_command
        self._unregister_command = unregister_command
        self._initial_response: I
        super().__init__(self._flow_manager)

    @property
    def initial_response(self) -> I:
        return self._initial_response

    async def __aenter__(self) -> StatusFlowSeparateInitial[I, T]:
        return await self.start()

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        await self.stop()

    async def _emit_status(self, _: UpdateType, value: T) -> None:
        await self._flow_manager.emit(value)

    async def start(self) -> StatusFlowSeparateInitial[I, T]:
        if not self._gopro.is_ble_connected:
            raise RuntimeError("Can not track status if BLE is not connected.")
        self._gopro.register_update(self._emit_status, self._update)
        initial_response = await self._register_command
        assert initial_response.ok
        self._initial_response = initial_response.data
        return self

    def on_start(self, action: Callable[[T], None]) -> StatusFlowSeparateInitial[I, T]:
        super().on_start(action)
        return self

    async def stop(self) -> None:
        self._gopro.unregister_update(self._emit_status, self._update)
        if self._unregister_command:
            await self._unregister_command


class StatusFlow[T](StatusFlowSeparateInitial[T, T]):
    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        update: UpdateType,
        register_command: Coroutine[Any, Any, GoProResp[T]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        super().__init__(gopro, update, register_command, unregister_command)
