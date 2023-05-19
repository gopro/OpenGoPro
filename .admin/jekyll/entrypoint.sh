#!/usr/bin/env bash
# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar  8 23:33:16 UTC 2023

set -e

help() {
    cat <<EOF

Usage: gopro-jekyll [OPTIONS] COMMAND
Use the jekyll infrastructure to build or serve the site.

This expects the source documents to be available (i.e. mountd) at /site

Required positional arguments:
    COMMAND          one of [serve, build] where

Optional arguments:
    -h               Print this Help.
    -p PORT          Port to server jekyll site from. Defaults to 4998
    -u HOST_URL      Set host URL for jekyll site. Defaults to http://localhost:4998/
    -b BASE_URL      Set base URL for jekyll site. Defaults to ""

EOF
}

port=4998
host_url="http://jekyll:4998/"
base_url=\"\"

# Special case to handle help
if [[ $1 == "--help" || $1 == "help" ]]; then
    help
    exit 1
fi

# Parse optional arguments
while getopts "hp:u:b:" option; do
    case ${option} in
    h) # help
        help
        exit 0
        ;;
    p) # port
        port=$OPTARG
        ;;
    u) # host url
        host_url=$OPTARG
        ;;
    b) # base url
        base_url=$OPTARG
        ;;
    \? | :)
        help
        exit 1
        ;;
    esac
done

# Jump to positional arguments
shift $((OPTIND - 1))
if [[ $# < 1 ]]; then
    echo "Missing command parameter" >&2
    help
    exit 1
fi

command=$1

function config() {
    echo "🛠️  Configuring Jekyll site"
    echo "url: ${host_url}" >/_config-temp.yml
    echo "baseurl: ${base_url}" >>/_config-temp.yml
    cat /_config-temp.yml
}

if [[ $command == "serve" ]]; then
    config
    echo "🚦  Serving jekyll site..."
    bundle exec jekyll serve --host 0.0.0.0 --port ${port} --watch --incremental --force_polling --config _config.yml,/_config-temp.yml
elif [[ $command == "build" ]]; then
    config
    echo "🏗️  Building jekyll site..."
    bundle exec jekyll build --config _config.yml,/_config-temp.yml
elif [[ $command == "bash" ]]; then # Special hidden command for devlopment
    echo "Entering bash in container..."
    bash
else
    echo "command $command is not supported"
    help
    exit 1
fi