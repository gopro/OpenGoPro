"""Flow abstraction specifically for use with camera statuses that can be (un)registered for."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Callable, Coroutine, Generic, TypeVar

from open_gopro.communicator_interface import BaseGoProCommunicator
from open_gopro.exceptions import GoProError
from open_gopro.flow import Flow, FlowManager
from open_gopro.models.response import GoProResp
from open_gopro.types import UpdateType

T = TypeVar("T")
I = TypeVar("I")
C = TypeVar("C", bound="StatusFlowSeparateInitial")


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
        gopro: BaseGoProCommunicator,
        update: UpdateType,
        register_command: Coroutine[Any, Any, GoProResp[I]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        self._gopro = gopro
        self._flow_manager: FlowManager[T] = FlowManager(debug_id=str(update))
        self._update = update
        self._register_command = register_command
        self._unregister_command = unregister_command
        self._initial_response: I
        self._is_open = False
        super().__init__(manager=self._flow_manager, debug_id=str(update))

    @property
    def initial_response(self) -> I:
        """Initial status response received from the register command.

        Returns:
            I: Initial status
        """
        return self._initial_response

    async def __aenter__(self) -> StatusFlowSeparateInitial[I, T]:
        if not self._is_open:
            await self.start()
        return self

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        if self._is_open:
            await self.stop()

    async def _emit_status(self, _: UpdateType, value: T) -> None:
        """Emit a newly status for flow collection

        Args:
            value (T): Value of received status.
        """
        await self._flow_manager.emit(value)

    async def start(self: C) -> C:
        """Configure the camera to start receiving statuses.

        Raises:
            GoProNotOpened: Can't start because there is no BLE connection
            GoProError: Register command returned a failure status

        Returns:
            C: modified status flow
        """
        self._gopro.register_update(self._emit_status, self._update)
        initial_response = await self._register_command
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving status ==> {self._update}")
        self._initial_response = initial_response.data
        self._is_open = True
        return self

    def on_start(self: C, action: Callable[[T], None]) -> C:
        """Register a callback to be called when the first status is collected.

        Args:
            action (Callable[[T], None]): action to be called on start

        Returns:
            C: modified status flow
        """
        super().on_start(action)
        return self

    async def stop(self) -> None:
        """Configure the camera to stop sending statuses"""
        self._gopro.unregister_update(self._emit_status, self._update)
        if self._unregister_command:
            await self._unregister_command
        self._is_open = False


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
        gopro: BaseGoProCommunicator,
        update: UpdateType,
        register_command: Coroutine[Any, Any, GoProResp[T]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        super().__init__(gopro, update, register_command, unregister_command)

    async def start(self: C) -> C:
        """Configure the camera to start receiving statuses.

        The initial response will be treated and emitted the same as subsequent responses.

        Raises:
            GoProNotOpened: Can't start because there is no BLE connection
            GoProError: Register command returned a failure status

        Returns:
            C: modified status flow
        """
        self._gopro.register_update(self._emit_status, self._update)
        initial_response = await self._register_command
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving status ==> {self._update}")
        await self._emit_status(self._update, initial_response.data)
        self._is_open = True
        return self
