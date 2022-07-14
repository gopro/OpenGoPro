# live_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jul  6 19:59:52 UTC 2022

"""A simple GUI to demo live stream functionality."""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText

from open_gopro import GoPro, Params
from open_gopro.constants import ActionId
import open_gopro.demos.gui_framework as gui


class LiveStreamFrame(gui.AppWidget, tk.Frame):
    """The tkinter frame to contain all of the live stream demo widgets"""

    WIDTH = 400
    HEIGHT = 300
    INPUT_WIDTH = 50
    VID_UPDATE_DELAY = 15

    def __init__(self, window: gui.Window) -> None:
        gui.AppWidget.__init__(self, window)
        tk.Frame.__init__(self, self.root)
        self.gopro: GoPro = GoPro(enable_wifi=False)
        self.video: gui.VideoCapture
        self.build_gui()
        self.should_quit = False

    def build_gui(self) -> None:
        """Configure all of the widgets needed for initial GUI display"""

        # Setup the main video_canvas
        self.video_canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        # Setup the input form
        self.input_frame = ttk.Frame()
        # URL
        self.label_url = ttk.Label(self.input_frame, text="URL")
        self.label_url.grid(row=0, column=0, sticky="w")
        self.input_url = ttk.Entry(self.input_frame, width=self.INPUT_WIDTH)
        self.input_url.grid(row=0, column=1)
        # SSID
        self.label_ssid = ttk.Label(self.input_frame, text="SSID")
        self.label_ssid.grid(row=1, column=0, sticky="w")
        self.input_ssid = ttk.Entry(self.input_frame, width=self.INPUT_WIDTH)
        self.input_ssid.grid(row=1, column=1)
        # Password
        self.label_password = ttk.Label(self.input_frame, text="Password")
        self.label_password.grid(row=2, column=0, sticky="w")
        self.input_password = ttk.Entry(self.input_frame, width=self.INPUT_WIDTH, show="*")
        self.input_password.grid(row=2, column=1)
        # Window Size Drop Down
        self.label_window_size = ttk.Label(self.input_frame, text="Window Size")
        self.label_window_size.grid(row=3, column=0, sticky="w")
        self.window_size = tk.StringVar(self.input_frame)
        self.window_size.set(Params.WindowSize.SIZE_720.name)  # default value
        self.menu_window_size = ttk.OptionMenu(
            self.input_frame, self.window_size, *[x.name for x in Params.WindowSize]
        )
        self.menu_window_size.grid(row=3, column=1, sticky="w")
        # Len Type Drop Down
        self.label_lens_type = ttk.Label(self.input_frame, text="Lens Type")
        self.label_lens_type.grid(row=4, column=0, sticky="w")
        self.lens_type = tk.StringVar(self.input_frame)
        self.lens_type.set(Params.LensType.WIDE.name)  # default value
        self.menu_lens_type = ttk.OptionMenu(
            self.input_frame, self.lens_type, *[x.name for x in Params.LensType]
        )
        self.menu_lens_type.grid(row=4, column=1, sticky="w")
        # Minimum bitrate
        self.label_min_bitrate = ttk.Label(self.input_frame, text="Minimum Bitrate")
        self.label_min_bitrate.grid(row=5, column=0, sticky="w")
        self.min_bit_text = tk.StringVar()
        self.min_bit_text.set("800")
        self.input_min_bitrate = ttk.Entry(
            self.input_frame, width=self.INPUT_WIDTH, textvariable=self.min_bit_text
        )
        self.input_min_bitrate.grid(row=5, column=1)
        # Maximum bitrate
        self.label_max_bitrate = ttk.Label(self.input_frame, text="Maximum Bitrate")
        self.label_max_bitrate.grid(row=6, column=0, sticky="w")
        self.max_bit_text = tk.StringVar()
        self.max_bit_text.set("8000")
        self.input_max_bitrate = ttk.Entry(
            self.input_frame, width=self.INPUT_WIDTH, textvariable=self.max_bit_text
        )
        self.input_max_bitrate.grid(row=6, column=1)
        # Starting bitrate
        self.label_start_bitrate = ttk.Label(self.input_frame, text="Starting Bitrate")
        self.label_start_bitrate.grid(row=7, column=0, sticky="w")
        self.start_bit_text = tk.StringVar()
        self.start_bit_text.set("1000")
        self.input_start_bitrate = ttk.Entry(
            self.input_frame, width=self.INPUT_WIDTH, textvariable=self.start_bit_text
        )
        self.input_start_bitrate.grid(row=7, column=1)
        # Buttons
        self.button_start = ttk.Button(self.input_frame, text="Start Livestream", command=self.start)
        self.button_start.grid(row=8, columnspan=2)
        self.button_stop = ttk.Button(self.root, text="Stop (and exit)", command=self.stop)
        self.input_frame.pack()
        # Add text widget to display logging info
        self.log_viewer = ScrolledText.ScrolledText(self, state="disabled")
        self.log_viewer.configure(font="TkFixedFont")
        self.log_viewer.grid(column=0, row=1, sticky="w", columnspan=4)
        # Configure root window to use this widget for displaying the log
        self.window.set_log_viewer(self.log_viewer)
        self.pack()

    @gui.background
    async def start(self) -> None:
        """Start setting up livestream and configure GUI to remove input form

        Raises:
            Exception: Failed to open Video Source
        """

        # Get inputs as strings
        try:
            ssid = self.input_ssid.get()
            password = self.input_password.get()
            url = self.input_url.get()
            window_size = Params.WindowSize[self.window_size.get()].value
            lens_type = Params.LensType[self.lens_type.get()].value
            min_bit = int(self.input_min_bitrate.get())
            max_bit = int(self.input_max_bitrate.get())
            start_bit = int(self.input_start_bitrate.get())
            # Validate input
            if [
                x
                for x in (ssid, password, url, window_size, lens_type, min_bit, max_bit, start_bit)
                if x == ""
            ]:
                self.logger.critical("Missing argument(s)!")
                return
        except Exception as e:  # pylint: disable=broad-except
            self.logger.critical(repr(e))
            return

        # Remove all input widgets
        self.input_frame.pack_forget()

        self.logger.info("Connecting to BLE...")
        await self.as_async(self.gopro.open)
        # Turn off shutter in case it was already on
        await self.as_async(self.gopro.ble_command.set_shutter, Params.Shutter.OFF)
        await self.as_async(self.gopro.ble_command.request_wifi_connect, ssid, password)
        while (
            update := await self.as_async(self.gopro.get_notification)
        ) and update != ActionId.NOTIF_PROVIS_STATE:
            pass
        if update["provisioningState"] == Params.ProvisioningState.SUCCESS_NEW_AP:
            self.logger.info("Connected to Wifi AP!")
        else:
            self.logger.info(f"Connection to Wifi AP failed: {update['provisioningState']}")

        self.logger.info("Enabling livestream...")
        await self.as_async(
            self.gopro.ble_command.set_livestream_mode,
            url,
            window_size,
            bytes([0]),
            min_bit,
            max_bit,
            start_bit,
            lens_type,
        )
        await self.as_async(self.gopro.ble_command.set_shutter, Params.Shutter.ON)
        self.logger.info("Livestream has been enabled.")

        # Add stop button
        self.button_stop.pack(anchor="center", expand=True)
        # Start displaying video
        self.video_canvas.pack()
        try:
            self.video = gui.VideoCapture(url, self.WIDTH, self.HEIGHT)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error(repr(e))
            self.logger.critical("Unable to continue.")
            raise e
        self.update_video()

    @gui.background
    async def stop(self) -> None:
        """Stop the livestream"""

        self.should_quit = True  # Stop video-update loop
        if self.gopro:
            if self.gopro.is_ble_connected:
                await self.as_async(self.gopro.ble_command.set_shutter, Params.Shutter.OFF)
            await self.as_async(self.gopro.close)
        self.window.quit()

    def update_video(self) -> None:
        """Periodically update the video every VID_UPDATE_DELAY ms"""
        self.video.display_frame(self.video_canvas)
        if not self.should_quit:
            self.root.after(self.VID_UPDATE_DELAY, self.update_video)


def main() -> None:
    gui.create_and_run(widgets=[LiveStreamFrame], title="Open GoPro Livestream Demo")


if __name__ == "__main__":
    main()
