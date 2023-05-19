#!/usr/bin/env bash
# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri May 19 19:39:24 UTC 2023


function build_demos() {
    pushd /demos >/dev/null
    prepare-demos "/demos" "/site/_demos"
    popd >/dev/null
}

echo "📇 Building demo documentation..."
build_demos

function watch_demos() {
    echo "Watching for demo changes..."
    fswatch -r -m poll_monitor /demos/* |
        while read event; do
            if [[ $event == *.md ]]; then
                echo "fswatch: 📇 Rebuilding demo docs..."
                build_demos
                echo "fswatch: Done"
            fi
        done
}

if [[ -z "$@" ]]; then
    watch_demos
else
    watch_demos &
    echo "Running $@"
    exec "$@"
fi
