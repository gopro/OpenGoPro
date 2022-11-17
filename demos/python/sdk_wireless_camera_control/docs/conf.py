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
    HttpCommand,
    RegisterUnregisterAll,
    BleCommand,
)

DEBUG = False

gopro = WirelessGoPro(enable_wifi=False)

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
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
    "sphinx.ext.autosectionlabel",
]
html_theme = "sphinx_rtd_theme"
html_context = {
    "display_github": True,
}
add_module_names = False

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

# Extract version set from pyproject.toml
import importlib.metadata as importlib_metadata

version = importlib_metadata.version("open_gopro")

# Why aren't these working? Was it because they are are not included from api.rst?
# autodoc_type_aliases = {
#     "ExceptionHandler": "open_gopro.exceptions.ExceptionHandler",
#     "ResponseType": "constants.ResponseType",
# }

nitpicky = True
nitpick_ignore = [
    ("py:class", "T"),
    ("py:class", "T_co"),
    ("py:class", "ExceptionHandler"),
    ("py:class", "datetime.datetime"),
    ("py:class", "open_gopro.responses.Parser"),
]
nitpick_ignore_regex = [
    (r"py:class", r".+Type"),
    (r"py:class", r".*Path"),
    (r"py:class", r".*GoProBle.*"),
    (r"py:class", r".*GoProWifi.*"),
    (r"py:class", r".*JsonParser"),
    (r"py:class", r".*BytesParserBuilder"),
    (r"py:class", r".*BytesParser"),
    (r".*", r".*construct.*"),
]


def debug_print(*args) -> None:
    if DEBUG:
        print(*args)


def get_command_from_name(name: str) -> Optional[Union[BleCommand, WifiCommand]]:
    cls_attr_to_instance_prop = dict(
        BleStatuses="ble_status",
        BleSettings="ble_setting",
        BleCommands="ble_command",
        WifiSettings="wifi_setting",
        WifiCommands="wifi_command",
    )

    debug_print("==============================", name)
    try:
        if len(subcommand := name.split(".")) > 2:
            attr, method = subcommand[-2:]
            return eval(f"gopro.{cls_attr_to_instance_prop[attr]}.{method}")
    except (AttributeError, KeyError) as e:
        return None


def on_autodoc_process_docstring(app, what, name, obj, options, lines):
    """Redirect docstring from class method to instance attribute for commands

    Note that, per autodoc, lines is modified in place

    See https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-signature
    """
    if isinstance(
        command := get_command_from_name(name),
        (BleWriteCommand, BleProtoCommand, WifiGetJsonCommand, WifiGetBinary),
    ) and (docstring := type(command).__call__.__doc__):
        lines[:] = GoogleDocstring(docstring, app.config, app, what, name, obj, options).lines()[:]


def on_autodoc_process_signature(app, what, name, *_) -> Optional[tuple[str, str]]:
    """Modify an object's function signature

    Used to redirect command docstrings from a class's __call__ method to an instance attribute.

    See https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-process-signature
    """
    try:
        # Any command except for register / unregister all and direct reads
        if isinstance(command := get_command_from_name(name), (BleCommand, WifiCommand)) and not isinstance(
            command, (RegisterUnregisterAll, BleReadCommand)
        ):
            debug_print(command)
            # Get the __call__ docstring of the attribute's class type
            docstring: str = type(command).__call__.__doc__
            if not docstring:
                raise RuntimeError(f"{command} missing docstring")
            debug_print(docstring)
            # Remove all prepended whitespace before section labels
            match_labels = re.compile(r"^[^\S\r\n]+(?=Args:|Returns:|Raises:)", flags=re.MULTILINE)
            docstring = re.sub(match_labels, "", docstring)
            # Deindent everything else to one tab (needs to be whitespace)
            match_indents = re.compile(r"^[^\S\r\n]+", flags=re.MULTILINE)
            docstring = re.sub(match_indents, "    ", docstring)
            # Remove trailing whitespace
            docstring = docstring.strip(" ")
            # Use darglint to parse docstring to gather params signature part
            d = Docstring.from_google(docstring)
            args = ""
            if (params := d.get_items(Sections.ARGUMENTS_SECTION)) and (
                param_types := d._get_argument_types()
            ):
                for param, param_type in zip(params, param_types):
                    args += f"{param}: {param_type}, "
            args = args.strip(", ")
            # Build signature
            # TODO can we find a way to show empty parentheses if no args. Currently '' produces no parentheses
            ret = (f"({args or ''})", d._get_return_type())
            debug_print(ret)
            return ret
    except Exception as e:
        debug_print(repr(e))
        raise e


def setup(app):
    app.connect("autodoc-process-docstring", on_autodoc_process_docstring)
    app.connect("autodoc-process-signature", on_autodoc_process_signature)
