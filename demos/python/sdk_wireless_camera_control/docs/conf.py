# conf.py/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

project = "Open GoPro Python SDK"
copyright = "2020, GoPro Inc."
author = "Tim Camise"
version = "0.5.5"
release = "0.5.5"
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