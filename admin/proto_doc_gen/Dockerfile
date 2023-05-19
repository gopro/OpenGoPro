FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    fswatch \
    wget \
    protobuf-compiler

WORKDIR /bin

# Install protoc-gen-doc
RUN wget -c https://github.com/pseudomuto/protoc-gen-doc/releases/download/v1.5.1/protoc-gen-doc_1.5.1_linux_amd64.tar.gz -O - | tar -xz

COPY entrypoint.sh /bin/entrypoint.sh

WORKDIR /protos

# Default to just enter image in bash. Should be overriden in container definition in docker-compose.yml
ENTRYPOINT [ "/bin/entrypoint.sh" ]
