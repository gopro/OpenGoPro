# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

from __future__ import annotations
import re
from datetime import date
from typing import Union, Optional

from darglint.docstring.docstring import Docstring
from darglint.docstring.sections import Sections
from sphinx.ext.napoleon.docstring import GoogleDocstring

from open_gopro import WirelessGoPro
from open_gopro.api.builders import (
    HttpGetBinary,
    HttpGetJsonCommand,
    BleProtoCommand,
    BleWriteCommand,
    BleReadCommand,
    RegisterUnregisterAll,
)
from open_gopro.interface import BleMessage, HttpMessage

gopro = WirelessGoPro(enable_wifi=False)

project = "Open GoPro Python SDK"
copyright = f"{date.today().year}, GoPro Inc."
author = "Tim Camise"

source_suffix = ".rst"
master_doc = "index"
pygments_style = "sphinx"
html_static_path = ["_static"]
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.graphviz",
    "sphinx.ext.inheritance_diagram",
    "sphinxemoji.sphinxemoji",
]
html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
}
add_module_names = False
inheritance_graph_attrs = dict(rankdir="BT", center="true")
inheritance_node_attrs = dict(color="dodgerblue1", style="filled")
autodoc_default_options = {
    "members": True,
}

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("open_gopro")

nitpicky = True

# # TODO why isn't this working?
# autodoc_type_aliases = {
#     "IdType": "open_gopro.interface.IdType",
#     "CommunicatorType": "open_gopro.interface.CommunicatorType",
#     "ParserType": "open_gopro.interface.ParserType",
#     "DisconnectHandlerType": "open_gopro.ble.controller.DisconnectHandlerType",
#     "NotiHandlerType": "open_gopro.ble.controller.NotiHandlerType",
#     "ValueType": "open_gopro.api.builders.ValueType",
#     "BleDevice": "open_gopro.ble.controller.BleDevice",
#     "BleHandle": "open_gopro.ble.controller.BleHandle",
#     "CmdType": "open_gopro.constants.CmdType",
#     "ResponseType": "open_gopro.constants.ResponseType",
# }

nitpick_ignore = [
    ("py:class", "T"),
    ("py:class", "T_co"),
    ("py:class", "ExceptionHandler"),
    ("py:class", "datetime.datetime"),
    ("py:class", "open_gopro.responses.Parser"),
    ("py:class", "InitVar"),
    ("py:class", "abc.ABC"),
    ("py:class", "collections.abc.Iterable"),
]
nitpick_ignore_regex = [
    (r"py:class", r".+Type"),
    (r"py:obj", r".+Type"),
    (r"py:class", r".*Path"),
    (r"py:class", r".*BleDevice"),
    (r"py:class", r".*BleHandle"),
    (r"py:class", r".*JsonParser"),
    (r"py:class", r".*BytesParserBuilder"),
    (r"py:class", r".*BytesParser"),
    (r".*", r".*construct.*"),
]

# This is the expected signature of the handler for this event, cf doc
def autodoc_skip_member_handler(app, what, name, *_):
    for skip in ("internal", "deprecated"):
        if skip in name.lower():
            return name


def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip_member_handler)
