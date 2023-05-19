FROM python:3.10-alpine

RUN apk add --no-cache \
    git \
    curl \
    bash

RUN pip install git+https://github.com/linkchecker/linkchecker.git@v10.2.1

WORKDIR /workdir
COPY entrypoint.sh ./entrypoint.sh
COPY parse_linkchecker_results.py ./parse_linkchecker_results.py

ENTRYPOINT [ "/workdir/entrypoint.sh" ]
