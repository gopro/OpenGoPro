# test_x_runlast_demos.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Sep 15 23:48:50 UTC 2021

import pytest

from pathlib import Path

from tests import cameras
from open_gopro.demos.photo import main as photo_demo


@pytest.mark.parametrize("camera", list(cameras.keys()))
def test_photo_demo(camera):
    print("Testing photo demo")
    assert (
        photo_demo(
            identifier=cameras[camera],
            log_location=Path("reports") / "logs" / "e2e" / "test_photo_demo.log",
            output_location=Path(".") / "photo.jpg",
        )
        == 0
    )
