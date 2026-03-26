from parsel import Selector


def clean_html(html):
    if not html:
        return html
    sel = Selector(text=html)
    # Iterate through every node in the tree
    for node in sel.xpath("//*"):
        # Access the underlying lxml element via .root
        node.root.attrib.pop("style", None)
        node.root.attrib.pop("class", None)

    # Return the serialised HTML
    return sel.get()
