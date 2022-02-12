---
layout: none
---

{% assign searchable_pages = site.pages | where_exp: "page", "page.title and page.search != false" %}
{%- for collection in site.collections -%}
    {%- assign docs = c.docs | where_exp:'doc','doc.search != false' -%}
    {%- for doc in docs -%}
        {% assign searchable_pages = searchable_pages | push: doc %}
    {%- endfor -%}
{%- endfor -%}


var store = [
    {%- for doc in searchable_pages -%}
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
            {%- assign slug = id -%}
        {% elsif tokens.size == 1 %}
            {%- continue -%}
        {% else %}
            {%- assign id = tokens[0] | remove: "#" | strip -%}
            {%- assign slug = id | slugify -%}
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
                replace:"</h6>", " " |
                strip_html |
                remove: "#" |
                remove_first: id |
                strip_newlines |
                strip |
                jsonify }},
            "categories": [],
            "tags": [],
            "url": {{ doc.url | relative_url |
                        append: "#" |
                        append: slug |
                        jsonify }},
            "teaser": ''
        }
      {%- unless last_file and last_section -%},{%- endunless -%}
    {%- endfor -%}
    {%- endfor -%}
]