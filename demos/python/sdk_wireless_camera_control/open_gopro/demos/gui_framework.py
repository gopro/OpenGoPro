# gui_framework.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jul  6 19:59:52 UTC 2022

"""Common GUI framework functionality to use async with Tkinter"""

# cv2's members can not be discovered by mypy
# pylint: disable=no-member

from __future__ import annotations
import queue
import asyncio
import logging
from pathlib import Path
import tkinter as tk
import tkinter.scrolledtext as ScrolledText
from typing import Union, Callable, Any, List, Type, Optional

import wrapt
import cv2
import PIL.Image
import PIL.ImageTk

from open_gopro.util import setup_logging

logger = logging.getLogger(__name__)


class AppWidget:
    """Common widget functionality for use with Open GoPro GUI framework"""

    def __init__(self, window: Window) -> None:
        """Constructor

        Args:
            window (Window): Window that will control this widget
        """
        self.window = window

    @property
    def root(self) -> tk.Tk:
        """Access the tkinter root

        Returns:
            tk.Tk: top level root
        """
        return self.window.root

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Acceess the asyncio loop where the GUI thread is running

        Returns:
            asyncio.AbstractEventLoop: asyncio loop
        """
        return self.window.loop

    @property
    def logger(self) -> logging.Logger:
        """Get the logger that is configured for use with the Tkinter App

        Raises:
            RuntimeError: Logger has not yet been configured

        Returns:
            logging.Logger: logger that is ready for logging
        """
        if module_logger := self.window.log_handler.logger:
            return module_logger
        raise RuntimeError("Attempt to use logger before it was configured.")

    def as_async(self, action: Callable, *args: Any) -> Any:
        """Create an asynchronous coroutine from a synchonous function / method

        Args:
            action (Callable): function / method
            args (List[any]): arguments to action

        Returns:
            Any: asynchronous coroutine. Should be awaited in an async method.
        """
        return self.loop.run_in_executor(None, action, *args)


class VideoCapture:
    """Displays a video source in a tkinter window"""

    def __init__(
        self,
        video_source: Union[int, str] = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        """Constructor

        Args:
            video_source (Union[int, str], Optional): video device handle or stream URL. Defaults to 0 (default system video).
            width (Optional[int], Optional): video frame width. Will be set by cv2 if None.
            height (Optional[int], Optional): video frame height. Will be set by cv2 if None.

        Raises:
            ValueError: failed opening the video source
        """
        self.image: PIL.Image.Image
        self.photo: PIL.ImageTk.PhotoImage
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = width or int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = height or int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def display_frame(self, canvas: tk.Canvas) -> None:
        """Get, process, and display a video frame

        Args:
            canvas (tk.Canvas): TKinter canvas to display video frame
        """
        ret = False
        frame = None
        if self.vid.isOpened():
            ret, frame = self.vid.read()

        if ret and frame is not None:
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.image = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def __del__(self) -> None:
        # Release the video source when the object is destroyed
        if self.vid.isOpened():
            self.vid.release()


@wrapt.decorator
def background(wrapped: Callable, instance: AppWidget, args: Any, kwargs: Any) -> Any:
    """Decorator to schedule a widget method in the background as an async task

    Args:
        wrapped (Callable): widget method to send to background
        instance (AppWidget): Widget instance where the method exists
        args (Any): any positional arguments
        kwargs (Any): any keyword arguments

    Returns:
        Any: Task object (not needed)
    """
    return instance.loop.create_task(wrapped(*args, **kwargs))


class LogHandler(logging.Handler):
    """A log handler to be used with TKinter async GUI frameowrk

    Does not actually display from emit. Instead, it queues messages for later displaying in the GUI thread.
    """

    def __init__(self, level: logging._Level = logging.DEBUG) -> None:
        """Constructor

        Args:
            level (logging._Level, Optional): Logging level. Defaults to logging.DEBUG.
        """
        super().__init__(level)
        self.log_q: queue.Queue[str] = queue.Queue()
        self.logger: Optional[logging.Logger] = None

    @property
    def viewer(self) -> ScrolledText.ScrolledText:
        """Get the log viewer widget

        Raises:
            RuntimeError: attempt access viewer before it was set

        Returns:
            ScrolledText.ScrolledText: log viewer widget
        """
        if self._viewer:
            return self._viewer
        raise RuntimeError("Log viewer has not been set.")

    @viewer.setter
    def viewer(self, viewer: ScrolledText.ScrolledText) -> None:
        """Set the log viewer widget

        Will also configure the log handler

        Args:
            viewer (ScrolledText.ScrolledText): log viewer widget
        """
        self._viewer = viewer
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S"))
        self.setLevel(logging.INFO)
        # Configure logging
        global logger
        logger = setup_logging(logger, Path("livestream_gui.log"), handlers=(self,))
        logger.info("Starting GUI")
        self.logger = logger

    def emit(self, record: logging.LogRecord) -> None:
        """Enqueue the log record string for later displaying in GUI thread

        Args:
            record (logging.LogRecord): record to enqueuef
        """
        self.log_q.put_nowait(self.format(record))

    def log_queued_messages(self) -> None:
        """Dequeue log records and display them until the queue is empty

        WARNING! This must be called from the main GUI thread
        """

        while not self.log_q.empty() and (msg := self.log_q.get_nowait()):
            self.viewer.configure(state="normal")
            self.viewer.insert(tk.END, msg + "\n")
            self.viewer.configure(state="disabled")
            # Autoscroll to the bottom
            self.viewer.yview(tk.END)


class Window:
    """A Tkinter async Open GoPro GUI Window

    Note that the widgets will be insantiated (and thus packed / placed) in the order they exist in the
    input list.
    """

    def __init__(self, widgets: List[Type[AppWidget]], title: str) -> None:
        """Constructor

        Args:
            widgets (List[Type[AppWidget]]): List of widgets to be instantiated by Window
            title (str): Window title
        """
        self.widgets = widgets
        self.loop: asyncio.AbstractEventLoop
        self.root = tk.Tk()
        self.root.title(title)
        self.log_handler = LogHandler()
        self._should_quit = False

    def set_log_viewer(self, viewer: ScrolledText.ScrolledText) -> None:
        """Configure a ScrolledText widget to be used to diplay logs

        If called twice, the initial widget will be overriden.

        Args:
            viewer (ScrolledText.ScrolledText): widget to use for logs
        """
        self.log_handler.viewer = viewer

    def quit(self) -> None:
        """Quit the Window (and thus the entire GUI)"""
        self._should_quit = True

    async def exec(self) -> None:
        """The main GUI processing loop

        Will asyncio.sleep(0) after each iteration for cooperative multitasking
        """
        self.loop = asyncio.get_event_loop()
        for widget in self.widgets:
            widget(self)

        while not self._should_quit:
            self.log_handler.log_queued_messages()
            self.root.update()
            await asyncio.sleep(0)
        self.root.quit()


def create_and_run(widgets: List[Type[AppWidget]], title: str) -> None:
    """Helper function to build and run a GUI from a list of widget types

    Individual widget classes should handle packing / displaying their members

    Args:
        widgets (List[Type[AppWidget]]): List of widgets to put in the GUI
        title (str): window title
    """
    asyncio.run(Window(widgets, title).exec())
