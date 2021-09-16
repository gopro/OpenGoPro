---
permalink: /demos
read_time: false
redirect_from:
    - /swift
    - /python
    - /csharp
    - /c_c++
    - /ionic
---

# Demos

{% assign languages = "" | split: " " %}
{% for demo in site.demos %}
    {% assign parts = demo.path | split: "/" %}
    {% assign language = parts[1] | split: " " %}
    {% assign languages = languages | concat: language %}
{% endfor %}

{% assign unique_languages = languages | uniq %}
{% for language in unique_languages %}
    {% assign words = language | split: '_' %}
# {% for word in words %}{{ word | capitalize }} {% endfor %}
    {% for demo in site.demos %}
        {% assign parts = demo.path | split: "/" %}
        {% assign target_language = parts[1] %}
        {% if target_language == language %}
[{{ demo.title }}]({{ demo.permalink | prepend: site.baseurl }})

- {{ demo.snippet }}

        {% endif %}
    {% endfor %}
{% endfor %}