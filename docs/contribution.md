# Contribution

This page will provide  examples for various documentation features available in this repo / theme.

## Examples

### Links

#### External

External links should be created using standard markdown links, i.e.

```
[GoPro](https://gopro.com/)
```

[GoPro](https://gopro.com/)


Note that the `https://` is required otherwise the link will be attempted to resolve to a local file.

#### Internal

Internal links shall be created using the Jekyll [link](https://jekyllrb.com/docs/liquid/tags/#links) tag with the
path to the file from the top of the directory.

For example, to link to [this file]({% link contribution.md %}):

{% raw %}
```
[this file]({% link contribution.md %})
```
{% endraw %}

Specific sections can also be linked. For example, to link to [this section]({% link contribution.md %}#internal):

{% raw %}
```
[this section]({% link contribution.md %}#internal):
```
{% endraw %}

There is an exception to this when linking to a file in the `tutorials`. These are handled differently
since `tutorials` is the base directory for all collections. Therefore, the `tutorials` directory should be omitted
from the path. For example, to link to [the first python tutorial]({% link _python-tutorials/tutorial_1_connect_ble.md %}):

{% raw %}
```
[the first python tutorial]({% link _python-tutorials/tutorial_1_connect_ble.md %})
```
{% endraw %}


### Callouts

#### Notes

Blue colored notes via:

{% raw %}

```markdown
{% note This is a note. %}
```

{% endraw %}
{% note This is a note. %}


#### Successes

Green colored success via:

{% raw %}

```markdown
{% success This is for when something good has happened. %}
```

{% endraw %}
{% success This is for when something good has happened. %}

#### Warnings

Red colored warnings via:

{% raw %}

```markdown
{% warning This is for when something bad has happened. %}
```

{% endraw %}
{% warning This is for when something bad has happened. %}

#### Tips

Yellow colored tips via:

{% raw %}

```markdown
{% tip This is for tips. %}
```

{% endraw %}
{% tip This is for tips. %}

If one of the above options does not suit your use case, there is also the option for a simple callout using
default markdown syntax via:

```markdown
> I'm a simple callout
```

> I'm a simple callout

### Collapsible Accordion

Collapsible accordion sections can be added, for example with use for FAQ's via:

{% raw %}
```markdown
{% accordion
  question="Question"
  answer="Answer"
%}

```
{% endraw %}

Here is an example:

{% accordion
  question="Question"
  answer="Answer"
%}


### Quiz

Multiple choice quizzes via:

{% raw %}
```markdown
{% quiz
    question="What is the question?"
    option="A:::Option 1 (this one is correct)"
    option="B:::Option 2"
    option="C:::Option 3"
    correct="A"
    info="And here is some more info"
%}
```
{% endraw %}

{% quiz
    question="What is the question?"
    option="A:::Option 1 (this one is correct)"
    option="B:::Option 2"
    option="C:::Option 3"
    correct="A"
    info="And here is some more info"
%}

True or false quizzes can be made from this via:

{% raw %}
```markdown
{% quiz
    question="True or False?"
    option="True:::Option 1(this one is correct)"
    option="False:::Option 2"
    correct="True"
    info="And here is some more info"
%}
```
{% endraw %}

{% quiz
    question="True or False?"
    option="True:::Option 1(this one is correct)"
    option="False:::Option 2"
    correct="True"
    info="And here is some more info"
%}

### Tabs

Tabs can be created via:

{% raw %}
```markdown
{% tabs example %}
{% tab example tab1 %}
This is the content of the first tab.
{% endtab %}
{% tab example tab 2 %}
This is the content of the second tab.
{% endtab %}
{% tab example tab3 %}
This is the content of the third tab.
{% endtab %}
{% endtabs %}
```
{% endraw %}

{% tabs example %}
{% tab example tab1 %}
This is the content of the first tab.
{% endtab %}
{% tab example tab 2 %}
This is the content of the second tab.
{% endtab %}
{% tab example tab3 %}
This is the content of the third tab.
{% endtab %}
{% endtabs %}

### Diagrams

You can add Mermaid or PlantUML diagrams. They are centered by default.

{% note Note for the following examples, you need 3 leading backticks instead of 2. We're only showing 2 here
because there is no way to escape this properly. If this is unclear, just look at the .md file. %}

#### Mermaid

[Mermaid](https://mermaid-js.github.io/mermaid/#/) diagrams via:

````markdown
``mermaid!
pie title Pets adopted by volunteers
  "Dogs" : 386
  "Cats" : 85
  "Rats" : 35
``
````

```mermaid!
pie title Pets adopted by volunteers
  "Dogs" : 386
  "Cats" : 85
  "Rats" : 35
```

#### PlantUML

[PlantUML](https://plantuml.com/) diagrams via:

````markdown
``plantuml!
Bob -> Alice : hello world
``
````

```plantuml!
Bob -> Alice : hello world
```

### Icons

Search for them on [font awesome](https://fontawesome.com/icons). Then add them via html:

```html
<i class="fa fa-tools"></i>
```

<i class="fa fa-tools"></i>

```html
<i class="fa fa-hammer"></i>
```

<i class="fa fa-hammer"></i>

### Emojis

Any [Github](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md) emoji can be used:

I give this page two :+1:

Happy clown --> 🤡

### Variable length / width cell tables

For more information, see the Jekyll Spaceship [documentation](https://github.com/jeffreytse/jekyll-spaceship#1-table-usage)

Normal markdown tables work but you can also combine lines (via the trailing backslash):

```markdown
| : Easy Multiline : |        |           |
| :----------------- | :----- | :-------- |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange    |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange    |
| Apple              | Banana | Orange    |
```

| : Easy Multiline : |        |           |
| :----------------- | :----- | :-------- |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange    |
| Apple              | Banana | Orange \  |
| Apple              | Banana | Orange    |
| Apple              | Banana | Orange    |


or combine individual vertical cells (via `^^`) or horizontal cells (via omitting the `|` separator)

```markdown
|              Stage | Direct Products | ATP Yields |
| -----------------: | --------------: | ---------: |
|         Glycolysis |           2 ATP              |
|                 ^^ |          2 NADH |   3--5 ATP |
| Pyruvaye oxidation |          2 NADH |      5 ATP |
|  Citric acid cycle |           2 ATP |            |
|                 ^^ |          6 NADH |     15 ATP |
|                 ^^ |          2 FADH |      3 ATP |
|         30--32 ATP |                              |
```

|              Stage | Direct Products | ATP Yields |
| -----------------: | --------------: | ---------: |
|         Glycolysis |           2 ATP              |
|                 ^^ |          2 NADH |   3--5 ATP |
| Pyruvaye oxidation |          2 NADH |      5 ATP |
|  Citric acid cycle |           2 ATP |            |
|                 ^^ |          6 NADH |     15 ATP |
|                 ^^ |          2 FADH |      3 ATP |
|         30--32 ATP |                              |

### Figures

Use the `figure` include. Optional parameters are:

- alt: alternate text if image is not found
- size (percentage)
- caption

Remote:

{% raw %}
```
{% include figure image_path="https://raw.githubusercontent.com/gopro/gpmf-parser/master/docs/readmegfx/CameraIMUOrientationSM.png" alt="GoPro Logo" size="50%" caption="This is a figure caption." %}
```
{% endraw %}

{% include figure image_path="https://raw.githubusercontent.com/gopro/gpmf-parser/master/docs/readmegfx/CameraIMUOrientationSM.png" alt="GoPro Logo" size="50%" caption="This is a figure caption." %}

Local:

{% raw %}
```
{% include figure image_path="/assets/images/logos/logo.png" alt="GoPro Logo" size="50%" caption="This is a figure caption." %}
```
{% endraw %}

{% include figure image_path="/assets/images/logos/logo.png" alt="GoPro Logo" size="50%" caption="This is a figure caption." %}

Galleries are also [possible](https://mmistakes.github.io/minimal-mistakes/docs/helpers/#gallery)
