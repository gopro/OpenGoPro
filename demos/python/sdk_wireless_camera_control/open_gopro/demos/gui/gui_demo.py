# gui_demo.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Mon Sep 12 20:44:38 UTC 2022

"""Top level of GUI"""

from __future__ import annotations

import asyncio
import logging
import tkinter as tk
from tkinter import font, ttk

from open_gopro.demos.gui.components import THEME, controllers, models, views

logger = logging.getLogger(__name__)


class App(tk.Frame):
    """Top level App frame"""

    HEIGHT = 1300
    ASPECT_RATIO = 16 / 9
    WIDTH = int(HEIGHT * ASPECT_RATIO)
    SASH_WIDTH = 2
    TOOLBAR_HEIGHT = 25
    SPLASH_WIDTH = 1000
    SPLASH_HEIGHT = 500
    FONT_SIZE = 12

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.style.theme_use(THEME)
        self.style.configure("Treeview", font=(None, App.FONT_SIZE), rowheight=int(App.FONT_SIZE * 3))
        tk.Frame.__init__(self, master=self.root, width=self.WIDTH, height=self.HEIGHT)
        self.root.title("Open GoPro")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(size=App.FONT_SIZE)
        self.views: list[views.View] = []
        self.create_models()
        self.create_controllers()
        self.create_views()
        self._should_quit = False
        self.root.withdraw()  # Hide for now

    @property
    def controllers(self) -> list[controllers.Controller]:
        """List of created controllers

        Returns:
            list[controllers.Controller]: controllers
        """
        return controllers.Controller.controllers

    def create_models(self) -> None:
        """Create all models"""
        self.gopro_model = models.GoProModel()
        self.models = [self.gopro_model]

    def create_controllers(self) -> None:
        """Create all controllers"""
        self.message_palette_controller = controllers.MessagePalette(self.loop, self.gopro_model)
        self.main_log_controller = controllers.Log(self.loop, logging.INFO)
        self.statusbar_controller = controllers.StatusBar(self.loop)
        self.video_controller = controllers.Video(self.loop)
        self.video_controller.bind_status_bar(self.statusbar_controller)
        self.menubar_controller = controllers.Menubar(self.loop, self.quit)
        self.statustab_controller = controllers.StatusTab(self.loop, self.gopro_model)
        self.message_palette_controller.register_response_handler(self.statustab_controller.display_response_updates)
        self.message_palette_controller.register_response_handler(self.video_controller.handle_auto_start)
        self.statustab_controller.bind_statusbar(self.statusbar_controller)
        for controller in self.controllers:
            controller.logger = self.main_log_controller.logger
        self.splash_controller = controllers.SplashScreen(self.loop, self.gopro_model)
        self.splash_log_controller = controllers.Log(self.loop, logging.INFO)
        self.splash_controller.logger = self.splash_log_controller.logger

    def create_views(self) -> None:
        """Create all views"""
        self.splash = controllers.create_widget(
            master=self,
            view=views.SplashScreen,
            controller=self.splash_controller,
            width=self.SPLASH_WIDTH,
            height=self.SPLASH_HEIGHT,
        )
        self.splash_log = controllers.create_widget(
            master=self.splash.root,  # type: ignore
            view=views.TextLog,
            controller=self.splash_log_controller,
        )
        self.splash_log.pack(expand=True, fill=tk.BOTH)

        # Set up paned window (everything except toolbars)
        self.panes = tk.PanedWindow(
            master=self,
            orient=tk.HORIZONTAL,
            bd=self.SASH_WIDTH,
            width=self.WIDTH,
            height=self.HEIGHT - self.TOOLBAR_HEIGHT,
        )
        self.panes.pack(fill=tk.BOTH, expand=True)

        # Left pane (Message palette)
        self.message_palette = controllers.create_widget(
            master=self.panes,
            view=views.MessagePalette,
            controller=self.message_palette_controller,
            width=int(self.WIDTH * 0.4),
            relief=tk.SUNKEN,
        )
        self.panes.add(self.message_palette, stretch="always")

        # Middle pane (param form / log)
        self.middle_pane = tk.PanedWindow(
            master=self.panes,
            orient=tk.VERTICAL,
            bd=self.SASH_WIDTH,
            width=int(self.WIDTH * 0.45),
        )
        self.middle_pane.propagate(False)
        self.middle_pane.pack(fill=tk.BOTH, expand=True)
        self.panes.add(self.middle_pane, stretch="always")
        self.param_form = controllers.create_widget(
            master=self.middle_pane,
            view=views.ParamForm,
            controller=self.message_palette_controller,
            height=int(self.HEIGHT * 0.2),
            bd=self.SASH_WIDTH,
            relief=tk.SUNKEN,
        )
        self.middle_pane.add(self.param_form, stretch="always", minsize=int(self.HEIGHT * 0.2))
        self.main_log = controllers.create_widget(
            master=self.middle_pane,
            view=views.TreeViewLog,
            controller=self.main_log_controller,
            height=int(self.HEIGHT * 0.8),
            bd=self.SASH_WIDTH,
            relief=tk.SUNKEN,
        )
        self.middle_pane.add(self.main_log, stretch="always", minsize=int(self.HEIGHT * 0.5))

        # Right Pane (data view / video)
        self.right_pane = tk.PanedWindow(
            master=self.panes,
            orient=tk.VERTICAL,
            width=int(self.WIDTH * 0.25),
            bd=self.SASH_WIDTH,
        )
        self.right_pane.pack(fill=tk.BOTH, expand=True)
        self.panes.add(self.right_pane, stretch="always")
        # Top of right pane (tabs)
        self.data = ttk.Notebook(master=self.right_pane, height=int(self.HEIGHT * 0.7))
        self.right_pane.add(self.data, stretch="always")
        self.status_tab = controllers.create_widget(
            master=self.data,
            view=views.StatusTab,
            controller=self.statustab_controller,
        )
        self.data.add(self.status_tab, text="Camera State")
        self.ble_tab = ttk.Treeview(master=self.data)
        self.ble_tab.pack(fill=tk.BOTH, expand=True)
        self.data.add(self.ble_tab, text="BLE Info")
        # Bottom of right pane (video).
        self.video = controllers.create_widget(
            master=self.right_pane,
            view=views.Video,
            controller=self.video_controller,
            bd=self.SASH_WIDTH,
            relief=tk.SUNKEN,
        )
        self.right_pane.add(self.video, stretch="always", minsize=700, hide=False)
        self.pack(fill=tk.BOTH, expand=True)

        # Menu bar
        self.menubar = controllers.create_widget(
            master=self.root,  # type: ignore
            view=views.Menubar,
            controller=self.menubar_controller,
        )

        # StatusBar
        self.statusbar = controllers.create_widget(
            master=self,
            view=views.StatusBar,
            controller=self.statusbar_controller,
            height=self.TOOLBAR_HEIGHT,
            bd=self.SASH_WIDTH,
            background="gray",
        )

    async def run(self) -> None:
        """GUI main loop."""
        # Wait to be ready
        while not self.splash_controller.are_models_started:
            await self.splash_controller.update()
            self.splash_log_controller.log_queued_messages(self.splash_log)  # type: ignore
        self.splash_controller.logger.setLevel(logging.CRITICAL)
        self.splash.root.destroy()  # type: ignore

        # Update status bar and start its polling
        self.statusbar_controller.update_status(controllers.StatusBar.Ble.CONNECTED)
        self.statusbar_controller.update_status(controllers.StatusBar.Wifi.CONNECTED)
        self.statustab_controller.poll()

        # Unhide root
        self.root.deiconify()

        # Main loop. Continue until told to quit
        while not self._should_quit:
            self.main_log_controller.log_queued_messages(self.main_log)  # type: ignore
            self.root.update()
            await asyncio.sleep(0)
        self.root.quit()

    def quit(self) -> None:
        """Stop the main loop and exit"""
        self._should_quit = True


async def main() -> None:
    await App().run()


def entrypoint() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    entrypoint()
