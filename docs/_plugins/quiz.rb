# quiz.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:22 PM

require "liquid/tag/parser"
require 'securerandom'
require 'erb'

module Jekyll
    class Quiz < Liquid::Tag
        # include all URL filters from Jekyll
        include Jekyll::Filters::URLFilters
        # include all standard liquid filters
        include Liquid::StandardFilters

        def initialize(tag, args, tokens)
            super
            @raw_args = args
            @tag = tag.to_sym
            @args = Liquid::Tag::Parser.new(args)
            @tokens = tokens
            super
        end

        def render(context)
            # required for URLFilters
            @context = context

            # Need a unique ID for our quiz
            uuid = SecureRandom.uuid

            # Extract arguments
            question = @args[:question]
            correct = @args[:correct]
            info = @args[:info]
            option_chars = []
            option_strings = []

            options = @args[:option]
            options.each { |option|
                parts = option.split(":::", 2)
                option_chars << parts[0]
                option_strings << parts[1]
            }

            # Load template file
            currentDirectory = File.dirname(__FILE__)
            templateFile = File.read(currentDirectory + '/quiz_template.erb')
            template = ERB.new(templateFile)
            output = template.result(binding)

            return output
        end

        private

        def config
            @config ||= @context.registers[:site].config
        end
    end
end

Liquid::Template.register_tag('quiz', Jekyll::Quiz)
