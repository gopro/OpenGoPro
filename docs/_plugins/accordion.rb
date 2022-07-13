# accordion.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:21 PM

require "liquid/tag/parser"

require_relative 'common'

module Jekyll
    class Accordion < Liquid::Block
        alias_method :render_block, :render

        # include all standard liquid filters
        include Liquid::StandardFilters

        def initialize(block_name, markup, tokens)
            super
            if markup == ''
                raise SyntaxError.new("Block #{block_name} requires 1 attribute")
            end
            @title=markup
        end

        def render(context)
            # Get converter
            site = context.registers[:site]
            converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
            # Convert content
            title = convert_markdown(context, @title)
            content = converter.convert(render_block(context))
            # Place results into html
            output = <<~EOS
            <div class="accordion-container">
                <button class="accordion">#{title}<i class="fa fa-chevron-down"></i></i></button>
                <div class="panel">#{content}</div>
            </div>
            EOS
            return output
        end
    end
end

Liquid::Template.register_tag('accordion', Jekyll::Accordion)
