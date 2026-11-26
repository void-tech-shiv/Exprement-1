from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.tags = []
        self.styles = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.styles.append(attrs["href"])


page = Page()
page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
assert {"header", "main", "nav", "footer"}.issubset(page.tags)
assert page.tags.count("h1") == 1
assert len(page.ids) == len(set(page.ids))
assert all(link and link != "#" for link in page.links)
assert all(link[1:] in page.ids for link in page.links if link.startswith("#"))
assert page.styles and all((ROOT / path).is_file() for path in page.styles)
assert (ROOT / "assets" / "cover.svg").is_file()
print("Portfolio structure checks passed.")
