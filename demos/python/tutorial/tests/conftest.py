import asyncio
import logging
from pathlib import Path

import pytest


##############################################################################################################
#                                             Log Management
##############################################################################################################


@pytest.fixture(scope="class", autouse=True)
def manage_logs(request):
    log_file = Path(request.node.name + ".log")
    request.config.pluginmanager.get_plugin("logging-plugin").set_log_path(Path("reports") / "logs" / log_file)


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
