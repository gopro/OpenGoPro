# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed Oct 19 15:33:20 UTC 2022

FROM python:3.10

WORKDIR /workdir
COPY ./test/get_test_zip.py /workdir

RUN pip install --upgrade pip
RUN pip install requests==2.28.1

ENTRYPOINT ["python", "./get_test_zip.py"]