#!/usr/bin/env bash
# start_rtmp_server.sh/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jul  6 19:59:53 UTC 2022


docker kill rtmp-server >/dev/null 2>&1
docker run --rm --detach -p 1935:1935 --name rtmp-server tiangolo/nginx-rtmp
echo "rtmp-server Docker container running"
echo "Access the livestream at rtmp://<IPADDR>/live/test"
echo
echo "where <IPADDR> the IP address of the adapter where the container is running"
