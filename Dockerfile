# Dockerfile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:50 UTC 2021

FROM ruby:2.7-alpine

WORKDIR /site

RUN apk add --no-cache build-base
RUN apk add --no-cache gcc bash git

# Install bundler
RUN gem install bundler

# Install ruby gems.
# Note! Since we're doing this when building the image, the image needs to be re-built if we change the gems
COPY docs/Gemfile* .
RUN bundle config set --local system 'true' && bundle install
# Port 4000 doesn't work for some reason?
EXPOSE 5000

# Default command to run if no command is passed
CMD ["bundle exec jekyll serve --host 0.0.0.0 --port 5000 --force_polling --incremental --baseurl ''"]
# If a command is passed, execute it in bash
ENTRYPOINT [ "/bin/bash", "-c" ]
