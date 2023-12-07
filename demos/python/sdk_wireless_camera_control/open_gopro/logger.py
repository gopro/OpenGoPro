# logger.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Aug 24 17:08:14 UTC 2023

"""Logger abstraction above default python logging"""

from __future__ import annotations

import http.client as http_client
import logging
from pathlib import Path
from typing import Any, Final

from rich import traceback
from rich.logging import RichHandler


class Logger:
    """A singleton class to manage logging for the Open GoPro internal modules

    Args:
        logger (logging.Logger): input logger that will be modified and then returned
        output (Path, Optional): Path of log file for file stream handler. If not set, will not log to file.
        modules (dict[str, int], Optional): Optional override of modules / levels. Will be merged into default
            modules.
    """

    _instances: dict[type[Logger], Logger] = {}
    ARROW_HEAD_COUNT: Final = 8
    ARROW_TAIL_COUNT: Final = 14

    def __new__(cls, *_: Any) -> Any:  # noqa https://github.com/PyCQA/pydocstyle/issues/515
        if cls not in cls._instances:
            c = object.__new__(cls)
            cls._instances[cls] = c
            return c
        raise RuntimeError("The logger can only be setup once and this should be done at the top level.")

    def __init__(
        self,
        logger: Any,
        output: Path | None = None,
        modules: list[str] | None = None,
    ) -> None:
        self.modules = [
            "open_gopro.gopro_base",
            "open_gopro.gopro_wired",
            "open_gopro.gopro_wireless",
            "open_gopro.api.builders",
            "open_gopro.api.http_commands",
            "open_gopro.api.ble_commands",
            "open_gopro.communication_client",
            "open_gopro.ble.adapters.bleak_wrapper",
            "open_gopro.ble.client",
            "open_gopro.wifi.adapters.wireless",
            "open_gopro.wifi.mdns_scanner",
            "open_gopro.responses",
            "open_gopro.util",
            "bleak",
            "urllib3",
            "http.client",
        ]

        self.logger = logger
        self.modules = modules or self.modules
        self.handlers: list[logging.Handler] = []

        # monkey-patch a `print` global into the http.client module; all calls to
        # print() in that module will then use our logger's debug method
        http_client.HTTPConnection.debuglevel = 1
        http_client.print = lambda *args: logging.getLogger("http.client").debug(" ".join(args))  # type: ignore

        self.file_handler: logging.Handler | None
        if output:
            # Logging to file with millisecond timing
            self.file_handler = logging.FileHandler(output, mode="w")
            file_formatter = logging.Formatter(
                fmt="%(threadName)13s:%(asctime)s.%(msecs)03d %(filename)-40s %(lineno)4s %(levelname)-8s | %(message)s",
                datefmt="%H:%M:%S",
            )
            self.file_handler.setFormatter(file_formatter)
            # Set to TRACE for concurrency debugging
            self.file_handler.setLevel(logging.DEBUG)
            logger.addHandler(self.file_handler)
            self.addLoggingHandler(self.file_handler)
        else:
            self.file_handler = None

        # Use Rich for colorful console logging
        self.stream_handler = RichHandler(rich_tracebacks=True, enable_link_path=True, show_time=False)
        stream_formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S")
        self.stream_handler.setFormatter(stream_formatter)
        self.stream_handler.setLevel(logging.INFO)
        logger.addHandler(self.stream_handler)
        self.addLoggingHandler(self.stream_handler)

        self.addLoggingLevel("TRACE", logging.DEBUG - 5)
        logger.setLevel(logging.TRACE)  # type: ignore # pylint: disable=no-member

        traceback.install()  # Enable exception tracebacks in rich logger

    @classmethod
    def get_instance(cls) -> Logger:
        """Get the singleton instance

        Raises:
            RuntimeError: Has not yet been instantiated

        Returns:
            Logger: singleton instance
        """
        if not (logger := cls._instances.get(Logger, None)):
            raise RuntimeError("Logging must first be setup")
        return logger

    def addLoggingHandler(self, handler: logging.Handler) -> None:
        """Add a handler for all of the internal GoPro modules

        Args:
            handler (logging.Handler): handler to add
        """
        self.logger.addHandler(handler)
        self.handlers.append(handler)

        # Enable / disable logging in modules
        for module in self.modules:
            l = logging.getLogger(module)
            l.setLevel(logging.TRACE)  # type: ignore
            l.addHandler(handler)

    # From https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility/35804945#35804945
    @staticmethod
    def addLoggingLevel(levelName: str, levelNum: int) -> None:
        """Comprehensively adds a new logging level to the `logging` module and the currently configured logging class.

        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present

        Example:
        --------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5

        Args:
            levelName (str): name of level (i.e. TRACE)
            levelNum (int): integer level of new logging level
        """
        methodName = levelName.lower()

        def logForLevel(self: Any, message: str, *args: Any, **kwargs: Any) -> None:
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message: str, *args: Any, **kwargs: Any) -> None:
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    @staticmethod
    def build_log_tx_str(stringable: Any) -> str:
        """Build a string with Tx arrows

        Args:
            stringable (Any): stringable object to surround with arrows

        Returns:
            str: string surrounded by Tx arrows
        """
        s = str(stringable).strip(r"{}")
        arrow = f"{'<'*Logger.ARROW_HEAD_COUNT}{'-'*Logger.ARROW_TAIL_COUNT}"
        return f"\n{arrow}{s}{arrow}\n"

    @staticmethod
    def build_log_rx_str(stringable: Any, asynchronous: bool = False) -> str:
        """Build a string with Rx arrows

        Args:
            stringable (Any): stringable object to surround with arrows
            asynchronous (bool): Should the arrows contain ASYNC?. Defaults to False.

        Returns:
            str: string surrounded by Rx arrows
        """
        s = str(stringable).strip(r"{}")
        assert Logger.ARROW_TAIL_COUNT > 5
        if asynchronous:
            arrow = f"{'-'*(Logger.ARROW_TAIL_COUNT//2-3)}ASYNC{'-'*(Logger.ARROW_TAIL_COUNT//2-2)}{'>'*Logger.ARROW_HEAD_COUNT}"
        else:
            arrow = f"{'-'*Logger.ARROW_TAIL_COUNT}{'>'*Logger.ARROW_HEAD_COUNT}"
        return f"\n{arrow}{s}{arrow}\n"


def setup_logging(
    base: logging.Logger | str, output: Path | None = None, modules: list[str] | None = None
) -> logging.Logger:
    """Configure the GoPro modules for logging and get a logger that can be used by the application

    This can only be called once and should be done at the top level of the application.

    Args:
        base (Union[logging.Logger, str]): Name of application (i.e. __name__) or preconfigured logger to use as base
        output (Path, Optional): Path of log file for file stream handler. If not set, will not log to file.
        modules (dict[str, int], Optional): Optional override of modules / levels. Will be merged into default
            modules.

    Raises:
        TypeError: Base logger is not of correct type

    Returns:
        logging.Logger: updated logger that the application can use for logging
    """
    if isinstance(base, str):
        base = logging.getLogger(base)
    elif not isinstance(base, logging.Logger):
        raise TypeError("Base must be of type logging.Logger or str")
    l = Logger(base, output, modules)
    return l.logger


def set_file_logging_level(level: int) -> None:
    """Change the global logging level for the default file output handler

    Args:
        level (int): level to set
    """
    if fh := Logger.get_instance().file_handler:
        fh.setLevel(level)


def set_stream_logging_level(level: int) -> None:
    """Change the global logging level for the default stream output handler

    Args:
        level (int): level to set
    """
    Logger.get_instance().stream_handler.setLevel(level)


def set_logging_level(level: int) -> None:
    """Change the global logging level for the default file and stream output handlers

    Args:
        level (int): level to set
    """
    set_file_logging_level(level)
    set_stream_logging_level(level)


def add_logging_handler(handler: logging.Handler) -> None:
    """Add a handler to all of the GoPro internal modules

    Args:
        handler (logging.Handler): handler to add
    """
    Logger.get_instance().addLoggingHandler(handler)
