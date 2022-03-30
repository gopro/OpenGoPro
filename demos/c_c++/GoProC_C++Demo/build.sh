#! /bin/bash
# build.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Feb  8 01:22:35 UTC 2022

set -e
cd "$(dirname "$0")"

# Verify Prerequisites
if ! command -v cmake &>/dev/null; then
    echo "cmake can not be found."
    echo "Please install: https://cmake.org/install/"
    exit
fi

CONAN="python3 -m conans.conan"
if ! $CONAN --version &>/dev/null; then
    echo "conan can not be found."

    if ! command -v python3 &>/dev/null; then
        echo "Please install: https://docs.conan.io/en/latest/installation.html"
        exit
    else
        echo "Trying to install conan with discovered python3"
        pip3 install conan
    fi
fi

# Install Conan packages
mkdir -p build
cd build
$CONAN install .. --build=missing

if [ "$(uname)" == "Darwin" ]; then
    cmake -DCMAKE_BUILD_TYPE=Release ..
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    cmake -DCMAKE_BUILD_TYPE=Release ..
else # Windows. Force to 64 bit.
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_GENERATOR_PLATFORM=x64 ..
fi

cmake --build . --config Release
