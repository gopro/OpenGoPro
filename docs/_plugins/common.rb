# common.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Feb 15 01:05:56 UTC 2022

def convert_markdown (context, markdown)
    converter = context.registers[:site].find_converter_instance(::Jekyll::Converters::Markdown)
    converted = converter.convert(markdown)
    start = converted.index(">") + 1 # Remove html tag open
    stop = converted.rindex("</") # Remove html tag close
    return converted.slice(start...stop)
end