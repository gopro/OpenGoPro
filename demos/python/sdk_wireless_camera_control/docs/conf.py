# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

from __future__ import annotations
from datetime import date

from open_gopro import WirelessGoPro

from sphinx.ext.intersphinx import missing_reference

import open_gopro.models

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

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("open_gopro")

nitpicky = True

TYPE_ALIASES = {
    "CameraState": "open_gopro.types.CameraState",
    "UpdateCb": "open_gopro.types.UpdateCb",
    "UpdateType": "open_gopro.types.UpdateType",
    "JsonDict": "open_gopro.JsonDict",
    "ResponseType": "open_gopro.types.ResponseType",
    "Protobuf": "open_gopro.types.Protobuf",
    "IdType": "open_gopro.types.IdType",
    # TODO there must be a better way of doing this...
    "Params.Toggle": "open_gopro.api.params.Toggle",
    "Params.CameraControl": "open_gopro.api.params.CameraControl",
    "Params.WebcamProtocol": "open_gopro.api.params.WebcamProtocol",
    "Params.WebcamResolution": "open_gopro.api.params.WebcamResolution",
    "Params.WebcamFOV": "open_gopro.api.params.WebcamFOV",
}

# This is very broken.
# https://github.com/sphinx-doc/sphinx/issues/10455
# https://github.com/sphinx-doc/sphinx/issues/10785
# autodoc_type_aliases = {
# "CameraState": "open_gopro.types.CameraState",
# "Path": "pathlib.Path",
# }

nitpick_ignore = [
    ("py:class", "T"),
    ("py:class", "T_co"),
    ("py:class", "ExceptionHandler"),
    ("py:class", "abc.ABC"),
    ("py:class", "InitVar"),
    # TODO need to fix these
    ("py:class", "Path"),
    ("py:class", "JsonDict"),
    ("py:class", "ValueType"),
]
nitpick_ignore_regex = [
    (r"py:class", r".*proto\..+"),
    (r"py:class", r".*_pb2\..+"),
    (r".*", r".*construct.*"),
    # Generic Types that are pointless to document
    (r"py:class", r".*\.T"),
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
