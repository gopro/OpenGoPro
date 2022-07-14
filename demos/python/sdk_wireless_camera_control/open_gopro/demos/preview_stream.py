# preview_stream.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Jul  7 23:14:49 UTC 2022

"""A simple GUI to demo preview stream functionality."""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as ScrolledText

from open_gopro import GoPro, Params
import open_gopro.demos.gui_framework as gui


class PreviewStreamFrame(gui.AppWidget, tk.Frame):
    """The tkinter frame to contain all of the preview stream demo widgets"""

    WIDTH = 400
    HEIGHT = 300
    INPUT_WIDTH = 50
    VID_UPDATE_DELAY = 15
    URL = r"udp://127.0.0.1:8554"

    def __init__(self, window: gui.Window) -> None:
        gui.AppWidget.__init__(self, window)
        tk.Frame.__init__(self, self.root)
        self.gopro: GoPro = GoPro()
        self.video: gui.VideoCapture
        self.build_gui()
        self.should_quit = False

    def build_gui(self) -> None:
        """Configure all of the widgets needed for initial GUI display"""

        # Setup the main video_canvas
        self.video_canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        # Setup the input form
        self.input_frame = ttk.Frame()
        # Buttons
        self.button_start = ttk.Button(self.input_frame, text="Start preview stream", command=self.start)
        self.button_start.grid(row=0, columnspan=2)
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
        """Start setting up preview stream and configure GUI to remove input form

        Raises:
            Exception: Failed to open Video Source
        """

        # Remove all input widgets
        self.input_frame.pack_forget()

        self.logger.info("Connecting to BLE...")
        await self.as_async(self.gopro.open)
        # Turn off shutter in case it was already on
        await self.as_async(self.gopro.ble_command.set_shutter, Params.Shutter.OFF)
        # Stop preview stream in case it was running
        await self.as_async(self.gopro.wifi_command.stop_preview_stream)
        self.logger.info("Enabling preview stream...")
        # Start preview stream
        await self.as_async(self.gopro.wifi_command.start_preview_stream)
        self.logger.info("Preview has been enabled.")

        # Add stop button
        self.button_stop.pack(anchor="center", expand=True)
        # Start displaying video
        self.video_canvas.pack()
        try:
            self.video = gui.VideoCapture(self.URL, self.WIDTH, self.HEIGHT)
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error(repr(e))
            self.logger.critical("Unable to continue.")
            raise e
        self.update_video()

    @gui.background
    async def stop(self) -> None:
        """Stop the preview stream"""

        self.should_quit = True  # Stop video-update loop
        if self.gopro:
            if self.gopro.is_ble_connected:
                await self.as_async(self.gopro.wifi_command.stop_preview_stream)
            await self.as_async(self.gopro.close)
        self.window.quit()

    def update_video(self) -> None:
        """Periodically update the video every VID_UPDATE_DELAY ms"""
        self.video.display_frame(self.video_canvas)
        if not self.should_quit:
            self.root.after(self.VID_UPDATE_DELAY, self.update_video)


def main() -> None:
    gui.create_and_run(widgets=[PreviewStreamFrame], title="Open GoPro preview stream Demo")


if __name__ == "__main__":
    main()
