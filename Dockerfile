# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:11 PM

FROM ruby:2.7-alpine

WORKDIR /site

RUN apk add --no-cache build-base
RUN apk add --no-cache bash curl

# Install bundler
RUN gem install bundler

# Install ruby gems.
# Note! Since we're doing this when building the image, the image needs to be re-built if we change the gems
COPY docs/Gemfile* /site/
RUN bundle config set --local system 'true' && bundle install

# Default to just enter image in bash. Should be overriden in container definition in docker-compose.yml
CMD [ "/bin/bash" ]
