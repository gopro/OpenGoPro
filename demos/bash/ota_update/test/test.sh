#!/usr/bin/env bash
# test.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Oct 19 15:33:20 UTC 2022

set -e

# Check to see if we need sudo
case "$(uname -sr)" in
Linux*Microsoft*) ;; # WSL does not need sudo
Linux*)
    SUDO=sudo
    ;;
*) ;;
esac

# Handle variable expansion in Windows MSYS / Git Bash
export MSYS_NO_PATHCONV=1

pushd ..
echo "Building Docker image..."
$SUDO docker build -t ota-test -f ./test/Dockerfile .

# Get the test Zip
$SUDO docker run --rm --mount type=bind,source=$(pwd)/test,target=/workdir ota-test $@

if [[ $1 != "--help" && $1 != "-h" ]]; then
    # Now test the script
    ./send_ota.sh -d ./test/UPDATE.zip
fi

popd >/dev/null
