# CORS NGINX Docker Proxy

## What is this?

This is a simple [NGINX](https://www.nginx.com/) docker server to
remove [CORS headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) from HTTP requests to a GoPro camera.
This proxy accepts input on port 8082 and forwards it to `http:10.5.5.9:8080`

## How do I use it?

It is intended to be run using the `docker-compose.yml` here via:

```
docker compose up
```

Once running, an HTTP-connected-GoPro can be communicated with by replacing the default `10.5.5.9:8080` with
`localhost:8082`. For example you can get the state via:

```
curl http://localhost:8082/gopro/camera/state
```

## Future work

- [ ] Allow the camera IP and port to be set at run-time
- [ ] Add camera HTTPS support
