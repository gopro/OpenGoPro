# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri May 19 19:39:24 UTC 2023

FROM python:3.10-alpine

RUN apk add --no-cache \
    git \
    curl \
    bash

RUN pip install git+https://github.com/linkchecker/linkchecker.git@v10.2.1

WORKDIR /workdir
COPY entrypoint.sh ./entrypoint.sh
COPY parse_linkchecker_results.py ./parse_linkchecker_results.py

ENTRYPOINT [ "/workdir/entrypoint.sh" ]
