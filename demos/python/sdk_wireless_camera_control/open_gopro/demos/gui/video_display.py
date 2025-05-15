# util.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu Feb 23 22:43:52 UTC 2023

"""Common GUI utilities"""

from __future__ import annotations

import enum
import logging
import queue
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable

import cv2

logger = logging.getLogger(__name__)


class StreamReader(ABC):
    """Stream Reader interface"""

    def __init__(self, source: str) -> None:
        self.source = source

    @abstractmethod
    def read(self) -> tuple[bool, Any]:
        """Read a frame from the stream

        Returns:
            tuple[bool, Any]: (success, frame)
        """

    @abstractmethod
    def display_frame(self, frame: Any) -> None:
        """Display a frame

        Args:
            frame (Any): frame to display
        """

    @abstractmethod
    def close(self) -> None:
        """Close the stream and release resources"""


class TsStreamReader(StreamReader):
    """Stream reader for TS streams

    Args:
        source (str): URL to read stream from
    """

    def __init__(self, source: str) -> None:
        super().__init__(source)
        self.cap = cv2.VideoCapture(source + "?overrun_nonfatal=1&fifo_size=50000000", cv2.CAP_FFMPEG)

    def read(self) -> tuple[bool, Any]:  # noqa
        return self.cap.read()

    def display_frame(self, frame: Any) -> None:  # noqa
        cv2.imshow(f"TS Stream from {self.source}", frame)

    def close(self) -> None:  # noqa
        self.cap.release()


class RtspStreamReader(StreamReader):
    """Stream reader for RTSP streams

    Args:
        source (str): URL to read stream from
    """

    def __init__(self, source: str) -> None:
        super().__init__(source)
        # TODO what arguments here?
        self.cap = cv2.VideoCapture(source)

    def read(self) -> tuple[bool, Any]:  # noqa
        return self.cap.read()

    def display_frame(self, frame: Any) -> None:  # noqa
        cv2.imshow(f"RTSP stream from {self.source}", frame)

    def close(self) -> None:  # noqa
        self.cap.release()


class BufferlessVideoCapture:
    """Buffer-less video capture to only display the most recent frame

    Open a video source to display it, and block until the user stops it by sending 'q'

    Args:
        source (str): video source to display
        protocol (Protocol): protocol to use to create the stream reader.
        printer (Callable): used to display output message. Defaults to print.
    """

    class Protocol(enum.Enum):
        """Stream Protocol"""

        RTSP = "RTSP"
        TS = "TS"

    def __init__(
        self,
        source: str,
        protocol: Protocol,
        printer: Callable = print,
    ) -> None:
        self._receive_thread = threading.Thread(
            target=self._read_frames,
            daemon=True,
            name="BufferlessVideoCaptureReceiveThread",
        )
        self.printer = printer
        self.printer(f"Starting viewer at {source}...")
        logger.debug(f"Starting viewer at {source}...")
        self._q: queue.Queue[Any] = queue.Queue()
        self._reader = TsStreamReader(source) if protocol == self.Protocol.TS else RtspStreamReader(source)
        # Start reading thread
        self._receive_thread.start()
        # TODO clean up thread on exit

    def display_blocking(self) -> None:
        """Display the stream, blocking, until the user stops it by sending 'q'"""
        self.printer("Viewer started")
        self.printer("Press 'q' in viewer to quit")
        while True:
            try:
                frame = self._q.get()
                self._reader.display_frame(frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.warning(e)
                break
        self._reader.close()
        cv2.destroyAllWindows()

    def _read_frames(self) -> None:
        """Read frames as soon as they are available, keeping only most recent one"""
        while True:
            try:
                ret, frame = self._reader.read()
                if not ret:
                    # logger.debug("Received empty frame.")
                    continue
                if not self._q.empty():
                    self._q.get_nowait()  # discard previous (unprocessed) frame
                self._q.put(frame)
            except queue.Empty:
                pass
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error(f"Video capture received exception: {repr(e)}, stopping capture.")
                break
