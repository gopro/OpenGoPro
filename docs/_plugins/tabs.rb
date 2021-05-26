# tabs.rb/Open GoPro, Version 1.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue May 18 22:08:52 UTC 2021

require 'securerandom'
require 'erb'

module Jekyll
    module Tabs
        class TabsBlock < Liquid::Block
            def initialize(block_name, markup, tokens)
                super
                if markup == ''
                    raise SyntaxError.new("Block #{block_name} requires 1 attribute")
                end
                @name = markup.strip
            end

            def render(context)
                environment = context.environments.first
                super

                uuid = SecureRandom.uuid
                currentDirectory = File.dirname(__FILE__)
                templateFile = File.read(currentDirectory + '/tabs_template.erb')
                template = ERB.new(templateFile)
                template.result(binding)
            end
        end

        class TabBlock < Liquid::Block
            alias_method :render_block, :render

            def initialize(block_name, markup, tokens)
                super
                markups = markup.split(' ', 2)
                if markups.length != 2
                    raise SyntaxError.new("Block #{block_name} requires 2 attributes")
                end
                @name = markups[0]
                @tab = markups[1]
            end

            def render(context)
                site = context.registers[:site]
                converter = site.find_converter_instance(::Jekyll::Converters::Markdown)
                environment = context.environments.first
                environment["tabs-#{@name}"] ||= {}
                environment["tabs-#{@name}"][@tab] = converter.convert(render_block(context))
            end
        end
    end
end

Liquid::Template.register_tag('tab', Jekyll::Tabs::TabBlock)
Liquid::Template.register_tag('tabs', Jekyll::Tabs::TabsBlock)