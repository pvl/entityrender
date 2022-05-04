from itertools import cycle

# Entity renderer adapted from displacy code in
# https://github.com/explosion/spaCy/tree/master/spacy/displacy
# MIT license
TPL_TITLE = """
<h2 style="margin: 0">{title}</h2>
"""

TPL_ENTS = """
<div class="entities" style="line-height: 2.5">{content}</div>
"""


TPL_ENT = """
<mark class="entity" style="background: {bg}; padding: 0.25em 0.3em; margin: 0 0.15em; line-height: 1; border-radius: 0.35em; box-decoration-break: clone; -webkit-box-decoration-break: clone">
    {text}
    <span style="font-size: 0.7em; font-weight: bold; line-height: 1; border-radius: 0.35em; text-transform: lowercase; vertical-align: middle; margin-left: 0.5rem">{label}</span>
</mark>
"""


class EntityRenderer(object):
    """Render named entities as HTML."""

    style = "ent"

    def __init__(self, labels, options={}):
        """Initialise dependency renderer.
        names: list of entity names
        options (dict): Visualiser-specific options (colors, ents)
        """

        base_colors = ["#7aecec", "#c887fb", "#ffeb80", "#bfeeb7", "#ff8197"]
        colors = dict(zip(labels, cycle(base_colors)))

        colors.update(options.get("colors", {}))
        self.default_color = "#ddd"
        self.colors = colors
        self.ents = options.get("ents", None)

    def render_ents(self, text, spans, title=""):
        """Render entities in text.
        text (unicode): Original text.
        spans (list): Individual entity spans and their start, end and label.
        title (unicode or None): Document title.
        """
        markup = ""
        offset = 0
        for span in spans:
            label = span["label"]
            start = span["start"]
            end = span["end"]
            entity = text[start:end]
            fragments = text[offset:start].split("\n")
            for i, fragment in enumerate(fragments):
                markup += fragment
                if len(fragments) > 1 and i != len(fragments) - 1:
                    markup += "<br>"
            if self.ents is None or label.upper() in self.ents:
                color = self.colors.get(label, self.default_color)
                markup += TPL_ENT.format(label=label, text=entity, bg=color)
            else:
                markup += entity
            offset = end
        markup += text[offset:]
        markup = TPL_ENTS.format(content=markup, colors=self.colors)
        if title:
            markup = TPL_TITLE.format(title=title) + markup
        return markup
