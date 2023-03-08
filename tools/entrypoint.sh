#!/usr/bin/env bash
# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar  8 23:33:16 UTC 2023


echo "📚 Preparing demos..."

if ! prepare-demos; then
    exit 1
fi

exec "$@"
