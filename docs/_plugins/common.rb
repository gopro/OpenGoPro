def convert_markdown (context, markdown)
    converter = context.registers[:site].find_converter_instance(::Jekyll::Converters::Markdown)
    converted = converter.convert(markdown)
    start = converted.index(">") + 1 # Remove html tag open
    stop = converted.rindex("</") # Remove html tag close
    return converted.slice(start...stop)
end