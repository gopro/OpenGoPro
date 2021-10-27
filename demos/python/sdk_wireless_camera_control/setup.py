# setup.py/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:05:52 PM

"""Package definition"""

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.

NAME = "open_gopro"
DESCRIPTION = "Open GoPro API and Examples"
URL = "https://gopro.github.io/OpenGoPro/python_sdk/"
EMAIL = "tcamise@gopro.com"
AUTHOR = "Tim Camise"

TEST_REQUIRED = ["pytest", "pytest-cov", "pytest-asyncio", "pytest-html"]

REQUIRED = [
    "bleak==0.12.1",
    "construct>=2.10",
    "wrapt>=1.12.1",
    "requests",
    "rich",
    "protobuf>=3",
    "betterproto",
    "typing-extensions",
]

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, NAME, "__version__.py")) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s: str):
        """Prints things in bold

        Args:
            s (str): Thing to print
        """
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=("tests", "examples", "docs")),
    entry_points={
        "console_scripts": [
            "gopro-demo=open_gopro.demos.demo:main",
            "gopro-photo=open_gopro.demos.photo:entrypoint",
            "gopro-video=open_gopro.demos.video:main",
            "gopro-stream=open_gopro.demos.stream:main",
            "gopro-log-battery=open_gopro.demos.log_battery:main",
            "gopro-wifi=open_gopro.demos.connect_wifi:main",
            "gopro-ble-write=open_gopro.demos.ble_write:main",
        ]
    },
    install_requires=REQUIRED,
    test_suite="tests",
    tests_require=TEST_REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Developers",
        "Topic :: Communications",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
