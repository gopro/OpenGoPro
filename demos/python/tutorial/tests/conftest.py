# conftest.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jan  5 23:22:13 UTC 2022

import asyncio
import logging
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--ssid", action="store", required=True)
    parser.addoption("--password", action="store", required=True)


##############################################################################################################
#                                             Log Management
##############################################################################################################


@pytest.fixture(scope="class", autouse=True)
def manage_logs(request):
    log_file = Path(request.node.name + ".log")
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(Path(".reports") / "logs" / log_file)


@pytest.fixture(scope="function", autouse=True)
def test_log(request):
    logging.debug("################################################################################")
    logging.debug("Test '{}' STARTED".format(request.node.nodeid))
    logging.debug("################################################################################")


##############################################################################################################
#                                             General
##############################################################################################################


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
