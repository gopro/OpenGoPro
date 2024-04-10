# Protobuf Builder

This is a Docker image to build the [Protobuf](../../protobuf/) files in this repo. It currently only build Python
output but should be used in the future for other languages.

## Usage

It is intended to be used via the [docker compose configuration](../../docker-compose.yml).

First build:

```shell
docker compose build proto-build
```

Then build the protobuf files with:

```shell
docker compose run --rm proto-build
```

The output files will be placed in the [build directory](../../.build/protobuf).
