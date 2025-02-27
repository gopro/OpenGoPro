# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Mar 27 22:05:54 UTC 2024

FROM python:3.11.11

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    # Set env variables
    DEBIAN_FRONTEND=noninteractive \
    # Install
    apt-get install -y \
    gosu \
    wget \
    default-jre-headless \
    protobuf-compiler && \
    # clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN wget https://repo1.maven.org/maven2/pro/streem/pbandk/protoc-gen-pbandk-jvm/0.16.0/protoc-gen-pbandk-jvm-0.16.0-jvm8.jar -O protoc-gen-pbandk
RUN chmod +x protoc-gen-pbandk

COPY . /

RUN pip install -r /requirements.txt

RUN chmod +x /entrypoint.sh

RUN useradd -ms /bin/bash user

ENTRYPOINT [ "/entrypoint.sh" ]
