#!/usr/bin/env bash
# send_ota.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Oct 19 15:33:20 UTC 2022

set -e

BASE_URL=http://10.5.5.9:8080
USE_DOCKER=false
FILE=
POLLING_PERIOD_SEC=0.500

help() {
    cat <<EOF
Usage: $0 [-d] OTA_UPDATE_FILE

Given a target FW .zip file, calculate its SHA1 hash, then send it over-the-air to an already connected camera.
Required positional arguments:
    OTA_UPDATE_FILE  target .zip file to send over-the-air. If using docker, must be passed as relative path
                     from the directory of this script
Optional arguments:
    -d               Use docker for openssl and curl commands.
    -h               Print this Help.

EOF
}

##############################################################################################################
#                          Argument parsing and Setup
##############################################################################################################

# Parse optional arguments
while getopts "hd" option; do
    case ${option} in
    h) #For option h (help)
        help
        exit 0
        ;;
    d) #For option d (use docker)
        USE_DOCKER=true
        ;;
    \? | :)
        echo
        help
        exit 1
        ;;
    *)
        echo "Unexpected error occurred." >&2
        help
        exit 1
        ;;
    esac
done

# Jump to positional arguments and parse
shift $((OPTIND - 1))
if [[ $# < 1 ]]; then
    echo "ERROR: Missing OTA_UPDATE_FILE argument" >&2
    echo
    help
    exit 1
fi
FILE="$1"
if [ ! -f "$FILE" ]; then
    echo "ERROR: Cannot find file: \"$FILE\""
    echo
    help
    exit 1
fi

# Configure curl and openssl commands to be native or docker
IN_FILE="$FILE" # Store original file name since it might change if using Docker (to the docker image absolute path)
if $USE_DOCKER; then
    # Check to see if we need sudo
    case "$(uname -sr)" in
    Linux*Microsoft*) ;; # WSL does not need sudo
    Linux*)
        SUDO=sudo
        ;;
    *) ;;
    esac

    export MSYS_NO_PATHCONV=1 # Handle variable expansion in Windows MSYS / Git Bash
    DOCKER_BASE_CMD="$SUDO docker run --rm --mount type=bind,source=$(pwd)/$IN_FILE,target=/test_image"
    OPENSSL="$DOCKER_BASE_CMD alpine/openssl"
    CURL="$DOCKER_BASE_CMD curlimages/curl"
    FILE="/test_image"
else
    OPENSSL="openssl"
    CURL="curl"
fi

##############################################################################################################
#                          Local Functions
##############################################################################################################

function log() {
    echo
    echo =====================================================================================================
    echo $1
}

# Get the camera statuses and extract status 8 (System Busy)
# Return 1 (busy) or 0 (not busy)
function is_system_busy {
    $CURL -s "$BASE_URL/gopro/camera/state" |
        grep -v 'settings' |
        grep -o '\"8\":[0-9]\+' |
        cut -d':' -f'2'
}

# Takes curl parameters as input. Then performs the curl command, validates the return, and reads the Busy
# status until the camera is ready
# Exits with error 1 if curl command fails
function curl_validate_pend() {
    # Send command and check error code
    if ! $CURL "$@"; then
        echo "❌ Error!! Command failed. ❌"
        exit 1
    fi

    # Wait for system to be ready for next command
    while [ "$(is_system_busy)" = '1' ]; do
        sleep $POLLING_PERIOD_SEC
    done
}

##############################################################################################################
#                          Main script
##############################################################################################################

echo "Calculating SHA1 hash of file: $IN_FILE..."
sha1_hash=$($OPENSSL dgst -sha1 -hex "$FILE" | sed 's|.*= \(.*\)|\1|g')
if [ $? -ne 0 ]; then
    echo "ERROR: Unable to get sha1 digest from file: \"$IN_FILE\""
    exit 1
fi
echo "SHA1 is $sha1_hash"

log "Deleting any partially stored OTA data..."
curl_validate_pend "$BASE_URL/gp/gpSoftUpdate?request=delete"

log "Showing OTA update UI..."
curl_validate_pend "$BASE_URL/gp/gpSoftUpdate?request=showui"

log "Sending $IN_FILE to the camera..."
curl_validate_pend "$BASE_URL/gp/gpSoftUpdate" \
    -X POST \
    -H "Content-Type: multipart/form-data" \
    -F "sha1=$sha1_hash" \
    -F "offset=0" \
    -F "file=@$FILE"

log "Notifying camera that transfer is complete..."
curl_validate_pend "$BASE_URL/gp/gpSoftUpdate" \
    -X POST \
    -H "Content-Type: multipart/form-data" \
    -F "sha1=$sha1_hash" \
    -F "complete=true"

log "Notifying camera that it should start loading the new firmware..."
curl_validate_pend "$BASE_URL/gp/gpSoftUpdate?request=start"

log "👍 Image has been transferred succesfully! The camera will now apply the firmware update."
exit 0
