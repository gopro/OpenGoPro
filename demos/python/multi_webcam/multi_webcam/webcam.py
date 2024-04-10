# webcam.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Nov 11 20:03:39 UTC 2022

from __future__ import annotations
import json
import enum
import logging
import itertools
import multiprocessing as mp
from typing import Any, Protocol, Optional

import cv2 as cv
import requests

logging.getLogger(__name__)


class SupportsWebcam(Protocol):
    def release(self) -> None:
        ...

    def read(self) -> None:
        ...


class Webcam:
    """The GoPro webcam connected via USB"""

    BASE_IP = "172.2{}.1{}{}.51"
    BASE_ENDPOINT = "http://{ip}:8080/gopro/"

    class Endpoint(enum.Enum):
        WIRELESS_USB_DISABLE = "camera/control/wired_usb?p=0"
        GET_DATE_TIME = "camera/get_date_time"
        GET_WEBCAM_STATUS = "webcam/status"
        START_PREVIEW = "webcam/preview"
        START_WEBCAM = "webcam/start"
        STOP_WEBCAM = "webcam/stop"
        DISABLE_WEBCAM = "webcam/exit"

    class State(enum.IntEnum):
        DISABLED = enum.auto()
        READY = enum.auto()
        LOW_POWER_PREVIEW = enum.auto()
        HIGH_POWER_PREVIEW = enum.auto()

    def __init__(self, serial: str) -> None:
        """Constructor

        Args:
            serial (str): (At least) last 3 digits of GoPro's serial number
        """
        self.ip = self.BASE_IP.format(*serial[-3:])
        self.state = self.State.DISABLED
        self._base_url = self.BASE_ENDPOINT.format(ip=self.ip)

    def _send_http_no_validate(self, endpoint: Webcam.Endpoint, **kwargs) -> requests.Response:
        logging.debug(f"Sending {endpoint.value}: {kwargs}")
        response = requests.get(self._base_url + endpoint.value, params=kwargs)
        logging.debug(f"HTTP return code {response.status_code}")
        logging.debug(json.dumps(response.json(), indent=4))
        return response

    def _send_http(self, endpoint: Webcam.Endpoint, **kwargs) -> requests.Response:
        response = self._send_http_no_validate(endpoint, **kwargs)
        response.raise_for_status()
        return response

    def enable(self) -> None:
        """Prepare the GoPro to be ready to function as a webcam"""
        self._send_http_no_validate(self.Endpoint.WIRELESS_USB_DISABLE)
        self.state = self.State.READY

    def preview(self) -> None:
        """Start the webcam preview"""
        logging.info("Starting preview")
        self._send_http(self.Endpoint.START_PREVIEW)
        self.state = self.State.LOW_POWER_PREVIEW

    def start(
        self, port: Optional[int] = None, resolution: Optional[int] = None, fov: Optional[int] = None
    ) -> None:
        """Start the webcam stream

        Note that the FOV and Resolution param values come from the Open GoPro Spec:
        https://gopro.github.io/OpenGoPro/http#tag/settings

        Args:
            port (Optional[int]): Port to stream to. Defaults to None (will be auto-assigned by the camera).
            resolution (Optional[int]): Resolution to use. Defaults to None (will be auto-assigned by the camera).
            fov (Optional[int]): Field of View to use. Defaults to None (will be auto-assigned by the camera).
        """
        logging.info("Starting webcam")
        params = {}
        for setting, key in zip([port, resolution, fov], ["port", "res", "fov"]):
            if setting is not None:
                params[key] = setting
        self._send_http(self.Endpoint.START_WEBCAM, **params)
        self.state = self.State.HIGH_POWER_PREVIEW
        logging.info("Webcam started successfully")

    def stop(self) -> None:
        """Stop the webcam stream"""
        logging.info("Stopping webcam")
        self._send_http(self.Endpoint.STOP_WEBCAM)
        self.state = self.State.READY

    def disable(self) -> None:
        """Disable the webcam"""
        logging.info("Disabling webcam")
        self._send_http(self.Endpoint.DISABLE_WEBCAM)
        self.state = self.State.DISABLED


class Player:
    """The Webcam Stream Viewer via Open CV

    Note that each player runs in a separate process.
    """

    def __init__(self) -> None:
        """Constructor"""
        self._vid: SupportsWebcam
        self._process = mp.Process(target=self._run, daemon=True)
        self._player_started = mp.Event()
        self._stop_player = mp.Event()
        self._url: str

    @property
    def is_running(self) -> bool:
        """Is the player currently running?

        Returns:
            bool: True if yes, False if no
        """
        return self._player_started.is_set()

    @property
    def url(self) -> str:
        """The URL that is being used to view the stream (minus any OpenCV args)

        Returns:
            str: stream URL
        """
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        if self.is_running:
            raise RuntimeError("Can not set URL while player is running")
        self._url = url

    def _run(self) -> None:
        """The main stream display loop.

        While the player is running, get a frame and display it
        """
        self._vid = cv.VideoCapture(self.url + "?overrun_nonfatal=1&fifo_size=50000000", cv.CAP_FFMPEG)
        self._player_started.set()
        logging.info("Player started.")
        while not self._stop_player.is_set():
            ret, frame = self._vid.read()
            if ret:
                cv.imshow("frame", frame)
            cv.waitKey(1)  # Show for 1 millisecond
        # After the loop release the cap object
        self._vid.release()
        # Destroy all the windows
        cv.destroyAllWindows()

    def start(self, url: str) -> None:
        """Start the stream player

        Args:
            url (str): URL to view stream at
        """
        logging.info(f"Starting player @ {url}")
        self.url = url
        self._process.start()
        self._player_started.wait()

    def stop(self) -> None:
        """Stop the stream player and wait for the process to stop"""
        if self.is_running:
            logging.info("Stopping player")
            self._stop_player.set()
            self._process.join()


class GoProWebcamPlayer:
    """Configure and view a GoPro webcam stream

    This is the top level class that will both configure the GoPro via HTTP and start the Open CV stream
    to display frames received from the GoPro.

    It also manages the ports used across multiple GoPros to ensure there are no overlaps.
    """

    STREAM_URL = "udp://0.0.0.0:{port}"
    _used_ports: set[int] = set()
    _free_port: itertools.count[int] = itertools.count(start=8554)

    @classmethod
    def _get_free_port(cls) -> int:
        """Find a port that is not currently being used.

        Returns:
            int: available port
        """
        while (port := next(cls._free_port)) in cls._used_ports:
            continue
        return port

    def __init__(self, serial: str, port: Optional[int] = None) -> None:
        """Constructor

        Args:
            serial (str): (at least) last 3 digits of GoPro's serial number
            port (Optional[int], optional): Port that GoPro will stream to. Defaults to
                None (will be auto-assigned starting at 8554).

        Raises:
            RuntimeError: The desired port is already used.
        """
        self.serial = serial
        self.webcam = Webcam(serial)
        self.player = Player()
        if port and port in GoProWebcamPlayer._used_ports:
            raise RuntimeError(f"Port {port} is already being used")
        self.port = port or GoProWebcamPlayer._get_free_port()
        GoProWebcamPlayer._used_ports.add(self.port)
        logging.debug(f"Using port {self.port}")

    def __enter__(self) -> GoProWebcamPlayer:
        self.open()
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def open(self) -> None:
        """Enable the GoPro webcam."""
        self.webcam.enable()

    def play(self, resolution: Optional[int] = None, fov: Optional[int] = None) -> None:
        """Configure and start the GoPro Webcam. Then open and display the stream.

        Note that the FOV and Resolution param values come from the Open GoPro Spec:
        https://gopro.github.io/OpenGoPro/http#tag/settings

        Args:
            resolution (Optional[int]): Resolution for webcam stream. Defaults to None (will be assigned by GoPro).
            fov (Optional[int]): Field of view for webcam stream. Defaults to None (will be assigned by GoPro).
        """
        self.webcam.start(self.port, resolution, fov)
        self.player.start(GoProWebcamPlayer.STREAM_URL.format(port=self.port))

    def close(self) -> None:
        """Stop the stream player and disable the GoPro webcam"""
        self.player.stop()
        self.webcam.disable()
