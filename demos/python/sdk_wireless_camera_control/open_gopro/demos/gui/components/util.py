# util.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 23 22:43:52 UTC 2023

"""Common GUI utilities"""

from __future__ import annotations
import queue
import threading
from typing import Callable, Any

import cv2


def display_video_blocking(source: str, printer: Callable = print) -> None:
    """Open a video source to display it, and block until the user stops it by sending 'q'

    Args:
        source (str): video source to display
        printer (Callable): used to display output message. Defaults to print.
    """
    BufferlessVideoCapture(source, printer)


class BufferlessVideoCapture(threading.Thread):
    """Buffer-less video capture to only display the most recent frame

    Open a video source to display it, and block until the user stops it by sending 'q'
    """

    def __init__(self, source: str, printer: Callable = print) -> None:
        """Constructor

        Args:
            source (str): video source to display
            printer (Callable): used to display output message. Defaults to print.
        """
        self.printer = printer
        printer("Starting viewer...")
        self.cap = cv2.VideoCapture(source + "?overrun_nonfatal=1&fifo_size=50000000", cv2.CAP_FFMPEG)
        self.q: queue.Queue[Any] = queue.Queue()
        super().__init__(daemon=True)
        self.start()
        printer("Viewer started")
        printer("Press 'q' in viewer to quit")
        while True:
            frame = self.q.get()
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self) -> None:
        """Read frames as soon as they are available, keeping only most recent one"""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass

            self.q.put(frame)
