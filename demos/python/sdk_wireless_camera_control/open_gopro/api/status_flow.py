"""Flow abstraction specifically for use with camera statuses that can be (un)registered for."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Callable, Coroutine, Generic, TypeVar

from open_gopro.api.api import WirelessApi
from open_gopro.exceptions import GoProError, GoProNotOpened
from open_gopro.flow import Flow, FlowManager
from open_gopro.gopro_base import GoProBase
from open_gopro.models.response import GoProResp
from open_gopro.types import UpdateType

T = TypeVar("T")
I = TypeVar("I")


class StatusFlowSeparateInitial(Flow[T], Generic[I, T]):
    """Status Flow for asynchronous camera statuses where the initial status is a different type than proceeding status notifications.

    Args:
        gopro (GoProBase[WirelessApi]): gopro camera to operate on
        update (UpdateType): the status's update type
        register_command (Coroutine[Any, Any, GoProResp[I]]): command to call to start receiving statuses
        unregister_command (Coroutine[Any, Any, Any] | None): Command to call to stop receiving statuses. Defaults to None.
    """

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
        """Initial status response received from the register command.

        Returns:
            I: Initial status
        """
        return self._initial_response

    async def __aenter__(self) -> StatusFlowSeparateInitial[I, T]:
        return await self.start()

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        await self.stop()

    async def _emit_status(self, _: UpdateType, value: T) -> None:
        """Emit a newly status for flow collection

        Args:
            value (T): Value of received status.
        """
        await self._flow_manager.emit(value)

    async def start(self) -> StatusFlowSeparateInitial[I, T]:
        """Configure the camera to start receiving statuses.

        Raises:
            GoProNotOpened: Can't start because there is no BLE connection
            GoProError: Register command returned a failure status

        Returns:
            StatusFlowSeparateInitial[I, T]: modified status flow
        """
        if not self._gopro.is_ble_connected:
            raise GoProNotOpened("Can not track status if BLE is not connected.")
        self._gopro.register_update(self._emit_status, self._update)
        initial_response = await self._register_command
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving status ==> {self._update}")
        self._initial_response = initial_response.data
        return self

    def on_start(self, action: Callable[[T], None]) -> StatusFlowSeparateInitial[I, T]:
        """Register a callback to be called when the first status is collected.

        Args:
            action (Callable[[T], None]): action to be called on start

        Returns:
            StatusFlowSeparateInitial[I, T]: modified status flow
        """
        super().on_start(action)
        return self

    async def stop(self) -> None:
        """Configure the camera to stop sending statuses"""
        self._gopro.unregister_update(self._emit_status, self._update)
        if self._unregister_command:
            await self._unregister_command


class StatusFlow(StatusFlowSeparateInitial[T, T], Generic[T]):
    """Status Flow for asynchronous camera statuses where all received statuses are the same type.

    Args:
        gopro (GoProBase[WirelessApi]): gopro camera to operate on
        update (UpdateType): the status's update type
        register_command (Coroutine[Any, Any, GoProResp[T]]): command to call to start receiving statuses
        unregister_command (Coroutine[Any, Any, Any] | None): Command to call to stop receiving statuses. Defaults to None.
    """

    def __init__(
        self,
        gopro: GoProBase[WirelessApi],
        update: UpdateType,
        register_command: Coroutine[Any, Any, GoProResp[T]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        super().__init__(gopro, update, register_command, unregister_command)
