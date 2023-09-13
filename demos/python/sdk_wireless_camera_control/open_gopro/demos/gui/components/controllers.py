# controllers.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 17 20:05:18 UTC 2022

"""GUI controllers and associated common functionality"""

from __future__ import annotations

import asyncio
import datetime
import enum
import logging
import queue
import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Any, Callable, Optional, Union, no_type_check

import cv2
import PIL.Image
import PIL.ImageTk
import wrapt

from open_gopro.demos.gui.components import models, views
from open_gopro.logger import add_logging_handler, setup_logging
from open_gopro.util import pretty_print

ResponseHandlerType = Callable[[str, models.GoProResp], None]


def create_widget(
    master: tk.Widget, view: type[views.View], controller: Controller, *args: Any, **kwargs: Any
) -> views.View:
    """Create a widget, binding a view to a controller

    Args:
        master (tk.Widget): master to use for widget
        view (type[views.View]): type of view to use
        controller (Controller): controller instance to use
        args (Any): positional arguments
        kwargs (Any): keyword arguments

    Returns:
        views.View: instantiated view (i.e. widget)
    """
    v = view(master, *args, **kwargs)
    controller.bind(v)
    return v


class MissingArgument(Exception):
    """Exception raised when a message is attempted to be sent without all of its arguments"""

    def __init__(self, argument: Optional[str]) -> None:
        super().__init__(f"Missing required argument for {argument}")


class BadArgumentValue(Exception):
    """Exception raised when an argument fails a validator check"""

    def __init__(self, argument: Optional[str]) -> None:
        super().__init__(f"Bad value for argument {argument}")


@wrapt.decorator
def background(wrapped: Callable, instance: Controller, args: Any, kwargs: Any) -> None:
    """Perform an action in the background in order to not block the main GUI processing

    Args:
        wrapped (Callable): action to perform
        instance (Controller): controller that owns action
        args (Any): positional arguments
        kwargs (Any): keyword arguments
    """
    instance.loop.create_task(wrapped(*args, **kwargs))


class Controller(ABC):
    """Controller base class

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
    """

    controllers: list[Controller] = []

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self._logger: Optional[logging.Logger] = None
        Controller.controllers.append(self)

    @property
    def logger(self) -> logging.Logger:
        """Get the controller's logger

        Raises:
            RuntimeError: logger has not yet been configured

        Returns:
            logging.Logger: logger
        """
        if self._logger:
            return self._logger
        raise RuntimeError("Logger not yet configured")

    @logger.setter
    def logger(self, logger: logging.Logger) -> None:
        self._logger = logger

    @no_type_check
    @abstractmethod
    def bind(self, view: views.View) -> None:
        """Bind a view to the controller

        Args:
            view (views.View): view to bind
        """
        raise NotImplementedError

    def as_async(self, action: Callable, *args: Any, **kwargs: Any) -> Any:
        """Create an asynchronous coroutine from a synchronous function / method

        Args:
            action (Callable): function / method
            *args (Any): positional arguments to action
            **kwargs (Any): keyword arguments to action

        Returns:
            Any: asynchronous coroutine. Should be awaited in an async method.
        """
        return self.loop.run_in_executor(None, partial(action, *args, **kwargs))


class SplashScreen(Controller):
    """Splash screen used to connect a GoPro

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
        model (models.GoProModel): GoPro device
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, model: models.GoProModel) -> None:
        super().__init__(loop)
        self.model = model
        self._are_models_started = False
        self.view: views.SplashScreen

    @property
    def are_models_started(self) -> bool:
        """Are all of the models started?

        Returns:
            bool: yes or no
        """
        return self._are_models_started

    def bind(self, view: views.SplashScreen) -> None:
        """Bind a splash screen view

        Args:
            view (views.SplashScreen): view to bind
        """
        self.view = view
        self.view.create_view(lambda: self.view.after(1, self.open_models))

    async def update(self) -> None:
        """Update the GUI to display changes"""
        self.view.root.update()
        await asyncio.sleep(0)

    @background
    async def open_models(self) -> None:
        """Open models in the background"""
        device = self.view.device_select.get()
        await self.as_async(self.model.start, device)
        self._are_models_started = True


class Menubar(Controller):
    """Menu bar controller

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
        on_quit (Callable): command to call when quit is clicked
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, on_quit: Callable) -> None:
        super().__init__(loop)
        self.quit = on_quit
        self.view: views.Menubar

    def bind(self, view: views.Menubar) -> None:
        """Bind a menubar view

        Args:
            view (views.Menubar): view to bind
        """
        self.view = view
        view.create_view()
        self.view.fileMenu.add_command(label="Exit", command=self.quit)


class StatusBar(Controller):
    """Status bar

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
    """

    class Ble(enum.Enum):
        """BLE status options"""

        IDLE = views.StatusBar.Color.RED
        CONNECTING = views.StatusBar.Color.YELLOW
        CONNECTED = views.StatusBar.Color.GREEN

    class Wifi(enum.Enum):
        """WiFi status options"""

        IDLE = views.StatusBar.Color.RED
        CONNECTING = views.StatusBar.Color.YELLOW
        CONNECTED = views.StatusBar.Color.GREEN

    class Encoding(enum.Enum):
        """Encoding status options"""

        ON = views.StatusBar.Color.RED
        OFF = views.StatusBar.Color.GREEN

    class Ready(enum.Enum):
        """Ready status options"""

        READY = views.StatusBar.Color.GREEN
        BUSY = views.StatusBar.Color.RED

    class Stream(enum.Enum):
        """Stream status options"""

        IDLE = views.StatusBar.Color.RED
        STARTING = views.StatusBar.Color.YELLOW
        READY = views.StatusBar.Color.GREEN

    StatusType = Union[Ble, Wifi, Encoding, Ready, Stream]

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        super().__init__(loop)
        self.view: views.StatusBar

    def bind(self, view: views.StatusBar) -> None:
        """Bind a StatusBar view

        Args:
            view (views.StatusBar): view to bind
        """
        self.view = view
        view.create_view()

    def update_status(self, status: StatusType) -> None:
        """Update a status. The relevant status icon will be found based on the passed in status

        Args:
            status (StatusType): new status

        Raises:
            ValueError: a status was passed that is not associated with any status icon
        """

        if status in StatusBar.Ble:
            self.view.update_status(self.view.ble_status, status.value, status.name.replace("_", " ").title())
        elif status in StatusBar.Wifi:
            self.view.update_status(self.view.wifi_status, status.value, status.name.replace("_", " ").title())
        elif status in StatusBar.Ready:
            self.view.update_status(self.view.ready_status, status.value, status.name.replace("_", " ").title())
        elif status in StatusBar.Encoding:
            self.view.update_status(self.view.encoding_status, status.value, status.name.replace("_", " ").title())
        elif status in StatusBar.Stream:
            self.view.update_status(self.view.stream_status, status.value, status.name.replace("_", " ").title())
        else:
            raise ValueError(f"No handler for status {status}")

    def handle_updates(self, identifier: enum.Enum, value: Any) -> None:
        """Check to see if an update requires a status change

        Args:
            identifier (enum.Enum): identifier to analyze
            value (Any): value to analyze
        """
        if identifier == models.constants.StatusId.ENCODING:
            self.update_status(StatusBar.Encoding.ON if value else StatusBar.Encoding.OFF)
        elif identifier == models.constants.StatusId.SYSTEM_BUSY:
            self.update_status(StatusBar.Ready.BUSY if value else StatusBar.Ready.READY)


class Video(Controller):
    """Displays a video source in a tkinter window

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
    """

    # pylint: disable=no-member
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        super().__init__(loop)
        self.image: PIL.Image.Image
        self.photo: PIL.ImageTk.PhotoImage
        self.vid: Any = None
        self.height: int
        self.width: int
        self.status_bar: StatusBar
        self.should_stop = False
        self.view: views.Video

    @property
    def is_open(self) -> bool:
        """Is the video currently open?

        Returns:
            bool: yes if open, no otherwise
        """
        return self.vid is not None and self.vid.isOpened()

    def bind(self, view: views.Video) -> None:
        """Bind a video view

        Args:
            view (views.Video): view to bind
        """
        self.view = view
        self.view.create_view(self.start, self.stop)

    def bind_status_bar(self, controller: StatusBar) -> None:
        """Bind a status bar controller to use for updating statuses

        Args:
            controller (StatusBar): controller to bind
        """
        self.status_bar = controller

    def start(self, source: Optional[str]) -> None:
        """Start playing a video

        If source is not passed, it will be extracted from the input entry

        Args:
            source (Optional[str]): desired video source or None to get from View
        """
        if self.is_open:
            views.popup_message("Error", "Stream is already started. Must stop first.")
            return

        video_source = source or self.view.url_entry.get()
        if video_source in (None, ""):
            views.popup_message("Error", "Missing required stream URL")
            return
        assert video_source
        # See if this is to be interpreted as an int
        self.status_bar.update_status(StatusBar.Stream.STARTING)
        # Open the video source
        self.logger.debug(f"Starting video from: {video_source}")
        self.vid = cv2.VideoCapture(video_source)
        if not self.is_open:
            views.popup_message("Error", f"Unable to open video source {video_source}")
        self.height = self.view.canvas.winfo_height()
        self.width = self.view.canvas.winfo_width()
        self.should_stop = False
        self.status_bar.update_status(StatusBar.Stream.READY)
        self.get_frame()

    def handle_auto_start(self, identifier: str, response: models.GoProResp) -> None:
        """Auto start live or preview stream

        Args:
            identifier (str): message that was sent
            response (models.GoProResp): response that was received
        """
        # Get binary's (which are of type Path) are not handled. TODO updating typing for this
        if not isinstance(response, models.GoProResp) or not response.ok:
            return

        # TODO This is broken
        video_source: Optional[str] = None
        if str(identifier).lower() == "livestream":
            video_source = response.identifier  # type: ignore
        elif str(identifier).lower() == "set preview stream" and "start" in (str(response.identifier) or ""):
            video_source = models.PREVIEW_STREAM_URL

        if video_source:
            if self.is_open:
                self.logger.debug("Stopping current stream due to new stream starting.")
                self.stop()
            self.start(video_source)

    def stop(self) -> None:
        """Stop playing the video"""
        if not self.is_open:
            views.popup_message("Error", "Stream is not started.")
            return
        self.should_stop = True

    def get_frame(self) -> None:
        """Get an individual video frame to display"""
        ret = False
        frame = None
        if self.vid.isOpened():
            ret, frame = self.vid.read()

        if ret and frame is not None:
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.image = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.image)
            self.view.display_frame(self.photo)

        if self.should_stop:
            self.vid.release()
            self.status_bar.update_status(StatusBar.Stream.IDLE)
        else:
            self.view.after(5, self.get_frame)

    def __del__(self) -> None:
        # Release the video source when the object is destroyed
        if self.vid.isOpened():
            self.vid.release()


class Log(Controller, logging.Handler):
    """Controller to use for displaying logs.

    Is capable of binding multiple views and then selecting per-record which one to use

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
        level (logging._Level, optional): log level to start at. Defaults to logging.INFO.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, level: int = logging.INFO) -> None:
        Controller.__init__(self, loop)
        logging.Handler.__init__(self, level)
        self.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d %(message)s", datefmt="%H:%M:%S"))
        self.setLevel(level)
        self.log_q: queue.Queue[logging.LogRecord] = queue.Queue()
        # Configure logging
        try:
            logger = setup_logging(__name__, Path("gui.log"))
        except RuntimeError:
            # logger is already configured, just get it
            logger = logging.getLogger(__name__)
        add_logging_handler(self)
        self.logger = logger
        self.views: list[views.Log] = []

    def bind(self, view: views.Log) -> None:
        """Bind a log view

        Args:
            view (views.Log): view to bind
        """
        view.create_view()
        self.views.append(view)

    def emit(self, record: logging.LogRecord) -> None:
        """Enqueue the log record string for later displaying in GUI thread

        Args:
            record (logging.LogRecord): record to enqueue
        """
        try:
            self.log_q.put_nowait(record)
        except ValueError:
            return

    def log_queued_messages(self, view: views.Log) -> None:
        """Dequeue log records and display them until the queue is empty

        WARNING! This must be called from the main GUI thread

        Args:
            view (views.Log): view to display records in

        Raises:
            RuntimeError: this view is not bound
        """
        if view not in self.views:
            raise RuntimeError("This view has not been bound to the log controller")
        while not self.log_q.empty() and (record := self.log_q.get_nowait()):
            view.create_log_entry(record)


class MessagePalette(Controller):
    """Pallet to hierarchically display messages and allow user to select.

    This control is used to control a message palette and param form

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
        model (models.GoProModel): model to get messages from
    """

    @dataclass
    class MessageMeta:
        """Couple the message and its identifier"""

        identifier: str
        message: Callable

    @dataclass
    class Argument:
        """Get, store, and process a message argument

        Args:
            getter (Callable): used to get the string value of the argument from a GUI element
            adapter (Callable): used to adapter the argument string value
            validator (Callable): used to validate the adapted value
            name (Optional[str]): name of argument
        """

        getter: Callable[[], Any]
        adapter: Callable[[Any], Any]
        validator: Callable[[Any], None]
        name: Optional[str] = None

        def process(self, validate: bool = True) -> Any:
            """Get, adapt, and optionally validate an argument

            Args:
                validate (bool): Should argument value be validated?. Defaults to True.

            Raises:
                MissingArgument: was not able to get the argument value
                BadArgumentValue: validation failed

            Returns:
                Any: argument value
            """
            value = self.getter()
            try:
                value = self.adapter(value)
            except Exception as e:
                raise MissingArgument(self.name) from e
            if validate:
                try:
                    self.validator(value)
                except Exception as e:
                    raise BadArgumentValue(self.name) from e
            return value

    def __init__(self, loop: asyncio.AbstractEventLoop, model: models.GoProModel) -> None:
        Controller.__init__(self, loop)
        self.model = model
        self.active_message: Optional[MessagePalette.MessageMeta] = None
        self.active_arguments: list[MessagePalette.Argument] = []
        self.param_form: views.ParamForm
        self.message_palette: views.MessagePalette
        self.response_handlers: list[ResponseHandlerType] = []

    def _bind_message_palette(self, view: views.MessagePalette) -> None:
        """Bind message pallet view

        Args:
            view (views.MessagePalette): view to bind
        """
        self.message_palette = view
        self.message_palette.create_view(self.model.message_dict)
        self.message_palette.tv.bind("<Button-1>", self.on_message_selection)

    def _bind_param_form(self, view: views.ParamForm) -> None:
        """Bind param form view

        Args:
            view (views.ParamForm): view to bind
        """
        self.param_form = view
        self.param_form.create_view()

    def bind(self, view: Union[views.MessagePalette, views.ParamForm]) -> None:
        """Bind a view (message palette or param form)

        Args:
            view (Union[views.MessagePalette, views.ParamForm]): view to bind

        Raises:
            TypeError: Invalid view
        """
        if isinstance(view, views.MessagePalette):
            self._bind_message_palette(view)
        elif isinstance(view, views.ParamForm):
            self._bind_param_form(view)
        else:
            raise TypeError("Only MessagePalette and ParamForms can be bound to MessagePalette Controller")

    def register_response_handler(self, handler: ResponseHandlerType) -> None:
        """Register response handler for message responses

        Args:
            handler (ResponseHandlerType): response handler controller
        """
        self.response_handlers.append(handler)

    def build_param_entries(self, message: models.Message) -> None:
        """Display all params for a given message in the param form

        Args:
            message (MessageType): message to build params for

        Raises:
            ValueError: found a parameter with a currently unhandled argument type
        """
        for adapter, validator, arg_type, arg_name in zip(*self.model.get_message_info(message)):
            getter: Callable
            if arg_type is None:
                continue
            if arg_type == bool:
                getter = self.param_form.create_option_menu(arg_name, ["True", "False"])
            elif arg_type in (int, float, str, bytes, bytearray, Path):
                getter = self.param_form.create_entry(arg_name)
            elif issubclass(arg_type, enum.Enum):
                getter = self.param_form.create_option_menu(arg_name, [x.name for x in arg_type])
            elif arg_type == datetime.datetime:
                getters: list[views.GetterType] = []
                getters.append(self.param_form.create_entry("year"))
                getters.append(self.param_form.create_entry("month"))
                getters.append(self.param_form.create_entry("day"))
                getters.append(self.param_form.create_entry("hour"))
                getters.append(self.param_form.create_entry("minute"))
                getters.append(self.param_form.create_entry("second"))
                getter = lambda getters=getters: tuple(int(get()) for get in getters)
                validator = lambda x: isinstance(x, datetime.datetime)
                adapter = lambda x: datetime.datetime(*x)
            else:
                raise ValueError("Unexpected argument type")

            self.active_arguments.append(MessagePalette.Argument(getter, adapter, validator, arg_name))

    def on_message_selection(self, event: Any) -> None:
        """Called when a message is selected to create param entries

        Args:
            event (Any): GUI event that prompted message selection
        """
        try:
            item_id = int(self.message_palette.tv.identify("item", event.x, event.y))
            if item_id >= views.MAX_TREEVIEW_ID:
                return
        except ValueError:  # User clicked outside of message area
            return
        self.param_form.reset_view()
        self.active_message = None
        self.active_arguments.clear()
        identifier, message = self.model.messages[item_id]
        self.param_form.create_message(identifier)

        if self.model.is_command(message):
            if not self.model.is_compound_command(message):
                self.active_arguments.append(
                    MessagePalette.Argument(
                        getter=lambda: self.model.gopro,
                        adapter=lambda x: x,
                        validator=lambda x: x.is_open,
                    )
                )
            self.build_param_entries(message)
            self.param_form.create_button("Send message", self.message_sender_factory(use_args=True))
        else:  # Setting or Status
            if self.model.is_ble(message):
                self.param_form.create_button("Get Value", self.message_sender_factory("get_value"))
                self.param_form.create_button(
                    "Register for Value Updates", self.message_sender_factory("register_value_update")
                )
                self.param_form.create_button(
                    "Unregister for Value Updates", self.message_sender_factory("unregister_value_update")
                )
                if self.model.is_setting(message):
                    self.param_form.create_button(
                        "Get Capabilities", self.message_sender_factory("get_capabilities_values")
                    )
                    self.param_form.create_button(
                        "Register for Capability Updates",
                        self.message_sender_factory("register_capability_update"),
                    )

                    self.param_form.create_button(
                        "Unregister for Capability Updates",
                        self.message_sender_factory("unregister_capability_update"),
                    )
            if not self.model.is_status(message):
                self.param_form.create_button("Set Value", self.message_sender_factory("set", use_args=True))
                self.build_param_entries(message)

        self.active_message = MessagePalette.MessageMeta(identifier, message)

    def message_sender_factory(self, attribute: Optional[str] = None, use_args: bool = False) -> Callable:
        """Build a method to be called when a message is requested to be sent

        Args:
            attribute (Optional[str], optional): Method of active message to use. Defaults to None (use active
                message directly).
            use_args (bool): Should the active args be passed to the message?. Defaults to False.

        Returns:
            Callable: method to use
        """

        @background
        async def on_message_send(self: MessagePalette) -> Optional[models.GoProResp]:
            assert self.active_message
            method = (
                self.active_message.message if attribute is None else getattr(self.active_message.message, attribute)
            )
            args = []
            kwargs = {}
            if use_args:
                for arg in self.active_arguments:
                    value = arg.process()
                    if name := arg.name:
                        kwargs[name] = value
                    else:
                        args.append(value)

            try:
                response = await self.as_async(method, *args, **kwargs)
            except Exception as e:  # pylint: disable=broad-except
                views.popup_message("Error", str(e))
                return None

            for handler in self.response_handlers:
                handler(self.active_message.identifier, response)
            return response

        return on_message_send.__get__(self, None)


class StatusTab(Controller):
    """Status tab controller to display updates in various status elements.

    New updates will be highlighted

    Args:
        loop (asyncio.AbstractEventLoop): already running asyncio loop to use for controllers
        model (models.GoProModel): model to build updates from
        poll_period (int, optional): how often to refresh updates (in ms). Defaults to 200.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, model: models.GoProModel, poll_period: int = 200) -> None:
        super().__init__(loop)
        self.model = model
        self.period = poll_period
        self.statusbar: Optional[StatusBar] = None
        self.view: views.StatusTab

    def bind(self, view: views.StatusTab) -> None:
        """Bind a status tab view

        Args:
            view (views.StatusTab): view to bind
        """
        self.view = view
        view.create_view()

    def bind_statusbar(self, statusbar: StatusBar) -> None:
        """Bind a status bar

        Args:
            statusbar (StatusBar): view to bind
        """
        self.statusbar = statusbar

    def _display_updates(self, response: Optional[models.GoProResp] = None) -> None:
        """Display any updates take from the response

        Args:
            response (Optional[models.GoProResp], optional): response to get updates from. Defaults to None.
                If none, model will check for asynchronous updates
        """

        cleared = False
        for identifier, value, update_type in self.model.updates(response):
            # Clear recents
            if not cleared:
                self.view.clear_recent_tags()
                cleared = True

            # A list must be a capability update
            if update_type is models.GoProModel.Update.CAPABILITY:
                self.view.update_capability(identifier, pretty_print(value))
                continue
            if update_type is models.GoProModel.Update.PROTOBUF:
                continue
            if update_type is models.GoProModel.Update.SETTING:
                self.view.update_setting(identifier, pretty_print(value))
            elif update_type is models.GoProModel.Update.STATUS:
                self.view.update_status(identifier, pretty_print(value))

            if self.statusbar:
                self.statusbar.handle_updates(identifier, value)

    def display_async_updates(self) -> None:
        """Display any updates that were received asynchronously (i.e. not message responses)"""
        self._display_updates()

    def display_response_updates(self, _: str, response: Optional[models.GoProResp]) -> None:
        """Display updates from the message response

        Args:
            response (Optional[models.GoProResp]): response to get updates from
        """
        self._display_updates(response)

    def poll(self) -> None:
        """Display updates every poll period ms"""
        self.display_async_updates()
        self.view.after(self.period, self.poll)
