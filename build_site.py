#!/usr/bin/env python3
"""Rebuild index.html from the editable website-content.md file. Standard library only."""
from html import escape
from pathlib import Path
import re

root = Path(__file__).resolve().parent
source = (root / "website-content.md").read_text(encoding="utf-8")
template = (root / "template.html").read_text(encoding="utf-8")
values = {}
group = field = None
buffer = []

def flush():
    if group and field:
        values[group + "_" + field] = "\n".join(buffer).strip()

for line in source.splitlines():
    if line.startswith("## "):
        flush()
        group, field, buffer = line[3:].strip().upper(), None, []
    elif line.startswith("### "):
        flush()
        field, buffer = line[4:].strip().upper(), []
    elif group and field:
        buffer.append(line)
flush()

for group in ("PROJECT_CONTEXT", "PROJECT_NOTIFIER", "PROJECT_ZORO", "PROJECT_SYNC"):
    url = values.get(group + "_LINK", "").strip()
    label = values.get(group + "_LINK_LABEL", "View project")
    if url.startswith("https://"):
        values[group + "_LINK_HTML"] = (
            '<a class="project-link" target="_blank" rel="noopener noreferrer" href="'
            + escape(url, quote=True) + '">' + escape(label) + ' ↗</a>'
        )
    else:
        values[group + "_LINK_HTML"] = ""

def replace(match):
    key = match.group(1)
    if key not in values:
        raise ValueError("Unknown template field: " + key)
    if key.endswith("_LINK_HTML"):
        return values[key]
    return escape(values[key], quote=True).replace("\n", "<br>")

page = re.sub(r"{{([A-Z0-9_]+)}}", replace, template)
(root / "index.html").write_text(page, encoding="utf-8")
print("Rebuilt index.html")
