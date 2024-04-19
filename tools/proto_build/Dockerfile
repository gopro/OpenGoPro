# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:54 UTC 2024

FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    bash

COPY . /workdir
RUN pip install -r /workdir/requirements.txt

RUN chmod +x /workdir/entrypoint.sh

ENTRYPOINT [ "/workdir/entrypoint.sh" ]
