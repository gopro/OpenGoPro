# callouts.rb/Open GoPro, Version 2.0 (C) Copyright 2021 GoPro, Inc. (http://gopro.com/OpenGoPro).
# This copyright was auto-generated on Tue Feb 15 01:05:56 UTC 2022

require_relative 'common'

module Jekyll
    module Callouts
        class Tip < Liquid::Block
            def render(context)
                "<div class=\"callout tip\">" +
                    "<i class=\"fa fa-tools fa-2x\" style=\"color: #ebc21c; margin: 0.25em;\"></i>" +
                    "<span>#{convert_markdown(context, super)}</span>" +
                "</div>"
            end
        end

        class Note < Liquid::Block
            def render(context)
                "<div class=\"callout note\">" +
                    "<i class=\"fa fa-clipboard fa-2x\" style=\"color: #3498db; margin: 0.25em;\"></i>" +
                    "<span>#{convert_markdown(context, super)}</span>" +
                "</div>"
            end
        end

        class Warning < Liquid::Block
            def render(context)
                "<div class=\"callout warning\">" +
                    "<i class=\"fa fa-exclamation-triangle fa-2x\" style=\"color: #df5142; margin: 0.25em;\"></i>" +
                    "<span>#{convert_markdown(context, super)}</span>" +
                "</div>"
            end
        end

        class Success < Liquid::Block
            def render(context)
                "<div class=\"callout success\">" +
                    "<i class=\"fa fa-check-circle fa-2x\" style=\"color: #2dcb71; margin: 0.25em;\"></i>" +
                    "<span>#{convert_markdown(context, super)}</span>" +
                "</div>"
            end
        end
    end
end

Liquid::Template.register_tag('tip', Jekyll::Callouts::Tip)
Liquid::Template.register_tag('note', Jekyll::Callouts::Note)
Liquid::Template.register_tag('warning', Jekyll::Callouts::Warning)
Liquid::Template.register_tag('success', Jekyll::Callouts::Success)
