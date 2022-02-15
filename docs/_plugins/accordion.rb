# accordion.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:21 PM

require "liquid/tag/parser"

require_relative 'common'

module Jekyll
    class Accordion < Liquid::Tag
        # include all standard liquid filters
        include Liquid::StandardFilters

        def initialize(tag, args, tokens)
            super
            @raw_args = args
            @tag = tag.to_sym
            @args = Liquid::Tag::Parser.new(args)
            @tokens = tokens
        end

        def render(context)
            # Extract arguments
            question = convert_markdown(context, @args[:question])
            answer = convert_markdown(context, @args[:answer])
            # Load template file
            currentDirectory = File.dirname(__FILE__)
            templateFile = File.read(currentDirectory + '/accordion_template.erb')
            template = ERB.new(templateFile)
            return template.result(binding)
        end
    end
end

Liquid::Template.register_tag('accordion', Jekyll::Accordion)
