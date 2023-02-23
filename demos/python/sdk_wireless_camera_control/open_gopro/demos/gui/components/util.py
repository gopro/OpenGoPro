"""Common GUI utilities"""

from __future__ import annotations
from typing import Optional, Callable

import cv2


def display_video_blocking(source: str, printer: Optional[Callable] = print) -> None:
    """Open a video source to display it, and block until the user stops it by sending 'q'

    Args:
        source (str): video source to display
        printer (Optional[Callable], optional): used to display output message. Defaults to print.
    """
    if printer:
        printer("Starting viewer...")
    vid = cv2.VideoCapture(source + "?overrun_nonfatal=1&fifo_size=50000000", cv2.CAP_FFMPEG)
    if printer:
        printer("Viewer started")
        printer("Press 'q' to quit")

    while True:
        ret, frame = vid.read()
        if ret and frame is not None:
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    vid.release()
    cv2.destroyAllWindows()
