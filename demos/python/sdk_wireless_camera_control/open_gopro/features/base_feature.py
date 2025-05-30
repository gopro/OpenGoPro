# base_feature.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon May 12 23:03:50 UTC 2025

"""Functionality common to all features."""
from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Callable

import wrapt

from open_gopro.gopro_base import GoProBase


@wrapt.decorator
def require_supported(wrapped: Callable, instance: BaseFeature, args: Any, kwargs: Any) -> Any:
    """Ensure the feature is supported before allowing access.

    Args:
        wrapped (Callable): The wrapped function or property
        instance (BaseFeature): The class instance (or None if accessing a property getter)
        args (Any): Positional arguments
        kwargs (Any): Keyword arguments

    Returns:
        Any: Result of the wrapped function

    Raises:
        RuntimeError: If feature is not supported
    """
    # Handle the case where instance might be None (property access)
    # In this case, the instance is actually the first argument in args
    actual_instance = instance if instance is not None else args[0]

    if not actual_instance.is_supported:
        raise RuntimeError(f"{actual_instance.__class__.__name__} feature is not supported on this camera")

    if instance is None:
        # Property getter case - call it with the rest of args (skipping the first one which is the instance)
        if len(args) > 1:
            return wrapped(args[0], *args[1:], **kwargs)
        return wrapped(args[0])

    # Normal method call
    return wrapped(*args, **kwargs)


class BaseFeature(ABC):
    """Base Feature definition / interface"""

    def __init__(self) -> None:
        self._loop: asyncio.AbstractEventLoop
        self._gopro: GoProBase[Any]

    @property
    @abstractmethod
    def is_supported(self) -> bool:
        """Is the feature supported on the  current camera?

        Returns:
            bool: True if ready, False otherwise
        """

    async def open(  # pylint: disable=unused-argument
        self,
        loop: asyncio.AbstractEventLoop,
        gopro: GoProBase[Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Open the feature for use.

        This should be called before using any other methods in the feature. It must be called for each
        GoProBase instance that is used with the feature.

        Args:
            loop (asyncio.AbstractEventLoop): asyncio loop to use for this feature
            gopro (GoProBase[Any]): camera to operate on
            *args (Any): additional arguments for subclasses
            **kwargs (Any): additional keyword arguments for subclasses
        """
        self._loop = loop
        self._gopro = gopro

    @abstractmethod
    async def close(self) -> None:
        """Close the feature for use."""
