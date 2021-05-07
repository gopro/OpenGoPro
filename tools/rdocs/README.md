- [Tools to build Rmarkdown documents into HTML](#tools-to-build-rmarkdown-documents-into-html)
  - [Directory Structure](#directory-structure)
  - [Requirements](#requirements)
  - [Usage](#usage)
  - [Building](#building)
    - [Getting Docker image](#getting-docker-image)
    - [More Info](#more-info)
  - [HTML Widgets](#html-widgets)
  - [Mermaid Diagrams](#mermaid-diagrams)

# Tools to build Rmarkdown documents into HTML

This directory contains a framework to convert Rmd files into nice-looking html. It is used
for some of the tutorials in this repo.

## Directory Structure

```
├── make_docs.R: R script to ensure required libraries are available and build html from an Rmd
├── Makefile: used to build html's when their Rmd targets change
├── quiz: directory to implement quiz htmlwidget
│   ...
├── README.md: This file
└── style.css: custom css to override theme used for generated html
```

## Requirements

Docker must be [installed](https://docs.docker.com/get-docker/).

## Usage

1. Write a document in rmarkdown (it is basically markdown with the ability to run code and have some interactivity)
2. Build as shown below to generate html output

## Building

This tool is meant to be run using the top-level Docker image defined in this repo. It's default command is to build
the docs. So to build the docs, you can just run the docker container (from the top-level of the repo) as:

### Getting Docker image

```
docker-compose run --rm docs
```

> Note! If you haven't ever built the image, you need to first:

```
docker-compose build docs
```

It will take around 8 minutes but this is a one-time thing.

### More Info

What the default command is doing is calling the `html` make goal of the Makefile defined in this directory to, in turn,
pass an input .rmd file and output directory to the `make_docs.R` script. So, you can also enter the docker
container and invoke this manually if desired as:

```
docker-comopse run --rm docs bash
make -f ./tools/rdocs/Makefile html
```

For more information on the makefile, try:

```
make -f ./tools/rdocs/Makefile help
```

The makefile is configured to automatically build any .Rmd's in the `tutorials` folder. If this needs to
be changed for some reason, the `RMDS` variable in the Makefile should be changed.

Of course, it is also possible to set up your local machine appropriately and do any of the above outside of Docker
if one so desired.

## HTML Widgets

It is possible to create html / javascript widgets that can be used by the rmarkdown documentation. So far, the
only one that exists here is the "quiz" widget.

To build a new one, follow the steps from the [documentation](http://www.htmlwidgets.org/develop_intro.html)

It is also possible to use any of the [pre-existing html widgets](http://gallery.htmlwidgets.org/)

## Mermaid Diagrams

The R [DiamgammeR](https://rich-iannone.github.io/DiagrammeR/) package is used to create in-line diagrams (
sequence diagrams, flow charts, etc) using Mermaid.

Here is an example:

```R
```{r, out.height='50%'}
mermaid(diagram = '
sequenceDiagram
  participant GoPro
  participant PC
  GoPro-->>PC: Advertising
  GoPro-->>PC: Advertising
  note over PC: Scanning
  PC->>GoPro: Connect
  note over GoPro, PC: Connected
  PC ->> GoPro: Pair Request
  GoPro ->> PC: Pair Response
  note over GoPro, PC: Paired
  PC ->> GoPro: Enable Notifications on Characteristic 1
  PC ->> GoPro: Enable Notifications on Characteristic 2
  PC ->> GoPro: Enable Notifications on Characteristic ..
  PC ->> GoPro: Enable Notifications on Characteristic N
  note over GoPro, PC: Ready to Communicate
')
```


For more information on the Mermaid syntax see [here](https://mermaid-js.github.io/mermaid/).
For a mermaid live editor, see [here](https://mermaid-js.github.io/mermaid-live-editor/).
