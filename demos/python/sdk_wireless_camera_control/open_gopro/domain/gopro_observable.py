# gopro_observable.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Observable abstraction specifically for use with API components that can be (un)registered for."""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, Callable, Coroutine, Generic, Self, TypeVar

from open_gopro.domain.communicator_interface import BaseGoProCommunicator
from open_gopro.domain.exceptions import GoProError
from open_gopro.domain.observable import Observable
from open_gopro.models.response import GoProResp
from open_gopro.models.types import UpdateType

T = TypeVar("T")
I = TypeVar("I")

logger = logging.getLogger(__name__)

# Type alias for command factories - callables that return fresh coroutines
CommandFactory = Callable[[], Coroutine[Any, Any, GoProResp[Any]]]


class GoproObserverDistinctInitial(Observable[T], Generic[I, T]):
    """Observable for asynchronous notifications where the initial notifications is a different type than proceeding notifications.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType | BaseGoProCommunicator._CompositeRegisterType): the observable's update type
        register_command (CommandFactory): factory that creates coroutine to start receiving values.
            Must be a callable (e.g., lambda) that returns a fresh coroutine each time, NOT a raw coroutine.
        unregister_command (CommandFactory | None): factory that creates coroutine to stop receiving values. Defaults to None.
    """

    def __init__(
        self,
        gopro: BaseGoProCommunicator,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        register_command: CommandFactory,
        unregister_command: CommandFactory | None = None,
    ) -> None:
        self._gopro = gopro
        self._update = update
        self._register_command_factory = register_command
        self._unregister_command_factory = unregister_command
        self._initial_response: I
        self._is_open = False
        super().__init__(debug_id=str(update))

    @property
    def initial_response(self) -> I:
        """Initial update received from the register command.

        Returns:
            I: Initial update
        """
        return self._initial_response

    async def __aenter__(self) -> GoproObserverDistinctInitial[I, T]:
        if not self._is_open:
            await self.start()
        return self

    async def __aexit__(self, exc_type: BaseException, exc_val: Any, exc_tb: TracebackType) -> None:
        if self._is_open:
            await self.stop()

    async def _emit_value(self, _: UpdateType | BaseGoProCommunicator._CompositeRegisterType, value: T) -> None:
        """Emit a newly received value for observing

        Args:
            value (T): Value of received element.
        """
        await self.emit(value)

    async def start(self: Self) -> Self:
        """Configure the camera to start receiving notifications.

        Raises:
            GoProError: Register command returned a failure update

        Returns:
            Self: modified observable
        """
        self._gopro._register_update(self._emit_value, self._update)
        initial_response = await self._register_command_factory()
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving update ==> {self._update}")
        self._initial_response = initial_response.data
        self._is_open = True
        return self

    async def stop(self) -> None:
        """Configure the camera to stop sending notifications"""
        self._gopro._unregister_update(self._emit_value, self._update)
        if self._unregister_command_factory:
            await self._unregister_command_factory()
        self._is_open = False


class GoProObservable(GoproObserverDistinctInitial[T, T]):
    """Observable for asynchronous camera API notifications where all received notifications are the same type.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType | BaseGoProCommunicator._CompositeRegisterType): the update's update type
        register_command (CommandFactory): factory that creates coroutine to start receiving notifications.
            Must be a callable (e.g., lambda) that returns a fresh coroutine each time, NOT a raw coroutine.
        unregister_command (CommandFactory | None): factory that creates coroutine to stop receiving notifications. Defaults to None.
    """

    async def start(self: Self) -> Self:
        """Configure the camera to start receiving notifications.

        The initial response will be treated and emitted the same as subsequent responses.

        Raises:
            GoProError: Register command returned a failure updates

        Returns:
            Self: modified observable
        """
        self._gopro._register_update(self._emit_value, self._update)
        initial_response = await self._register_command_factory()
        if not initial_response.ok:
            raise GoProError(f"Failed to start receiving updates ==> {self._update}")
        self._initial_response = initial_response.data
        await self._emit_value(self._update, initial_response.data)
        self._is_open = True
        return self


class GoProCompositeObservable(GoProObservable[dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T]]):
    """Observable for asynchronous camera notifications where all received notifications are the same type.

    Args:
        gopro (BaseGoProCommunicator): gopro camera to operate on
        update (UpdateType | BaseGoProCommunicator._CompositeRegisterType): the updates's update type
        register_command (CommandFactory): factory that creates coroutine to start receiving notifications.
            Must be a callable (e.g., lambda) that returns a fresh coroutine each time, NOT a raw coroutine.
        unregister_command (CommandFactory | None): factory that creates coroutine to stop receiving notifications. Defaults to None.
    """

    async def _emit_value(
        self,
        update: UpdateType | BaseGoProCommunicator._CompositeRegisterType,
        value: T | dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T],
    ) -> None:
        """Emit a newly received value for observation

        Args:
            update (UpdateType | BaseGoProCommunicator._CompositeRegisterType): The update type.
            value (T | dict[UpdateType | BaseGoProCommunicator._CompositeRegisterType, T]): The value.
        """
        # This is the initial response which comes as a dict of all values.
        if isinstance(update, BaseGoProCommunicator._CompositeRegisterType) and isinstance(value, dict):
            await self.emit(value)
        # Subsequent responses are just the individual value of the update.
        else:
            await self.emit({update: value})  # type: ignore
