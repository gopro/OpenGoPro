# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Fri Jun  9 22:45:24 UTC 2023

ARG ALPINE_VERSION=3.16

##### Building stage #####
FROM alpine:${ALPINE_VERSION} as builder

# Versions of nginx, rtmp-module and ffmpeg
ARG NGINX_VERSION=1.23.0
ARG NGINX_RTMP_MODULE_VERSION=1.2.2
ARG FFMPEG_VERSION=5.1

# Install dependencies
RUN apk update && \
    apk --no-cache add \
        bash build-base ca-certificates \
        openssl openssl-dev make \
        gcc libgcc libc-dev rtmpdump-dev \
        zlib-dev musl-dev pcre pcre-dev lame-dev \
        yasm pkgconf pkgconfig libtheora-dev \
        libvorbis-dev libvpx-dev freetype-dev \
        x264-dev x265-dev && \
    rm -rf /var/lib/apt/lists/*

# Download nginx source
RUN mkdir -p /tmp/build && \
    cd /tmp/build && \
    wget https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar zxf nginx-${NGINX_VERSION}.tar.gz && \
    rm nginx-${NGINX_VERSION}.tar.gz

# Download rtmp-module source
RUN cd /tmp/build && \
    wget https://github.com/arut/nginx-rtmp-module/archive/v${NGINX_RTMP_MODULE_VERSION}.tar.gz && \
    tar zxf v${NGINX_RTMP_MODULE_VERSION}.tar.gz && \
    rm v${NGINX_RTMP_MODULE_VERSION}.tar.gz

# Build nginx with nginx-rtmp module
RUN cd /tmp/build/nginx-${NGINX_VERSION} && \
    ./configure \
        --sbin-path=/usr/local/sbin/nginx \
        --conf-path=/etc/nginx/nginx.conf \
        --error-log-path=/var/log/nginx/error.log \
        --http-log-path=/var/log/nginx/access.log \
--pid-path=/var/run/nginx/nginx.pid \
    --lock-path=/var/lock/nginx.lock \
    --http-client-body-temp-path=/tmp/nginx-client-body \
    --with-http_ssl_module \
    --with-stream \
    --with-stream_ssl_module \
    --with-threads \
    --add-module=/tmp/build/nginx-rtmp-module-${NGINX_RTMP_MODULE_VERSION} && \
    make CFLAGS=-Wno-error -j $(getconf _NPROCESSORS_ONLN) && \
    make install

# Download ffmpeg source
RUN cd /tmp/build && \
    wget http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar zxf ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    rm ffmpeg-${FFMPEG_VERSION}.tar.gz

# Build ffmpeg
RUN cd /tmp/build/ffmpeg-${FFMPEG_VERSION} && \
    ./configure \
        --enable-version3 \
        --enable-gpl \
        --enable-small \
        --enable-libx264 \
        --enable-libx265 \
        --enable-libvpx \
        --enable-libtheora \
        --enable-libvorbis \
        --enable-librtmp \
        --enable-postproc \
        --enable-swresample \
--enable-libfreetype \
    --enable-libmp3lame \
    --disable-debug \
    --disable-doc \
    --disable-ffplay \
    --extra-libs="-lpthread -lm" && \
    make -j $(getconf _NPROCESSORS_ONLN) && \
    make install

# Copy stats.xsl file to nginx html directory and clean build files
RUN cp /tmp/build/nginx-rtmp-module-${NGINX_RTMP_MODULE_VERSION}/stat.xsl /usr/local/nginx/html/stat.xsl && \
    rm -rf /tmp/build

##### Building the final image #####
FROM alpine:${ALPINE_VERSION}

# Install dependencies
RUN apk update && \
    apk --no-cache add \
        bash ca-certificates openssl \
        pcre libtheora libvorbis lame libvpx \
        librtmp x264-dev x265-dev freetype htop && \
    rm -rf /var/lib/apt/lists/*

# Copy files from build stage to final stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /etc/nginx /etc/nginx
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /var/lock /var/lock
COPY --from=builder /var/run/nginx /var/run/nginx

# Forward logs to Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./hls.html /usr/local/nginx/html/player.html
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./cert_request.ext /cert_request.ext
COPY ./cert_request.ini /cert_request.ini

# Copy run script to container
COPY entrypoint.sh /entrypoint.sh

CMD ["bash", "/entrypoint.sh"]
