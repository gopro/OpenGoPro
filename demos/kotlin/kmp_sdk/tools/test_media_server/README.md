# Test Media Server

This is a test media server to view streams in various protocols using [MediaMtx](https://github.com/bluenviron/mediamtx).

## Usage

Start with

```shell
docker compose up
```

## View Streams

### Stream published from FFMPEG as RTSP (test)

| Stream Type     | URL                                     | Tested With |
| --------------- | --------------------------------------- | ----------- |
| RTSP (TCP)      | rtsp://<IP_ADDR>:8554/test              | VLC         |
| RTSP (UDP/RTP)  | rtsp://<IP_ADDR>:8000/test              |             |
| RTSP (UDP/RTCP) | rtsp://<IP_ADDR>:8001/test              |             |
| HLS             | http://localhost:8888/test              | Chrome      |
| RTMP            | rtmp://localhost/test                   | VLC         |
| SRT             | srt://localhost:8890?streamid=read:test |             |

### Stream published from FFMPEG as RTMP (test2)

| Stream Type     | URL                                      | Tested With |
| --------------- | ---------------------------------------- | ----------- |
| RTSP (TCP)      | rtsp://<IP_ADDR>:8554/test2              | VLC         |
| RTSP (UDP/RTP)  | rtsp://<IP_ADDR>:8000/test2              |             |
| RTSP (UDP/RTCP) | rtsp://<IP_ADDR>:8001/test2              |             |
| HLS             | http://localhost:8888/test2              | Chrome      |
| RTMP            | rtmp://localhost/test2                   | VLC         |
| SRT             | srt://localhost:8890?streamid=read:test2 |             |

## Notes

API access is not working. See [here](https://github.com/bluenviron/mediamtx/discussions/3841).
