# Open GoPro Documentation

- [Open GoPro Documentation](#open-gopro-documentation)
  - [Directory Structure](#directory-structure)
  - [Usage](#usage)
    - [Requirements](#requirements)
    - [Usage](#usage-1)
    - [Deployment](#deployment)
  - [Site layout](#site-layout)
  - [Contribution](#contribution)
  - [Testing](#testing)


This directory houses the documentation as well as the framework required to build the Jekyll site.

The documentation files consist of:

-   Interface specifications
-   Walk-through tutorials in various languages / frameworks

It is based on the [minimal mistakes theme](https://mmistakes.github.io/minimal-mistakes/).

## Directory Structure

```
├── README.md: This file
├── _config.yml: Jekyll site configuration
├── _data
│   └── navigation.yml: navigation menu definitions
├── _includes: html files that are added via the "include" liquid tag
├── _layouts: any layouts that overwrite default layouts or are new layouts
├── _plugins: Ruby files and templates for custom liquid tags and filters
│   ├── accordion.rb: accordion used for faq's
│   ├── accordion_template.erb: html template for accordion
│   ├── note.rb: blue note callout
│   ├── quiz.rb: multiple choice quiz
│   ├── quiz_template.erb: html template for quiz
│   ├── success.rb: green success callout
│   ├── tabs.rb: dynamic tabs
│   ├── tabs_template.erb: tabs html template
│   ├── tip.rb: orange tip callout
│   └── warning.rb: red warning callout
├── _sass: .scss files that overwrite the default minimal mistakes files
│   ├── ...
├── _site: location of generated site when it is built (ignored via .gitignore)
├── assets: static assets served along with the built html files
├── contribution.md: an example of various tools / functionality for writing .md files in this repo
├── faq.md: frequently asked questions
├── tutorials.md: top-level tutorials entrypoint
├── index.md: the home page.
├── specs: Open GoPro interface specifications
│   ├── ble_versions: individual BLE specs
│   └── http_versions: individual HTTP specs
└── tutorials: This is the Jekyll collections directory.
    ├── tutorial_X_XXX: per-tutorial documentation
    └── ...
```

## Usage

### Requirements

-   It is assumed that your environment has access to GNU or BSD tools (i.e. this will not run natively on Windows)
-   [Docker](https://www.docker.com) must be installed
-   To edit any files tracked by `.gitattributes`, git-lfs must be [installed](https://git-lfs.github.com/)

### Usage

First, build and serve the site locally via:

```
make serve
```

The site can then be viewed at `http://localhost:4998`

> Note! This is different than the address from the Jekyll CLI output

As you modify .md files in the `docs` repo, the changes will be mirrored to the local site when the page is
refreshed. The local site is served with an "incremental" build such that only the necessary files are re-built
after a change. This should work fine for modifications to .md files. However, if a sweeping change such
as site-wide configuration is made, it will likely be necessary to re-build the entire site via:

```
make clean serve
```

### Deployment

Github Pages serves the site from the `gh-pages` branch of this repo. Whenever the main branch is updated (such
as via a Pull Request being merged),
the "Jekyll Build and Deploy" [Github Actions](hhttps://github.com/gopro/OpenGoPro/actions/workflows/release.yml) workflow will automatically
be triggered to build the site from `main` and update the `gh-pages` branch.

> Note! This process should be invisible to the developer

## Site layout

The site map can be found after building the site at: `./_site/sitemap.xml`.

## Contribution

There is a contribution guide that describes all of the various features available either via the
minimal mistakes theme, the various Ruby gem plugins, or custom plugins in this repo such as:

-   links
-   callouts
-   figures
-   tabs
-   etc.

The source for the guide is in [contribution.md](contribution.md).

To view its output, serve the site, then go to [localhost:4998/contribution](localhost:4998/contribution)

## Testing

Assuming that python is installed and that the site is currently being served locally, the page can be tested
for any invalid links via the top-level Makefile in this repo:

```
make tests
```
