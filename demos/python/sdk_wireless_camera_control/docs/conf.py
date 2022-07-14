# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

import inspect
from datetime import date

from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

import open_gopro.api.params as Params

project = "Open GoPro Python SDK"
copyright = f"{date.today().year}, GoPro Inc."
author = "Tim Camise"

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
pygments_style = "sphinx"
html_static_path = ["_static"]
extensions = [
    "sphinx.ext.autodoc",
    "sphinxcontrib.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
]
html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
}

# TODO why doesn't this work?
# autodoc_type_aliases = {
#     "ExceptionHandler": "open_gopro.exceptions.ExceptionHandler",
#     "ResponseType": "constants.ResponseType",
# }

nitpicky = True
nitpick_ignore = [
    ("py:class", "InitVar"),
    ("py:class", "ExceptionHandler"),
    ("py:class", "ResponseType"),
    ("py:class", "CmdType"),
]
nitpick_ignore_regex = [
    (r"py:class", r".*Path"),
    (r"py:class", r".*GoProBle.*"),
    (r"py:class", r".*GoProWifi.*"),
    (r".*", r".*construct.*"),
    (r"py:class", r".*SettingValueType"),
]

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("open_gopro")
