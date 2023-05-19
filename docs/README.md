# Open GoPro Documentation

TODO this is out of date :(

This directory houses the documentation as well as the framework required to build the Jekyll site.

It is based on the [minimal mistakes theme](https://mmistakes.github.io/minimal-mistakes/).

## Directory Structure

```
├── Gemfile: Required Ruby gems to build the site
├── Gemfile.lock: Specific Ruby gem versions. This is generated from the Gemfile
├── README.md: This file
├── _config*.yml: Jekyll site configurations (different configs are needed for test, local, and deployment)
├── _data
│   └── navigation.yml: navigation menu definitions
├── _includes: html files that are added via the "include" liquid tag
│   ├── figure: used to add figures with some parameters
│   ├── footer: custom footer (not currently used)
│   └── head: custom header (used to add favicons)
├── _layouts: any layouts that overwrite default layouts or are new layouts
│   └── demo.html: adds Github button to the "single" layout
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
├── _site: location of generated site when it is built
├── assets: static assets served along with the built html files
│   ├── css
│   ├── images (add any static images from demos, tutorials, etc in relevant subdirectories here)
│   └── js
├── contribution.md: an example of various tools / functionality for writing .md files in this repo
├── demos.md: the top-level demos documentation
├── faq.md: frequently asked questions
├── index.html: the home page.
├── specs: Open GoPro interface specifications
│   ├── ble.md: top level BLE spec information
│   └── http.md: top level HTTP spec information
│   ├── ble_versions: individual BLE specs
│   └── http_versions: individual HTTP specs
└── tutorials: This is the Jekyll collections directory.
    ├── _bash-tutorials: bash tutorial source documentation
    ├── _demos: this is generated before the site is built from the top level demos folder in this repo
    ├── _python-tutorials: python tutorial source documentation
    └── tutorials.md: the top-level tutorials documentation
```

## Usage

See the top-level [README](../README.md) for how to use the Docker image defined in this repo
to locally serve the site for development.

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
