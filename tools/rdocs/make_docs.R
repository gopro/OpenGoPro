# make_docs.R/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Thu, May  6, 2021 11:38:41 AM

library("optparse")

option_list <- list(
    make_option(c("-i", "--input"),
        type = "character", default = NULL,
        help = "input .rmd file", metavar = "character"
    ),
    make_option(c("-o", "--output"),
        type = "character", default = NULL,
        help = "output directory", metavar = "character"
    )
)
opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)

if (is.null(opt$input)) {
    print_help(opt_parser)
    stop("Input file must be supplied", call. = FALSE)
}

if (is.null(opt$output)) {
    print_help(opt_parser)
    stop("Output file must be supplied", call. = FALSE)
}

require(rmdformats)
require(rmarkdown)
require(knitr)
require(htmlwidgets)
require(quiz)
require(DiagrammeR)

knitr::opts_chunk$set(echo = FALSE)

render(opt$input, output_dir = opt$output)