#!/usr/bin/env python3
"""Fix part fields that contain title text instead of numbers."""

import os
import re
from collections import defaultdict

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "islam")


def read_frontmatter(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.S)
    if not m:
        return None, content
    return m.group(1), m.group(2)


def get_field(fm_text, field):
    for line in fm_text.split("\n"):
        if line.startswith(f"{field}:"):
            val = line.split(":", 1)[1].strip()
            return val.strip("'\"")
    return None


def set_field(fm_text, field, value):
    needs_quotes = any(c in value for c in ":{}[],'\"&*?|>!%@`#")
    quoted = f"'{value}'" if needs_quotes else value
    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(f"{field}:"):
            lines[i] = f"{field}: {quoted}"
            return "\n".join(lines)
    lines.append(f"{field}: {quoted}")
    return "\n".join(lines)


def is_numeric_part(part):
    """Check if part is already a valid numeric-ish value (1, 2, 1a, 1b, addendum, etc)."""
    if not part:
        return False
    return bool(re.match(r"^[0-9]+[a-z]?$", part)) or part in ("addendum",)


def main():
    fixed = 0
    for folder in sorted(os.listdir(CONTENT_DIR)):
        folder_path = os.path.join(CONTENT_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        # Collect all articles grouped by series+subcategory
        articles = []
        for fname in os.listdir(folder_path):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(folder_path, fname)
            fm, body = read_frontmatter(fpath)
            if fm is None:
                continue
            series = get_field(fm, "series")
            part = get_field(fm, "part")
            subcategory = get_field(fm, "subcategory") or ""
            title = get_field(fm, "title") or fname
            articles.append({
                "path": fpath,
                "fm": fm,
                "body": body,
                "series": series,
                "part": part,
                "subcategory": subcategory,
                "title": title,
            })

        # Group by (series, subcategory)
        groups = defaultdict(list)
        for a in articles:
            if a["series"] and a["part"] and not is_numeric_part(a["part"]):
                groups[(a["series"], a["subcategory"])].append(a)

        for (series, subcat), group in groups.items():
            # Find max existing numeric part for this series in this folder
            max_existing = 0
            for a in articles:
                if a["series"] == series and a["subcategory"] == subcat and a["part"] and is_numeric_part(a["part"]):
                    try:
                        num = int(re.sub(r"[^0-9]", "", a["part"]) or "0")
                        max_existing = max(max_existing, num)
                    except ValueError:
                        pass

            # Sort by title for consistent ordering
            group.sort(key=lambda a: a["title"])

            for i, a in enumerate(group, max_existing + 1):
                new_part = str(i)
                a["fm"] = set_field(a["fm"], "part", new_part)
                with open(a["path"], "w", encoding="utf-8") as f:
                    f.write(f"---\n{a['fm']}\n---\n{a['body']}")
                fixed += 1

    print(f"Fixed {fixed} articles with non-numeric part values")


if __name__ == "__main__":
    main()
