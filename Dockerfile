# Dockerfile/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:38 AM

FROM r-base

# We can't have any user input
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    pandoc \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    tree

RUN R -e "install.packages(c('rmdformats', 'rmarkdown', 'htmlwidgets', 'devtools', 'optparse', 'DiagrammeR'), repos='https://cloud.r-project.org/')"

COPY . /workspace
WORKDIR /workspace

RUN make -f /workspace/tools/rdocs/Makefile install

CMD make -f ./tools/rdocs/Makefile tutorials
