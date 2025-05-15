# gopro.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:47 PM

"""Implements top level interface to GoPro module."""

from __future__ import annotations

import asyncio
import enum
import json
import logging
import threading
import traceback
from abc import abstractmethod
from typing import Any, Awaitable, Callable, Final, Generic, TypeVar

import requests
import wrapt

from open_gopro.api import (
    BleCommands,
    BleSettings,
    BleStatuses,
    HttpCommands,
    HttpSettings,
    WiredApi,
    WirelessApi,
)
from open_gopro.domain.communicator_interface import (
    GoProHttp,
    HttpMessage,
    Message,
    MessageRules,
)
from open_gopro.domain.exceptions import GoProNotOpened, ResponseTimeout
from open_gopro.models import GoProResp
from open_gopro.models.constants import ErrorCode
from open_gopro.models.types import JsonDict
from open_gopro.parsers.response import RequestsHttpRespBuilderDirector
from open_gopro.util import pretty_print
from open_gopro.util.logger import Logger

logger = logging.getLogger(__name__)

GoPro = TypeVar("GoPro", bound="GoProBase")
ApiType = TypeVar("ApiType", WiredApi, WirelessApi)
MessageMethodType = Callable[[Any, bool], Awaitable[GoProResp]]


class GoProMessageInterface(enum.Enum):
    """Enum to identify wireless interface"""

    HTTP = enum.auto()
    BLE = enum.auto()


@wrapt.decorator
def catch_thread_exception(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Callable | None:
    """Catch any exceptions from this method and pass them to the exception handler identifier by thread name

    Args:
        wrapped (Callable): method that this is wrapping
        instance (GoProBase): instance owner of method
        args (Any): positional args
        kwargs (Any): keyword args

    Returns:
        Callable | None: forwarded return of wrapped method or None if exception occurs
    """
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:  # pylint: disable=broad-exception-caught
        instance._handle_exception(threading.current_thread().name, {"exception": e})
        return None


def ensure_opened(interface: tuple[GoProMessageInterface]) -> Callable:
    """Raise exception if relevant interface is not currently opened

    Args:
        interface (tuple[GoProMessageInterface]): wireless interface to verify

    Returns:
        Callable: Direct pass-through of callable after verification
    """

    @wrapt.decorator
    def wrapper(wrapped: Callable, instance: GoProBase, args: Any, kwargs: Any) -> Callable:
        if GoProMessageInterface.BLE in interface and not instance.is_ble_connected:
            raise GoProNotOpened("BLE not connected")
        if GoProMessageInterface.HTTP in interface and not instance.is_http_connected:
            raise GoProNotOpened("HTTP interface not connected")
        return wrapped(*args, **kwargs)

    return wrapper


@wrapt.decorator
async def enforce_message_rules(wrapped: MessageMethodType, instance: GoProBase, args: Any, kwargs: Any) -> GoProResp:
    """Decorator proxy to call the GoProBase's _enforce_message_rules method.

    Args:
        wrapped (MessageMethodType): Operation to enforce
        instance (GoProBase): GoProBase instance to use
        args (Any): positional arguments to wrapped
        kwargs (Any): keyword arguments to wrapped

    Returns:
        GoProResp: common response object
    """
    return await instance._enforce_message_rules(wrapped, *args, **kwargs)


class GoProBase(GoProHttp, Generic[ApiType]):
    """The base class for communicating with all GoPro Clients"""

    HTTP_TIMEOUT: Final = 5
    HTTP_GET_RETRIES: Final = 5

    def __init__(self, **kwargs: Any) -> None:
        self._should_maintain_state = kwargs.get("maintain_state", True)
        self._exception_cb = kwargs.get("exception_cb", None)

    async def __aenter__(self: GoPro) -> GoPro:
        await self.open()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    @abstractmethod
    async def open(self, timeout: int = 10, retries: int = 5) -> None:
        """Connect to the GoPro Client and prepare it for communication

        Args:
            timeout (int): time before considering connection a failure. Defaults to 10.
            retries (int): number of connection retries. Defaults to 5.
        """

    @abstractmethod
    async def close(self) -> None:
        """Gracefully close the GoPro Client connection"""

    @property
    @abstractmethod
    async def is_ready(self) -> bool:
        """Is gopro ready to receive commands

        Returns:
            bool: yes if ready, no otherwise
        """

    @property
    @abstractmethod
    def _requests_session(self) -> requests.Session:
        """The requests session used to communicate with the GoPro Client

        Returns:
            requests.Session: requests session
        """

    @property
    @abstractmethod
    def identifier(self) -> str:
        """Unique identifier for the connected GoPro Client

        Returns:
            str: identifier
        """

    @property
    def version(self) -> str:
        """The API version that the connected camera supports

        Only 2.0 is currently supported

        Returns:
            str: supported version
        """
        return self._api.version

    @property
    @abstractmethod
    def http_command(self) -> HttpCommands:
        """Used to access the Wifi commands

        Returns:
            HttpCommands: the commands
        """

    @property
    @abstractmethod
    def http_setting(self) -> HttpSettings:
        """Used to access the Wifi settings

        Returns:
            HttpSettings: the settings
        """

    @property
    @abstractmethod
    def ble_command(self) -> BleCommands:
        """Used to call the BLE commands

        Returns:
            BleCommands: the commands
        """

    @property
    @abstractmethod
    def ble_setting(self) -> BleSettings:
        """Used to access the BLE settings

        Returns:
            BleSettings: the settings
        """

    @property
    @abstractmethod
    def ble_status(self) -> BleStatuses:
        """Used to access the BLE statuses

        Returns:
            BleStatuses: the statuses
        """

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Is this client ready for communication?

        Returns:
            bool: True if yes, False if no
        """

    @property
    @abstractmethod
    def is_ble_connected(self) -> bool:
        """Are we connected via BLE to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """

    @property
    @abstractmethod
    def is_http_connected(self) -> bool:
        """Are we connected via HTTP to the GoPro device?

        Returns:
            bool: True if yes, False if no
        """

    ##########################################################################################################
    #                                 End Public API
    ##########################################################################################################

    @abstractmethod
    async def _enforce_message_rules(
        self, wrapped: Callable, message: Message, rules: MessageRules, **kwargs: Any
    ) -> GoProResp:
        """Rule Enforcer. Called by enforce_message_rules decorator.

        Args:
            wrapped (Callable): operation to enforce
            message (Message): message passed to operation
            rules (MessageRules): rules to enforce
            **kwargs (Any) : arguments passed to operation

        Returns:
            GoProResp: Operation response
        """

    def _handle_exception(self, source: Any, context: JsonDict) -> None:
        """Gather exceptions from module threads and send through callback if registered.

        Note that this function signature matches asyncio's exception callback requirement.

        Args:
            source (Any): Where did the exception come from?
            context (JsonDict): Access exception via context["exception"]
        """
        # context["message"] will always be there; but context["exception"] may not
        if exception := context.get("exception", False):
            logger.error(f"Received exception {exception} from {source}")
            logger.error(traceback.format_exc())
            if self._exception_cb:
                self._exception_cb(exception)
        else:
            logger.error(f"Caught unknown message: {context['message']} from {source}")

    class _InternalState(enum.IntFlag):
        """State used to manage whether the GoPro instance is ready or not."""

        READY = 0
        ENCODING = 1 << 0
        SYSTEM_BUSY = 1 << 1

    @property
    @abstractmethod
    def ip_address(self) -> str:
        """The IP address of the GoPro device

        Raises:
            GoProNotOpened: The GoPro IP address is not yet available

        Returns:
            str: IP address
        """

    @property
    @abstractmethod
    def _base_url(self) -> str:
        """Build the base endpoint for USB commands

        Returns:
            str: base endpoint with URL from serial number
        """

    @property
    @abstractmethod
    def _api(self) -> ApiType:
        """Unique identifier for the connected GoPro Client

        Returns:
            ApiType: identifier
        """

    @staticmethod
    def _ensure_opened(interface: tuple[GoProMessageInterface]) -> Callable:
        """Raise exception if relevant interface is not currently opened

        Args:
            interface (tuple[GoProMessageInterface]): wireless interface to verify

        Returns:
            Callable: Direct pass-through of callable after verification
        """
        return ensure_opened(interface)

    @staticmethod
    def _catch_thread_exception(*args: Any, **kwargs: Any) -> Callable | None:
        """Catch any exceptions from this method and pass them to the exception handler identifier by thread name

        Args:
            *args (Any): positional args
            **kwargs (Any): keyword args

        Returns:
            Callable | None: forwarded return of wrapped method or None if exception occurs
        """
        return catch_thread_exception(*args, **kwargs)

    def _build_http_request_args(self, message: HttpMessage) -> dict[str, Any]:
        """Helper method to build request kwargs from message

        Args:
            message (HttpMessage): message to build args from

        Returns:
            dict[str, Any]: built args
        """
        # Dynamically build get kwargs
        request_args: dict[str, Any] = {}
        if message._headers:
            request_args["headers"] = message._headers
        if message._certificate:
            request_args["verify"] = str(message._certificate)
        return request_args

    @enforce_message_rules
    async def _get_json(
        self,
        message: HttpMessage,
        *,
        timeout: int = HTTP_TIMEOUT,
        rules: MessageRules = MessageRules(),
        **kwargs: Any,
    ) -> GoProResp:
        url = self._base_url + message.build_url(**kwargs)
        logger.debug(f"Sending:  {url}")
        logger.info(Logger.build_log_tx_str(pretty_print(message._as_dict(**kwargs))))
        for retry in range(1, GoProBase.HTTP_GET_RETRIES + 1):
            try:
                http_response = self._requests_session.get(
                    url,
                    timeout=timeout,
                    **self._build_http_request_args(message),
                )
                logger.trace(f"received raw json: {json.dumps(http_response.json() if http_response.text else {}, indent=4)}")  # type: ignore
                if not http_response.ok:
                    logger.warning(f"Received non-success status {http_response.status_code}: {http_response.reason}")
                response = RequestsHttpRespBuilderDirector(http_response, message._parser)()
                break
            except requests.exceptions.ConnectionError as e:
                # This appears to only occur after initial connection after pairing
                logger.warning(repr(e))
                # Back off before retrying. TODO This appears to be needed on MacOS
                await asyncio.sleep(2)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.critical(f"Unexpected error: {repr(e)}")
            logger.warning(f"Retrying #{retry} to send the command...")
        else:
            raise ResponseTimeout(GoProBase.HTTP_GET_RETRIES)

        logger.info(Logger.build_log_rx_str(pretty_print(response._as_dict())))
        return response

    @enforce_message_rules
    async def _get_stream(
        self,
        message: HttpMessage,
        *,
        timeout: int = HTTP_TIMEOUT,
        rules: MessageRules = MessageRules(),
        **kwargs: Any,
    ) -> GoProResp:
        url = self._base_url + message.build_url(path=kwargs["camera_file"])
        logger.debug(f"Sending:  {url}")
        with self._requests_session.get(
            url,
            stream=True,
            timeout=timeout,
            **self._build_http_request_args(message),
        ) as request:
            request.raise_for_status()
            file = kwargs["local_file"]
            with open(file, "wb") as f:
                logger.debug(f"receiving stream to {file}...")
                for chunk in request.iter_content(chunk_size=8192):
                    f.write(chunk)

        return GoProResp(protocol=GoProResp.Protocol.HTTP, status=ErrorCode.SUCCESS, data=file, identifier=url)

    @enforce_message_rules
    async def _put_json(
        self,
        message: HttpMessage,
        *,
        timeout: int = HTTP_TIMEOUT,
        rules: MessageRules = MessageRules(),
        **kwargs: Any,
    ) -> GoProResp:
        url = self._base_url + message.build_url(**kwargs)
        body = message.build_body(**kwargs)
        logger.debug(f"Sending:  {url} with body: {json.dumps(body, indent=4)}")
        for retry in range(1, GoProBase.HTTP_GET_RETRIES + 1):
            try:
                http_response = self._requests_session.put(
                    url,
                    timeout=timeout,
                    json=body,
                    **self._build_http_request_args(message),
                )
                logger.trace(f"received raw json: {json.dumps(http_response.json() if http_response.text else {}, indent=4)}")  # type: ignore
                if not http_response.ok:
                    logger.warning(f"Received non-success status {http_response.status_code}: {http_response.reason}")
                response = RequestsHttpRespBuilderDirector(http_response, message._parser)()
                break
            except requests.exceptions.ConnectionError as e:
                # This appears to only occur after initial connection after pairing
                logger.warning(repr(e))
                # Back off before retrying. TODO This appears to be needed on MacOS
                await asyncio.sleep(2)
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.critical(f"Unexpected error: {repr(e)}")
            logger.warning(f"Retrying #{retry} to send the command...")
        else:
            raise ResponseTimeout(GoProBase.HTTP_GET_RETRIES)

        return response
