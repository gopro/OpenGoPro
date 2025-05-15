# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

from __future__ import annotations
from datetime import date
import sys

import sphinx
from open_gopro import WirelessGoPro

from open_gopro.network.wifi.controller import SsidState, WifiController

# Workaround for https://github.com/sphinx-doc/sphinx/issues/13178 in Python 3.13
if sys.version_info[:2] >= (3, 13) and sphinx.version_info[:2] < (8, 2):
    import pathlib

    from sphinx.util.typing import _INVALID_BUILTIN_CLASSES

    _INVALID_BUILTIN_CLASSES[pathlib.Path] = "pathlib.Path"  # type: ignore


class MockWifiController(WifiController):
    def connect(self, ssid: str, password: str, timeout: float = 15) -> bool:
        return True

    def disconnect(self) -> bool:
        return True

    def current(self) -> tuple[str | None, SsidState]:
        return ("mocked", SsidState.CONNECTED)

    def available_interfaces(self) -> list[str]:
        return []

    def power(self, power: bool) -> bool:
        return True

    @property
    def is_on(self) -> bool:
        return True


gopro = WirelessGoPro(enable_wifi=False, wifi_adapter=MockWifiController)

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
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.intersphinx",
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
# https://autodoc-pydantic.readthedocs.io/en/stable/users/configuration.html
autodoc_pydantic_model_show_json = False
autodoc_pydantic_settings_show_json = False
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("open_gopro")

nitpicky = True

TYPE_ALIASES = {
    "CameraState": "open_gopro.models.types.CameraState",
    "UpdateCb": "open_gopro.models.types.UpdateCb",
    "UpdateType": "open_gopro.models.types.UpdateType",
    "JsonDict": "open_gopro.JsonDict",
    "ResponseType": "open_gopro.models.types.ResponseType",
    "Protobuf": "open_gopro.models.types.Protobuf",
    "IdType": "open_gopro.models.types.IdType",
    "StreamOptions": "open_gopro.models.types.StreamOptions",
    "SyncAction": "open_gopro.observable.SyncAction",
    "AsyncAction": "open_gopro.observable.AsyncAction",
    "SyncFilter": "open_gopro.observable.SyncFilter",
    "AsyncFilter": "open_gopro.observable.AsyncFilter",
}

nitpick_ignore = [
    ("py:class", "T"),
    ("py:class", "O"),
    ("py:class", "T_I"),
    ("py:class", "I"),
    ("py:class", "T_co"),
    ("py:class", "ExceptionHandler"),
    ("py:class", "abc.ABC"),
    ("py:class", "InitVar"),
    ("py:class", "Result"),
    ("py:class", "ResultE"),
    ("py:class", "returns.result.Result"),
    ("py:class", "TracebackType"),
    ("py:class", "UUID"),
    ("py:class", "Path"),
    ("py:class", "JsonDict"),
    ("py:class", "SyncAction"),
    ("py:class", "AsyncAction"),
    ("py:class", "SyncFilter"),
    ("py:class", "AsyncFilter"),
    ("py:class", "ValueType"),
]
nitpick_ignore_regex = [
    (r"py:class", r".*proto\..+"),
    (r"py:class", r".*_pb2\..+"),
    (r".*", r".*construct.*"),
    (r"py:class", r".*TinyDB.*"),
    (r"py:class", r".*asyncio.*"),
    (r"py:class", r".*WirelessApi*"),
    # Generic Types that are pointless to document
    (r"py:class", r".*\.T"),
    (r"py:class", r".*\.T_I"),
    (r"py:class", r".*\.O"),
    (r"py:class", r".*\.I"),
    (r"py:obj", r".*\.T_I"),
    (r"py:obj", r".*\.O"),
    (r"py:obj", r".*\.I"),
    (r"py:obj", r".*\.T"),
    (r"py:class", r".*\.T_co"),
    (r"py:class", r".*BleHandle"),
    (r"py:class", r".*BleDevice"),
    (r"py:class", r".*CommunicatorType"),
    (r"py:class", r".*NotiHandlerType"),
    (r"py:class", r".*DisconnectHandlerType"),
    (r"py:obj", r".*CommunicatorType"),
    (r"py:class", r".*QueryParserType"),
    (r"py:class", r".*ValueType"),
    (r"py:obj", r".*communicator_interface.MessageType"),
    (r"py:class", r".*dataclasses.*"),
    (r"py:class", r".*BaseGoProCommunicator._CompositeRegisterType.*"),
]


def autodoc_skip_member_handler(app, what, name, *_):
    for skip in ("internal", "deprecated"):
        if skip in name.lower():
            return name


def resolve_type_aliases(app, env, node, contnode):
    """Resolve :class: references to our type aliases as :attr: instead."""
    try:
        if node["refdomain"] == "py" and (target := TYPE_ALIASES.get(node["reftarget"])):
            # print(f"updating {node['reftarget']}")
            return app.env.get_domain("py").resolve_any_xref(
                env,
                node["refdoc"],
                app.builder,
                target,
                node,
                contnode,
            )[
                0
            ][1]
    except IndexError:
        # print("Error")
        return None


def setup(app):
    app.connect("autodoc-skip-member", autodoc_skip_member_handler)
    app.connect("missing-reference", resolve_type_aliases)
