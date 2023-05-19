#!/usr/bin/env bash
# entrypoint.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri May 19 19:39:24 UTC 2023


PORT=4998

# TODO Remove the following once Github actions gets upgraded
# The clean solution is to rely on the health check from the compose file but Github Actions does not yet
# support --wait

# Wait for page to be ready.
echo "⏳ Waiting for server to be ready..."
until curl http://jekyll:${PORT} >/dev/null 2>&1; do
    sleep 1
done

linkchecker \
    --check-extern \
    --ignore-url ".*10\.5\.5\.9.*" \
    --timeout 5 \
    -o csv \
    http://jekyll:${PORT} | tee .link_results.csv

echo "Filtering out errors that are not our fault."
python ./parse_linkchecker_results.py .link_results.csv
