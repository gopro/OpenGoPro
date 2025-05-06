"""Flow abstraction specifically for use with camera statuses that can be (un)registered for."""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, Coroutine, Generic, TypeVar

from open_gopro.domain.communicator_interface import BaseGoProCommunicator
from open_gopro.domain.exceptions import GoProError
from open_gopro.domain.flow import Flow
from open_gopro.domain.types import UpdateType
from open_gopro.models.response import GoProResp

T = TypeVar("T")
I = TypeVar("I")
C = TypeVar("C", bound="GoproFlowDistinctInitial")

logger = logging.getLogger(__name__)


class GoproFlowDistinctInitial(Flow[T], Generic[I, T]):
    """Status Flow for asynchronous camera statuses where the initial status is a different type than proceeding status notifications.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType): the status's update type
        register_command (Coroutine[Any, Any, GoProResp[I]]): command to call to start receiving statuses
        unregister_command (Coroutine[Any, Any, Any] | None): Command to call to stop receiving statuses. Defaults to None.
    """

    def __init__(
        self,
        gopro: BaseGoProCommunicator,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        register_command: Coroutine[Any, Any, GoProResp[I]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        self._gopro = gopro
        self._update = update
        self._register_command = register_command
        self._unregister_command = unregister_command
        self._initial_response: I
        self._is_open = False
        super().__init__(debug_id=str(update))

    @property
    def initial_response(self) -> I:
        """Initial status response received from the register command.

        Returns:
            I: Initial status
        """
        return self._initial_response

    async def __aenter__(self) -> GoproFlowDistinctInitial[I, T]:
        if not self._is_open:
            await self.start()
        return self

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        if self._is_open:
            await self.stop()

    async def _emit_flow_element(self, _: UpdateType | BaseGoProCommunicator._CompositeRegisterType, value: T) -> None:
        """Emit a newly received value for flow collection

        Args:
            value (T): Value of received status.
        """
        await self.emit(value)

    async def start(self: C) -> C:
        """Configure the camera to start receiving statuses.

        Raises:
            GoProError: Register command returned a failure status

        Returns:
            C: modified status flow
        """
        self._gopro._register_update(self._emit_flow_element, self._update)
        initial_response = await self._register_command
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving status ==> {self._update}")
        self._initial_response = initial_response.data
        self._is_open = True
        return self

    async def stop(self) -> None:
        """Configure the camera to stop sending statuses"""
        self._gopro._unregister_update(self._emit_flow_element, self._update)
        if self._unregister_command:
            await self._unregister_command
        self._is_open = False


class GoproFlow(GoproFlowDistinctInitial[T, T]):
    """Status Flow for asynchronous camera statuses where all received statuses are the same type.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType): the status's update type
        register_command (Coroutine[Any, Any, GoProResp[T]]): command to call to start receiving statuses
        unregister_command (Coroutine[Any, Any, Any] | None): Command to call to stop receiving statuses. Defaults to None.
    """

    def __init__(
        self,
        gopro: BaseGoProCommunicator,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        register_command: Coroutine[Any, Any, GoProResp[T]],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        super().__init__(gopro, update, register_command, unregister_command)

    async def start(self: C) -> C:
        """Configure the camera to start receiving statuses.

        The initial response will be treated and emitted the same as subsequent responses.

        Raises:
            GoProError: Register command returned a failure status

        Returns:
            C: modified status flow
        """
        self._gopro._register_update(self._emit_flow_element, self._update)
        initial_response = await self._register_command
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving status ==> {self._update}")
        self._initial_response = initial_response.data
        await self._emit_flow_element(self._update, initial_response.data)
        self._is_open = True
        return self


class GoproCompositeFlow(GoproFlow[dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T]]):
    """Status Flow for asynchronous camera statuses where all received statuses are the same type.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType): the status's update type
        register_command (Coroutine[Any, Any, GoProResp[T]]): command to call to start receiving statuses
        unregister_command (Coroutine[Any, Any, Any] | None): Command to call to stop receiving statuses. Defaults to None.
    """

    def __init__(
        self,
        gopro: BaseGoProCommunicator,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        register_command: Coroutine[
            Any, Any, GoProResp[dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T]]
        ],
        unregister_command: Coroutine[Any, Any, Any] | None = None,
    ) -> None:
        super().__init__(gopro, update, register_command, unregister_command)

    async def _emit_flow_element(
        self,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        value: T | dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T],
    ) -> None:
        """Emit a newly received value for flow collection

        Args:
            update: UpdateType | BaseGoProCommunicator._CompositeRegisterType: The update type.
            value: dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T]: The value.
        """
        # This is the initial response which comes as a dict of all values.
        if isinstance(update, BaseGoProCommunicator._CompositeRegisterType) and isinstance(value, dict):
            await self.emit(value)
        # Subsequent responses are just the individual value of the update.
        else:
            await self.emit({update: value})  # type: ignore
