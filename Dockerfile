# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:11 PM

FROM ruby:3.2-alpine

RUN apk add --no-cache build-base bash curl python3 py3-pip

# Install bundler
RUN gem install bundler

WORKDIR /site

# Install ruby gems.
# Note! Since we're doing this when building the image, the image needs to be re-built if we change the gems
COPY docs/Gemfile .
RUN bundle install

# Install our python tools
COPY ./tools /tools
RUN pip install /tools/prepare_demos

# Default to just enter image in bash. Should be overriden in container definition in docker-compose.yml
ENTRYPOINT [ "/tools/entrypoint.sh" ]
