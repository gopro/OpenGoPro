# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:11 PM

FROM python:3.10.10

RUN apt-get update && apt-get install -y \
    fswatch

# Install our python tool
COPY . /tools
RUN pip install /tools

WORKDIR /demos

# Default to just enter image in bash. Should be overriden in container definition in docker-compose.yml
ENTRYPOINT [ "/tools/entrypoint.sh" ]
