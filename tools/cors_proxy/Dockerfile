FROM nginx:alpine

WORKDIR /etc/nginx
COPY ./nginx.conf ./conf.d/default.conf
ENTRYPOINT [ "nginx" ]
CMD [ "-g", "daemon off;" ]
