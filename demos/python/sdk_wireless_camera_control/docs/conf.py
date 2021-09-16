# conf.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:41 PM

project = "Open GoPro Python SDK"
copyright = "2020, GoPro Inc."
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

import sys
import os

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# Insert the project root dir as the first element in the PYTHONPATH.
# This lets us ensure that the source package is imported, and that its
# version is used.
sys.path.insert(0, project_root)

import open_gopro

# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = open_gopro.__version__
# The full version, including alpha/beta/rc tags.
release = open_gopro.__version__
