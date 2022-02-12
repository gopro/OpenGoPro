---
layout: none
---

var store = [
  {%- for c in site.collections -%}
    {%- assign last_doc = false -%}
    {%- if forloop.last -%}
      {%- assign last_collection = true -%}
    {%- endif -%}
    {%- assign docs = c.docs | where_exp:'doc','doc.search != false' -%}
    {%- for doc in docs -%}
      {%- assign last_section = false -%}
      {%- if forloop.last -%}
            {%- assign last_doc = true -%}
      {%- endif -%}
      {%- assign sections = doc.content | newline_to_br | strip_newlines | split: "<br />#" -%}
      {%- for section in sections -%}
        {%- if forloop.last -%}
            {%- assign last_section = true -%}
        {%- endif -%}

        {%- assign tokens = section | split: "<br />" -%}
        {%- if forloop.first -%}
            {%- assign id = "" -%}
        {% elsif tokens.size == 1 %}
            {%- continue -%}
        {% else %}
            {%- assign id = tokens[0] | remove: "#" | strip -%}
        {% endif %}
        {
            "title": {{ doc.title | append: ": " | append: id | jsonify }},
            "excerpt": {{ section |
                newline_to_br |
                replace:"<br />", " " |
                replace:"</p>", " " |
                replace:"</h1>", " " |
                replace:"</h2>", " " |
                replace:"</h3>", " " |
                replace:"</h4>", " " |
                replace:"</h5>", " " |
                replace:"</h6>", " "|
                strip_html |
                strip_newlines |
                jsonify }},
            "categories": {{ doc.categories | jsonify }},
            "tags": {{ doc.tags | jsonify }},
            "url": {{ doc.url | relative_url |
                        append: "#" |
                        append: id |
                        replace: " ", "-" |
                        remove: "(" |
                        remove: ")" |
                        remove: "!" |
                        jsonify }},
            "teaser": ''
        }
      {%- unless last_file and last_section -%},{%- endunless -%}
    {%- endfor -%}
    {%- endfor -%}
  {%- endfor -%}
]