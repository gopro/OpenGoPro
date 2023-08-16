# Dockerfile/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:11 PM

FROM ruby:3.2.2-bullseye

RUN gem install bundler

# Install ruby gems.
# Note! Since we're doing this when building the image, the image needs to be re-built if we change the gems
COPY Gemfile /
RUN bundle install

COPY entrypoint.sh /bin/entrypoint.sh

WORKDIR /site

ENTRYPOINT [ "/bin/entrypoint.sh" ]
