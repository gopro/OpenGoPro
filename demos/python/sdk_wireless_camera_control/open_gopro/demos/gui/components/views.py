# views.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Aug 17 20:05:18 UTC 2022

"""GUI views and associated common functionality"""

# pylint: disable = arguments-differ

from __future__ import annotations

import enum
import json
import logging
import tkinter as tk
import tkinter.scrolledtext as ScrolledText
from abc import ABC, abstractmethod
from tkinter import font, ttk
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Optional,
    Sequence,
    TypeVar,
    Union,
    cast,
    no_type_check,
)
from urllib.parse import parse_qs, urlparse

from PIL import Image, ImageDraw, ImageTk

from open_gopro.demos.gui.components import THEME, models
from open_gopro.util import pretty_print

MAX_TREEVIEW_ID = 1000000

GetterType = Callable[[], Any]
T = TypeVar("T")


def sanitize_identifier(identifier: str) -> str:
    """Make the 'id' value human readable so that it looks the same for BLE and Wifi

    Args:
        identifier (str): identifier to sanitize

    Returns:
        str: sanitized response
    """
    identifier = (
        identifier.replace("_", " ")
        .lower()
        .removeprefix("cmdid.")
        .removeprefix("querycmdid.")
        .removeprefix("actionid.")
        .removeprefix("gopro/")
        .replace("/", " ")
        .title()
    )

    try:
        identifier = identifier.split("?")[0]
    except IndexError:
        pass

    return identifier


class DefaultTextEntry(ttk.Entry, Generic[T]):
    """A Tkinter Entry with default text that disappears when clicked

    Args:
        default (T): default value to show in entry

    Raises:
        ValueError: invalid entry type
    """

    def __init__(self, default: T, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        tk_var_type: type[tk.Variable]
        if isinstance(default, str):
            tk_var_type = tk.StringVar
        elif isinstance(default, bool):
            tk_var_type = tk.BooleanVar
        elif isinstance(default, int):
            tk_var_type = tk.IntVar
        elif isinstance(default, float):
            tk_var_type = tk.DoubleVar
        else:
            raise ValueError("entry_type must be one of [str, bool, int, float]")
        self.default: T = default
        self.var: tk.Variable = tk_var_type(value=self.default)
        self.insert(0, self.default)  # type: ignore
        self.bind("<FocusIn>", self.focus_in)

    def focus_in(self, *_: Any) -> None:
        """Called when entry is focused on, to remove default text

        Args:
            *_ (Any): Not used
        """
        if self.var.get() == self.default:
            self.delete(0, "end")

    def get(self) -> Optional[T]:  # type: ignore
        """Get the entry value. Will return none if the value is still default

        Returns:
            Optional[T]: value or None
        """
        return None if (current := cast(T, super().get())) == self.default else current


def popup_message(title: str, message: str, button: str = "OK") -> None:
    """Pop up a message in a separate window with an exit button.

    Args:
        title (str): Title of window
        message (str): message to display
        button (str): text to display in exit button. Defaults to "OK".
    """
    top = tk.Toplevel()
    # Get current mouse position
    abs_coord_x = top.winfo_pointerx() - top.winfo_rootx()
    abs_coord_y = top.winfo_pointery() - top.winfo_rooty()
    # Place window at mouse
    top.geometry(f"400x200+{abs_coord_x}+{abs_coord_y}")
    top.title(title)
    label = tk.Label(top, text=message, font=("Mistral 10 bold"), wraplength=350, pady=20)
    label.pack()

    def exit_btn() -> None:
        """On exit, close window"""
        top.destroy()
        top.update()

    btn = ttk.Button(top, text=button, command=exit_btn)
    btn.pack()


class View(ABC, tk.Widget):
    """View interface"""

    @no_type_check
    @abstractmethod
    def create_view(self) -> None:
        """Display the view (i.e. pack, grid, etc)"""
        raise NotImplementedError


class SplashScreen(View, tk.Frame):
    """Initial splash screen to connect a device"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        width = kwargs.pop("width", 200)
        height = kwargs.pop("height", 200)
        tk.Frame.__init__(self, *args, width=width, height=height, **kwargs)
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.style.theme_use(THEME)
        self.root.title("Open GoPro Device Selection")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.root.geometry(f"{width}x{height}")
        # Beta labal
        self.beta_label = ttk.Label(
            self.root,
            text="This is beta software!! Not all commands have been tested yet.",
            font="26",
            foreground="red",
        )
        # Choose
        self.choose_label = ttk.Label(self.root, text="Choose either: ", font="18")
        # Specific device input
        self.device_select_input = ttk.Frame(self.root)
        self.device_select = DefaultTextEntry(default="GoPro Device Name", master=self.device_select_input)
        self.device_select.grid(row=0, column=0, sticky="NSEW", padx=5)
        self.device_select_button = ttk.Button(self.device_select_input, text="Connect")
        self.device_select_button.grid(row=0, column=1)
        # Or..
        self.or_label = ttk.Label(self.root, text="or...", font="18")
        # Auto connect
        self.auto_connect_button = ttk.Button(self.root, text="Auto Connect To First Found GoPro")

    def create_view(self, command: Callable) -> None:
        """Display the Splash Screen

        Args:
            command (Callable): command to be called when buttons are clicked
        """
        self.beta_label.pack(pady=10)
        self.choose_label.pack(pady=10)
        self.device_select_input.pack()
        self.device_select_button.configure(command=command)
        self.or_label.pack()
        self.auto_connect_button.pack(pady=10)
        self.auto_connect_button.configure(command=command)


class Menubar(View, tk.Menu):
    """Menu Bar view (i.e exit, etc)"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Menu.__init__(self, *args, **kwargs)
        self.master.configure(menu=self)  # type: ignore
        self.fileMenu = tk.Menu(self)

    def create_view(self) -> None:
        """Display the menu bar"""
        self.add_cascade(label="File", menu=self.fileMenu)


class StatusBar(View, tk.Frame):
    """Status Bar View"""

    LABEL_WIDTH = 15
    STATUS_WIDTH = 25

    class Color(enum.Enum):
        """Predefined color values"""

        RED = "#f5c6d0"
        YELLOW = "#fcffa1"
        GREEN = "#a1ffaa"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.statuses: list[ttk.Label] = []
        self.ble_label: ttk.Label
        self.ble_status: ttk.Label
        self.wifi_label: ttk.Label
        self.wifi_status: ttk.Label
        self.ready_label: ttk.Label
        self.ready_status: ttk.Label
        self.stream_label: ttk.Label
        self.stream_status: ttk.Label
        self.encoding_label: ttk.Label
        self.encoding_status: ttk.Label

    def create_view(self) -> None:
        """Display the status bar"""
        self.pack(side=tk.BOTTOM, fill=tk.X)
        # BLE status
        self.ble_label = ttk.Label(self, text="BLE State:", relief=tk.RAISED, width=self.LABEL_WIDTH)
        self.ble_label.grid(row=0, column=0)
        self.ble_status = ttk.Label(
            self, text="Idle", relief=tk.RAISED, width=self.STATUS_WIDTH, background=StatusBar.Color.RED.value
        )
        self.ble_status.grid(row=0, column=1)
        # Wifi Status
        self.wifi_label = ttk.Label(self, text="Wifi State", relief=tk.RAISED, width=self.LABEL_WIDTH)
        self.wifi_label.grid(row=0, column=2)
        self.wifi_status = ttk.Label(
            self, text="Idle", relief=tk.RAISED, width=self.STATUS_WIDTH, background=StatusBar.Color.RED.value
        )
        self.wifi_status.grid(row=0, column=3)
        # Busy Status
        self.ready_label = ttk.Label(self, text="Ready State:", relief=tk.RAISED, width=self.LABEL_WIDTH)
        self.ready_label.grid(row=0, column=4)
        self.ready_status = ttk.Label(self, text="", relief=tk.RAISED, width=self.STATUS_WIDTH)
        self.ready_status.grid(row=0, column=5)
        # Encoding status
        self.encoding_label = ttk.Label(self, text="Encoding State:", relief=tk.RAISED, width=self.LABEL_WIDTH)
        self.encoding_label.grid(row=0, column=6)
        self.encoding_status = ttk.Label(self, text="", relief=tk.RAISED, width=self.STATUS_WIDTH)
        self.encoding_status.grid(row=0, column=7)
        # Stream Status
        self.stream_label = ttk.Label(self, text="Stream State:", relief=tk.RAISED, width=self.LABEL_WIDTH)
        self.stream_label.grid(row=0, column=8)
        self.stream_status = ttk.Label(
            self, text="IDLE", relief=tk.RAISED, width=self.STATUS_WIDTH, background=StatusBar.Color.RED.value
        )
        self.stream_status.grid(row=0, column=9)

    @staticmethod
    def update_status(status: ttk.Label, color: StatusBar.Color, text: str) -> None:
        """Update a status with a given color and text

        Args:
            status (ttk.Label): label to update
            color (StatusBar.Color): color to set the label to
            text (str): text to display on the label
        """
        status.configure(text=text, background=color.value)


class Video(View, tk.Frame):
    """Displays a video source in a tkinter window"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.frame_label = ttk.Label(self, text="Video Stream")
        self.input_frame = tk.Frame(self)
        self.url_entry = DefaultTextEntry(default="Stream URL", master=self.input_frame)
        self.url_entry.grid(row=0, column=0, sticky="NSEW", padx=5)
        self.start_button = ttk.Button(self.input_frame, text="Start")
        self.start_button.grid(row=0, column=1)
        self.stop_button = ttk.Button(self.input_frame, text="Stop")
        self.stop_button.grid(row=0, column=2)
        self.input_frame.grid_columnconfigure(0, weight=6)
        self.input_frame.grid_columnconfigure(1, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

    def create_view(self, start: Callable, stop: Callable) -> None:
        """Display the initial video view with no image

        Args:
            start (Callable): command to call when start is clicked
            stop (Callable): command to call when stop is clicked
        """
        self.frame_label.pack(side=tk.TOP)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.pack(expand=True, fill=tk.BOTH)
        self.start_button.config(command=start)
        self.stop_button.config(command=stop)

    def display_frame(self, photo: ImageTk.PhotoImage) -> None:
        """Display an individual video frame

        Args:
            photo (ImageTk.PhotoImage): frame to display
        """
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)


class Log(View, tk.Frame, ABC):
    """Log View interface"""

    class Format(enum.Enum):
        """Type of message to log

        For now, just sets the color
        """

        TX = "white"
        RX = "beige"
        ERROR = "#f5c6d0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)

    @abstractmethod
    def create_log_entry(self, record: logging.LogRecord) -> None:
        """Display and individual log entry

        Args:
            record (logging.LogRecord): record to log
        """
        raise NotImplementedError


class TreeViewLog(Log):
    """A Log displayed as a TreeView"""

    # custom indicator images
    im_open = Image.new("RGBA", (15, 15), "#00000000")
    im_empty = Image.new("RGBA", (15, 15), "#00000000")
    draw = ImageDraw.Draw(im_open)
    draw.polygon([(0, 4), (14, 4), (7, 11)], fill="white", outline="black")
    im_close = im_open.rotate(90)

    class Message:
        """An individual log message to displayed by a Tree View Log

        Args:
            record (logging.LogRecord): logger record that will comprise this message
            fmt (str): string to format a tuple of values

        Raises:
            ValueError: Not able to build a Message from this log record
        """

        ASYNC_TOKEN = "-ASYNC-"

        # NOTE! Direction is from perspective of PC
        def __init__(self, record: logging.LogRecord, fmt: str) -> None:
            self.fmt = fmt
            self.message = record.message.strip("\n")
            if self.message[2] == "<":
                self.direction = Log.Format.TX
            elif self.message[-3] == ">":
                self.direction = Log.Format.RX
            else:
                raise ValueError("Log message must start with a directional arrow")
            self.time = record.asctime
            self.is_async = self.ASYNC_TOKEN in self.message
            self.sanitize_message()
            try:
                self.data: dict = json.loads("{" + self.message + "}")
            except Exception as e:
                raise ValueError(f"Can not build log message from {self.message}") from e
            self.data["target"] = self.data.pop("uuid", None) or self.data.pop("endpoint", None)
            self.data["id"] = sanitize_identifier(self.data["id"])
            # Special case to handle wifi set setting response
            if self.data["id"].lower() == "camera setting":
                parsed_url = urlparse(self.data["target"])
                setting_id = int(parse_qs(parsed_url.query)["setting"][0])
                self.data["id"] = models.constants.SettingId(setting_id)
            self.data.pop("command", None)

        def sanitize_message(self) -> None:
            """Clean up the directional headers from the logger message string"""
            self.message = (
                self.message.replace(self.ASYNC_TOKEN, "")
                .strip("<>")
                .strip("-")
                .strip("<>")
                .replace("\t", "")
                .replace("\n", "")
                .strip(",")
            )

        @property
        def is_ok(self) -> bool:
            """Is the status ok or unknown?

            Returns:
                bool: True if yes, False otherwise
            """
            try:
                return self.data["status"].lower() in ["success", "unknown"]
            except KeyError:
                return True

        def logview_entries(self) -> Generator[tuple[str, tuple[str, ...]], None, None]:
            """From the Log Message, generate entries suitable for the Log View to consume

            Generates:
                1. top level description of message (formatted by self.fmt)
                2-N: individual elements of message as tuple(id, value)

            Yields:
                Generator[tuple[str, tuple[str, ...]], None, None]: see note in command description
            """
            work_dict = {**self.data, "log_time": self.time}
            # First yield top level
            out: list[str] = []
            for fmtstr in self.fmt:
                out.append(pretty_print(work_dict.pop(fmtstr, ""), should_quote=False))
            yield pretty_print(work_dict.pop("id"), should_quote=False), tuple(out)
            # Yield any additional items
            for key, value in work_dict.items():
                yield pretty_print(key, should_quote=False), (pretty_print(str(value), should_quote=False),)

        def __str__(self) -> str:
            return json.dumps(self.data, indent=4)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.tv = ttk.Treeview(self)
        self.tv["columns"] = ("log_time", "protocol", "target", "status")
        self.tv.column("log_time", width=20)
        self.tv.column("protocol", width=20)
        self.tv.column("status", width=50)
        self.tv.column("target", width=50)
        self.tv.heading("log_time", text="Time / Value")
        self.tv.heading("protocol", text="Protocol")
        self.tv.heading("status", text="Status")
        self.tv.heading("target", text="UUID / Endpoint")
        self.tv.tag_configure(Log.Format.TX.name, background=Log.Format.TX.value, foreground="black")
        self.tv.tag_configure(Log.Format.RX.name, background=Log.Format.RX.value, foreground="black")
        self.tv.tag_configure(Log.Format.ERROR.name, background=Log.Format.ERROR.value, foreground="black")
        self.sbv = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.tv.config(yscrollcommand=self.sbv.set)
        self.sbv.config(command=self.tv.yview)
        self.index = 0
        self.img_open = ImageTk.PhotoImage(TreeViewLog.im_open, name="img_open", master=self.winfo_toplevel())
        self.img_close = ImageTk.PhotoImage(TreeViewLog.im_close, name="img_close", master=self.winfo_toplevel())
        self.img_empty = ImageTk.PhotoImage(TreeViewLog.im_empty, name="img_empty", master=self.winfo_toplevel())
        self.style = ttk.Style(self.winfo_toplevel())
        self.style.element_create(
            "Treeitem.myindicator",
            "image",
            "img_close",
            ("user1", "!user2", "img_open"),
            ("user2", "img_empty"),
            sticky="w",
            width=15,
        )
        # replace Treeitem.indicator by custom one
        self.style.layout(
            "Treeview.Item",
            [
                (
                    "Treeitem.padding",
                    {
                        "sticky": "nswe",
                        "children": [
                            ("Treeitem.myindicator", {"side": "left", "sticky": ""}),
                            ("Treeitem.image", {"side": "left", "sticky": ""}),
                            (
                                "Treeitem.focus",
                                {
                                    "side": "left",
                                    "sticky": "",
                                    "children": [("Treeitem.text", {"side": "left", "sticky": ""})],
                                },
                            ),
                        ],
                    },
                )
            ],
        )

    def create_view(self) -> None:
        """Display the TreeView Log"""
        self.sbv.pack(side=tk.RIGHT, fill=tk.Y)
        self.tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pack(fill=tk.Y, expand=True)

    def create_log_entry_element(
        self, name: str, values: tuple[str, ...], fmt: Log.Format, parent: Optional[int] = None
    ) -> int:
        """Display an individual log entry element, potentially as a subtree

        Args:
            name (str): top level name of element
            values (tuple[str, ...]): values in element
            fmt (Log.Format): how to format the element
            parent (Optional[int], optional): Parent of element if part of subtree. Defaults to None.

        Returns:
            int: identifier of this created element
        """
        self.tv.insert(
            parent=str(parent or ""),
            index="end",
            iid=str(self.index),
            text=name,
            values=values,
            tags=fmt.name,
        )
        ret_index = self.index
        self.index += 1

        # Scroll to bottom
        self.tv.yview_moveto(1)

        return ret_index

    def create_log_entry(self, record: logging.LogRecord) -> None:
        """Create a log entry from a logging record

        Args:
            record (logging.LogRecord): record to analyze
        """
        try:
            msg = TreeViewLog.Message(record, self.tv["columns"])
        except ValueError:  # It doesn't have an arrow so we can't log it
            return
        logview_entry_gen = msg.logview_entries()
        name, values = next(logview_entry_gen)
        parent = self.create_log_entry_element(name, values, msg.direction if msg.is_ok else Log.Format.ERROR)
        for name, values in logview_entry_gen:
            self.create_log_entry_element(name, values, msg.direction, parent)


class TextLog(Log):
    """A Log View displayed as scrolled text"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.viewer = ScrolledText.ScrolledText(self, state="disabled")

    def create_view(self) -> None:
        """Display the text log view"""
        self.viewer.pack(expand=True, fill=tk.X)

    def create_log_entry(self, record: logging.LogRecord) -> None:
        """Create a text log entry from a logging record

        Args:
            record (logging.LogRecord): logging record to analyze
        """
        self.viewer.configure(state="normal")
        self.viewer.insert(tk.END, record.message + "\n")
        self.viewer.configure(state="disabled")
        # Autoscroll to the bottom
        self.viewer.yview(tk.END)


class ParamForm(View, tk.Frame):
    """A entry form to gather message arguments"""

    FRAME_TITLE_ROW = 0
    MESSAGE_NAME_ROW = 1
    PARAM_START_ROW = 2

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.value_inputs: list[Union[tk.Variable, ttk.Entry]] = []
        self.arg_frames: list[tk.Frame] = []
        self.frame_label: ttk.Label
        self.message_label: ttk.Label
        self.value_label: ttk.Label
        self.value_menu: ttk.OptionMenu
        self.send_button: ttk.Button

    def create_view(self) -> None:
        """Display the parameter form"""
        self.frame_label = ttk.Label(self, text="Parameter Configuration", name="frame_label")
        self.frame_label.pack()
        self.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    @property
    def param_row(self) -> int:
        """Get the current parameter row as the argument entry form is built

        Returns:
            int: parameter row
        """
        return len(self.value_inputs) + self.PARAM_START_ROW

    @property
    def active_arg_frame(self) -> tk.Frame:
        """Get the active tkinter frame of the argument that is currently being built

        Returns:
            tk.Frame: active argument frame
        """
        return self.arg_frames[-1]

    def reset_view(self) -> None:
        """Destroy the current argument entries"""
        for widget in self.winfo_children():
            if "frame_label" not in str(widget):
                widget.destroy()
        self.value_inputs.clear()
        self.arg_frames.clear()

    def create_message(self, message: str) -> None:
        """Create a message label

        Args:
            message (str): name of message
        """
        self.message_label = ttk.Label(self, text=message)
        self.message_label.pack()

    def _create_with_args(self, param: str) -> None:
        """Create an entry that includes an argument

        Args:
            param (str): text of argument
        """
        self.arg_frames.append(tk.Frame(self))
        self.active_arg_frame.pack()
        self.value_label = ttk.Label(self.active_arg_frame, text=param, anchor="w")
        self.value_label.pack(side=tk.LEFT)

    def create_option_menu(self, param: str, options: Sequence[str], default: Optional[str] = None) -> GetterType:
        """Create a drop down menu for an argument

        Args:
            param (str): name of argument
            options (Sequence[str]): all possible argument options
            default (Optional[str], optional): The default option. If none, the first option will be chosen.
                Defaults to None.

        Returns:
            GetterType: a getter to get this option menu value
        """
        self._create_with_args(param)
        value_input = tk.StringVar(self.active_arg_frame)
        default = default or options[0]
        value_input.set(default)
        self.value_menu = ttk.OptionMenu(self.active_arg_frame, value_input, default, *options)
        self.value_menu.pack(side=tk.RIGHT)
        self.value_inputs.append(value_input)
        return value_input.get

    def create_entry(self, param: str) -> GetterType:
        """Create a text entry for an argument

        Args:
            param (str): name of argument

        Returns:
            GetterType: A getter to get this text entry value
        """
        self._create_with_args(param)
        value_input = ttk.Entry(self.active_arg_frame)
        value_input.pack(side=tk.RIGHT)
        self.value_inputs.append(value_input)
        return value_input.get

    def create_button(self, label: str, command: Callable) -> None:
        """Create a button in the parameter entry form

        Args:
            label (str): string to place in button
            command (Callable): command to call when button is pressed
        """
        self.send_button = ttk.Button(self, text=label, command=command)
        self.send_button.pack()


class MessagePalette(View, tk.Frame):
    """A hierarchal display of messages by functionality for the user to select"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.tv = ttk.Treeview(self)
        self.sbv = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.tv.config(yscrollcommand=self.sbv.set)
        self.sbv.config(command=self.tv.yview)
        self.frame_label = ttk.Label(self, text="Message Palette")

    def create_view(self, messages: dict[str, list[str]]) -> None:
        """Display the message palette

        Args:
            messages (dict[str, list[str]]): dictionary to be mapped to message palette hierarchy
        """
        self.frame_label.pack()
        self.sbv.pack(side=tk.RIGHT, fill=tk.Y)
        self.tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pack(fill=tk.Y, expand=True)
        # Fill up tree view
        parent_index = MAX_TREEVIEW_ID
        child_index = 0
        for parent, children in messages.items():
            self.tv.insert(parent="", index="end", iid=str(parent_index), text=parent)
            for message in children:
                if "." in (identifier := sanitize_identifier(message)):
                    identifier = " ".join(identifier.split(".")[1:])
                self.tv.insert(
                    parent=str(parent_index),
                    index="end",
                    iid=str(child_index),
                    text=identifier,
                )
                child_index += 1
            self.tv.item(str(parent_index), open=True)
            parent_index += 1


class StatusTab(View, tk.Frame):
    """A Status window to display current setting values / capabilities and status values

    Most recent updates will be highlighted
    """

    STATUS_ID_OFFSET = int(MAX_TREEVIEW_ID / 2)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        tk.Frame.__init__(self, *args, **kwargs)
        self.tv = ttk.Treeview(self)
        self.tv["columns"] = ("value", "capabilities")
        self.tv.column("value", width=200)
        self.tv.column("capabilities", width=400)
        self.tv.heading("value", text="Value")
        self.tv.heading("capabilities", text="Capabilities")
        self.tv.tag_configure("recent", background="#73ffff", foreground="black")

        self.sbv = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sbh = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.tv.config(yscrollcommand=self.sbv.set)
        self.tv.config(xscrollcommand=self.sbh.set)
        self.sbv.config(command=self.tv.yview)
        self.sbh.config(command=self.tv.xview)
        self.setting_parent = str(MAX_TREEVIEW_ID)
        self.status_parent = str(int(self.setting_parent) + 1)
        self.setting_to_id: dict[int, str] = {}
        self.status_to_id: dict[int, str] = {}
        self.recent_tags: list[str] = []

    def create_view(self) -> None:
        """Display the Status Tab"""
        self.sbv.pack(side=tk.RIGHT, fill=tk.Y)
        self.sbh.pack(side=tk.TOP, fill=tk.X)
        self.tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.pack(fill=tk.Y, expand=True)
        # Fill up tree view. Start with just parents labels
        self.tv.insert(parent="", index="end", iid=self.setting_parent, text="Settings")
        self.tv.item(self.setting_parent, open=True)
        self.tv.insert(parent="", index="end", iid=self.status_parent, text="Statuses")
        self.tv.item(self.status_parent, open=True)

    def store_new_status(self, index: int) -> None:
        """Add a new status to the internal status index-id map

        Args:
            index (int): status index
        """
        self.status_to_id[index] = str(index + self.STATUS_ID_OFFSET)

    def store_new_setting(self, index: int) -> None:
        """Add a new setting to the internal setting index-id map

        Args:
            index (int): setting index
        """
        self.setting_to_id[index] = str(index)

    def _common_update(
        self,
        identifier: enum.IntEnum,
        update_map: dict[int, str],
        parent: str,
        store: Callable[[int], None],
        value: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> None:
        """Common functionality to update a setting / status, storing new index if needed.

        One of value or capability must be non-None

        Args:
            identifier (enum.IntEnum): ID of setting / status to update
            update_map (dict[int, str]): index-to-id translation map
            parent (str): parent of this identifier
            store (Callable[[int], None]): method to store new index in update_map
            value (Optional[str], optional): value of update. Defaults to None.
            capability (Optional[str], optional): capability of update. Defaults to None.

        Raises:
            ValueError: Either value or capability must be non-None
        """
        # Empty string is a valid input so explicitly check if is None
        if value is None and capability is None:
            raise ValueError("Require value or capability")

        # Does it already exist?
        if tree_index := update_map.get(int(identifier)):
            # The values key in TreeView will return all of its value (values and caps from our perspective)
            current_values = self.tv.item(tree_index)["values"]
            # Need to check is not None because falsy empty string is a valid input
            new_values = tuple(new if new is not None else old for new, old in zip((value, capability), current_values))
            self.tv.item(tree_index, tags=("recent",), values=new_values)
        else:
            store(int(identifier))
            tree_index = update_map[int(identifier)]
            self.tv.insert(
                parent=parent,
                index="end",
                iid=tree_index,
                text=pretty_print(identifier),
                values=(value or "", capability or ""),
                tags=("recent",),
            )
        self.recent_tags.append(tree_index)

    def update_setting(self, identifier: enum.IntEnum, value: str) -> None:
        """Display a setting value update

        Args:
            identifier (enum.IntEnum): setting that has been updated
            value (str): new value of setting
        """
        self._common_update(
            identifier,
            update_map=self.setting_to_id,
            store=self.store_new_setting,
            parent=self.setting_parent,
            value=value,
        )

    def update_capability(self, identifier: enum.IntEnum, capability: str) -> None:
        """Display a setting capability update

        Args:
            identifier (enum.IntEnum): setting that has been updated
            capability (str): new capability of setting
        """
        self._common_update(
            identifier,
            update_map=self.setting_to_id,
            parent=self.setting_parent,
            store=self.store_new_setting,
            capability=capability,
        )

    def update_status(self, identifier: enum.IntEnum, value: str) -> None:
        """Display a status value update

        Args:
            identifier (enum.IntEnum): status that has been updated
            value (str): new value of status
        """
        self._common_update(
            identifier,
            update_map=self.status_to_id,
            parent=self.status_parent,
            store=self.store_new_status,
            value=value,
        )

    def clear_recent_tags(self) -> None:
        """Set all currently marked 'recent' updates as not 'recent'"""
        for tree_index in self.recent_tags:
            self.tv.item(tree_index, tags=())
        self.recent_tags.clear()
