# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

from datetime import date

import open_gopro

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

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.

version = release = open_gopro.__version__
