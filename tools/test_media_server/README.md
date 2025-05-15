- [What is this?](#what-is-this)
- [Usage](#usage)
  - [SSL Configuration](#ssl-configuration)
- [Test Stream](#test-stream)
  - [RTMP](#rtmp)
  - [~~RTMPS~~](#rtmps)
- [More Information](#more-information)

# What is this?

This is a test server that can used for isolated testing of the following streams:

-   RTMP
-   ~~RTMPS~~

> Note! RTMPS functionality is not currently working as indicated by strike-throughs below

# Usage

Start server with:

```
SSL_DOMAIN="{IP_ADDRESS}" docker compose up
```

where `IP_ADDRESS` is the IP Address of the device the server is running on.

The server accepts communication on the following endpoints / ports:

| Port     | Endpoint      | Communication Type     | Example                                 |
| -------- | ------------- | ---------------------- | --------------------------------------- |
| 8080     |               | HLS stream viewer      | http://{IP_ADDRESS}:8080                |
| 8080     | stats         | stream stats via HTTP  | http://{IP_ADDRESS}:8080/stats          |
| 8443     | stats         | stream stats via HTTPS | https://{IP_ADDRESS}:8443/stats         |
| 1935     | live/test     | RTMP stream            | rtmp://{IP_ADDRESS}:1935/live/test      |
| ~~1936~~ | ~~live/test~~ | ~~RTMPS stream~~       | ~~rtmps://{IP_ADDRESS}:1936/live/test~~ |

The general usage is:

1. Start an RTMP(S) stream to one of the `live/test` endpoints.
2. View stream with at port 8080 (`http://{IP_ADDRESS}:8080`)
3. Optionally check stats at one of the stats endpoints

## SSL Configuration

A certificate and key are generated when docker image starts and placed in the `.ssl` directory.

To use this certificate to communicate with the test server, install `rtmp.crt` as trusted root certificate.
The steps for this vary per OS. On Ubuntu for example:

```
$ sudo cp ./.ssl/self-signed/rtmp.crt /usr/local/share/ca-certificates
$ sudo update-ca-certificates
```

# Test Stream

For sanity testing, an RTMP(S) stream can be sent to the test server as follows:

## RTMP

1. Test via:

```
docker run --rm jrottenberg/ffmpeg:4.1-alpine -r 30 -f lavfi -i testsrc -vf scale=1280:960 -vcodec libx264 -profile:v baseline -pix_fmt yuv420p -f flv rtmp://{IP_ADDRESS}:1935/live/test
```

2. View at: http://localhost:8080

## ~~RTMPS~~

~~1. Test via:~~


```
docker run --rm jrottenberg/ffmpeg:4.1-alpine -r 30 -f lavfi -i testsrc -vf scale=1280:960 -vcodec libx264 -profile:v baseline -pix_fmt yuv420p -f flv rtmps://{IP_ADDRESS}:1936/live/test
```

~~2. View at: http://localhost:8080~~

# More Information

Per-stream stats can be viewed at `http://localhost:8080/stats`. The `.xml` provided by this endpoint could,
for example, be used as a programmatic way to verify a stream has started / stopped.