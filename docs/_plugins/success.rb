# success.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Wed, Sep  1, 2021  5:06:22 PM

module Jekyll
    class Success < Liquid::Tag
        # include all URL filters from Jekyll
        include Jekyll::Filters::URLFilters
        # include all standard liquid filters
        include Liquid::StandardFilters

        def initialize(tag_name, text, tokens)
            super
            @text = text.strip!
        end

        def render(context)
            # required for URLFilters
            @context = context

            "<div class=\"success\">" +
                "<i " +
                    "class=\"fa fa-check-circle fa-2x\" " +
                    "style=\"" +
                        "color: #2dcb71;" +
                        "margin: 0.25em;" +
                    "\"" +
                "></i>" +
                "<span>  #{@text}</span>" +
            "</div>"
        end

        private

        def config
            @config ||= @context.registers[:site].config
        end
    end
end

Liquid::Template.register_tag('success', Jekyll::Success)
