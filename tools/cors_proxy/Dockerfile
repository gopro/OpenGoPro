# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Jul 24 17:52:26 UTC 2024

FROM nginx:alpine

WORKDIR /etc/nginx
COPY ./nginx.conf ./conf.d/default.conf
ENTRYPOINT [ "nginx" ]
CMD [ "-g", "daemon off;" ]
