#!/usr/bin/env python3
"""
Scraper for a curated set of primary patristic texts from the Christian
Classics Ethereal Library (ccel.org) -- the Ante-Nicene and
Nicene/Post-Nicene Fathers series (Philip Schaff, ed.), all explicitly
marked "Rights: Public Domain" in CCEL's own plain-text editions.

CCEL's copyright policy (https://www.ccel.org/about/copyright.html,
checked 2026-09-21) additionally states these editions "may be used for
personal, educational, or non-profit purposes" -- squarely covers this
project's use case.

CCEL's reader UI is a JS-driven single-page app with no static HTML
per-chapter, so this scraper instead downloads each volume's official
plain-text edition (e.g. https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt)
and slices out individual documents by their title-line markers (found by
inspecting the text), which is far more reliable than trying to reverse
engineer the reader's AJAX API.

Each volume's plain text intersperses footnote blocks (a paragraph whose
every line starts with a bracketed footnote number, e.g. "[1768] ...")
right after the chapter that cites them. These are stripped out (along
with the inline [NNNN] reference markers they'd otherwise orphan) to
produce clean reading text -- the ANF/NPNF critical apparatus roughly
doubles raw length and isn't what a personal-study reader wants.

Run: python3 sources/ccel_fathers.py
"""

import os
import re
import time

import requests
import yaml

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "christian-theology")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".ccel_cache")

SOURCE_NAME = "Christian Classics Ethereal Library"
DEFAULT_AUTHOR_EDITOR = "ed. Philip Schaff"
LICENSE = "Public Domain (CCEL plain-text edition). May be used for personal, educational, or non-profit purposes per ccel.org/about/copyright.html."

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

VOLUME_URL = {
    "anf01": "https://ccel.org/ccel/s/schaff/anf01/cache/anf01.txt",
    "npnf201": "https://ccel.org/ccel/s/schaff/npnf201/cache/npnf201.txt",
    "npnf204": "https://ccel.org/ccel/s/schaff/npnf204/cache/npnf204.txt",
    "orthodoxy": "https://ccel.org/ccel/c/chesterton/orthodoxy/cache/orthodoxy.txt",
    "incarnation": "https://ccel.org/ccel/a/athanasius/incarnation/cache/incarnation.txt",
    "theology1": "https://ccel.org/ccel/h/hodge/theology1/cache/theology1.txt",
}
VOLUME_SOURCE_PAGE = {
    "orthodoxy": "https://ccel.org/ccel/chesterton/orthodoxy",
    "incarnation": "https://ccel.org/ccel/athanasius/incarnation",
    "theology1": "https://ccel.org/ccel/hodge/theology1",
}
# Some volumes (e.g. Hodge) repeat every chapter title in a table of
# contents before the real text -- searches would match the ToC line
# first. Trim everything before this marker so title-based searches only
# see the real chapter text.
VOLUME_SKIP_TOC_BEFORE = {
    "theology1": "INTRODUCTION.",
}

# (volume, title, author, start_line_marker, end_line_marker_or_None, folder, category, subcategory)
# Line markers are exact (or near-exact) text as it appears at the start of a
# line in the plain-text edition; used to find the document's boundaries.
SEED = [
    ("anf01", "The First Epistle of Clement to the Corinthians", "Clement of Rome",
     "Introductory Note to the First Epistle of Clement", "Introductory Note to the Epistle of Mathetes",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Mathetes to Diognetus", "Mathetes",
     "Introductory Note to the Epistle of Mathetes", "Introductory Note to the Epistle of Polycarp",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Polycarp to the Philippians", "Polycarp",
     "Introductory Note to the Epistle of Polycarp", "Introductory Note to the Epistle Concerning the Martyrdom",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Martyrdom of Polycarp", "Anonymous (early church)",
     "Introductory Note to the Epistle Concerning the Martyrdom", "Introductory Note to the Epistles of Ignatius",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Ephesians", "Ignatius of Antioch",
     "Introductory Note to the Epistles of Ignatius", "The Epistle of Ignatius to the Magnesians",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Magnesians", "Ignatius of Antioch",
     "The Epistle of Ignatius to the Magnesians", "The Epistle of Ignatius to the Trallians",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Trallians", "Ignatius of Antioch",
     "The Epistle of Ignatius to the Trallians", "The Epistle of Ignatius to the Romans",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Romans", "Ignatius of Antioch",
     "The Epistle of Ignatius to the Romans", "The Epistle of Ignatius to the Philadelphians",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Philadelphians", "Ignatius of Antioch",
     "The Epistle of Ignatius to the Philadelphians", "The Epistle of Ignatius to the Smyrn",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to the Smyrnaeans", "Ignatius of Antioch",
     "The Epistle of Ignatius to the Smyrn", "The Epistle of Ignatius to Polycarp",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Ignatius to Polycarp", "Ignatius of Antioch",
     "The Epistle of Ignatius to Polycarp", "Introductory Note to the Syriac Version",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Martyrdom of Ignatius", "Anonymous (early church)",
     "Introductory Note to the Martyrdom of Ignatius", "Introductory Note to the Epistle of Barnabas",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Epistle of Barnabas", "Pseudo-Barnabas",
     "Introductory Note to the Epistle of Barnabas", "Introductory Note to the Fragments of Papias",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The First Apology of Justin Martyr", "Justin Martyr",
     "Introductory Note to the Writings of Justin Martyr", "The Second Apology of Justin",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),
    ("anf01", "The Second Apology of Justin Martyr", "Justin Martyr",
     "The Second Apology of Justin for the Christians", "Dialogue of Justin, Philosopher and Martyr",
     "14-church-history-and-denominations", "church-history-and-denominations", "Patristic Theology"),

    # --- Why Christianity: G.K. Chesterton, Orthodoxy (1908) ---
    ("orthodoxy", "Introduction in Defence of Everything Else", "G.K. Chesterton",
     "I. INTRODUCTION IN DEFENCE", "II. THE MANIAC",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Maniac", "G.K. Chesterton",
     "II. THE MANIAC", "III. THE SUICIDE OF THOUGHT",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Suicide of Thought", "G.K. Chesterton",
     "III. THE SUICIDE OF THOUGHT", "IV. THE ETHICS OF ELFLAND",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Ethics of Elfland", "G.K. Chesterton",
     "IV. THE ETHICS OF ELFLAND", "V. THE FLAG OF THE WORLD",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Flag of the World", "G.K. Chesterton",
     "V. THE FLAG OF THE WORLD", "VI. THE PARADOXES OF CHRISTIANITY",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Paradoxes of Christianity", "G.K. Chesterton",
     "VI. THE PARADOXES OF CHRISTIANITY", "VII. THE ETERNAL REVOLUTION",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Eternal Revolution", "G.K. Chesterton",
     "VII. THE ETERNAL REVOLUTION", "VIII. THE ROMANCE OF ORTHODOXY",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "The Romance of Orthodoxy", "G.K. Chesterton",
     "VIII. THE ROMANCE OF ORTHODOXY", "IX. AUTHORITY AND THE ADVENTURER",
     "15-why-christianity", "why-christianity", None),
    ("orthodoxy", "Authority and the Adventurer", "G.K. Chesterton",
     "IX. AUTHORITY AND THE ADVENTURER", None,
     "15-why-christianity", "why-christianity", None),

    # --- Who Is Christ: Athanasius, On the Incarnation ---
    ("incarnation", "On the Incarnation: Creation and the Fall", "Athanasius",
     "Chapter 1", "Chapter 2",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: The Divine Dilemma and Its Solution", "Athanasius",
     "Chapter 2", "Chapter 3",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: The Divine Dilemma, Continued", "Athanasius",
     "Chapter 3", "Chapter 4",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: The Death of Christ", "Athanasius",
     "Chapter 4", "Chapter 5",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: The Resurrection", "Athanasius",
     "Chapter 5", "Chapter 6",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: Refutation of the Jews", "Athanasius",
     "Chapter 6", "Chapter 7",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: Refutation of the Gentiles", "Athanasius",
     "Chapter 7", "Chapter 8",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: Refutation of the Gentiles, Continued", "Athanasius",
     "Chapter 8", "Chapter 9",
     "16-who-is-christ", "who-is-christ", None),
    ("incarnation", "On the Incarnation: Conclusion", "Athanasius",
     "Chapter 9", None,
     "16-who-is-christ", "who-is-christ", None),

    # --- Systematic Theology: Charles Hodge, Systematic Theology Vol. I ---
    ("theology1", "On Method", "Charles Hodge",
     "ON METHOD", "THEOLOGY", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Nature of Theology", "Charles Hodge",
     "THEOLOGY", "RATIONALISM", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Protestant Rule of Faith", "Charles Hodge",
     "THE PROTESTANT RULE OF FAITH", "PART I.", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Origin of the Idea of God", "Charles Hodge",
     "ORIGIN OF THE IDEA OF GOD", "THEISM.", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "Theism", "Charles Hodge",
     "THEISM.", "ANTI-THEISTIC THEORIES", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Knowledge of God", "Charles Hodge",
     "THE KNOWLEDGE OF GOD", "NATURE AND ATTRIBUTES OF GOD", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Nature and Attributes of God: The Divine Being", "Charles Hodge",
     "NATURE AND ATTRIBUTES OF GOD", "§ 8. Knowledge.", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Nature and Attributes of God: Knowledge, Will, Power, and Moral Perfections", "Charles Hodge",
     "§ 8. Knowledge.", "The Trinity.", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Trinity", "Charles Hodge",
     "The Trinity.", "THE DIVINITY OF CHRIST", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Divinity of Christ", "Charles Hodge",
     "THE DIVINITY OF CHRIST", "THE HOLY SPIRIT", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Holy Spirit", "Charles Hodge",
     "THE HOLY SPIRIT", "THE DECREES OF GOD", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "The Decrees of God", "Charles Hodge",
     "THE DECREES OF GOD", "CREATION.", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "Creation", "Charles Hodge",
     "CREATION.", "PROVIDENCE", "17-systematic-theology", "systematic-theology", None),
    ("theology1", "Providence", "Charles Hodge",
     "PROVIDENCE", "MIRACLES", "17-systematic-theology", "systematic-theology", None),
]

IGNATIUS_LETTERS = [
    "The Epistle of Ignatius to the Ephesians",
    "The Epistle of Ignatius to the Magnesians",
    "The Epistle of Ignatius to the Trallians",
    "The Epistle of Ignatius to the Romans",
    "The Epistle of Ignatius to the Philadelphians",
    "The Epistle of Ignatius to the Smyrnaeans",
    "The Epistle of Ignatius to Polycarp",
]
SERIES_PART = {title: (i + 1) for i, title in enumerate(IGNATIUS_LETTERS)}
SERIES_NAME = {title: "The Epistles of Ignatius" for title in IGNATIUS_LETTERS}


def log_error(doc, reason):
    with open(ERRORS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{doc}\t{reason}\n")
    print(f"    ERROR: {doc} - {reason}", flush=True)


def fetch_volume(volume):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"{volume}.txt")
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()
    resp = SESSION.get(VOLUME_URL[volume], timeout=60)
    resp.raise_for_status()
    text = resp.content.decode("utf-8")
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


RULE_RE = re.compile(r"^ {5}_{20,}\s*$")
FOOTNOTE_LINE_RE = re.compile(r"^\s*\[\d+\]")
INLINE_REF_RE = re.compile(r"\s?\[\d+\]")
CHAPTER_RE = re.compile(r"^\s*Chapter\s+([IVXLCDM]+)\.--(.+)$", re.IGNORECASE)
# CCEL's internal per-document marker, e.g.:
# "justin_martyr first_apology anf01 justin_martyr-first_apology The First
#  Apology http://www.ccel.org/ccel/schaff/anf01.viii.ii.html"
CCEL_MARKER_RE = re.compile(r"^\s*[a-z][a-z_]*(?:\s+[a-z][a-z_]*){2,}.*ccel\.org\S*\s*$")


def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def find_line(lines, marker, start=0):
    for i in range(start, len(lines)):
        if lines[i].strip().startswith(marker):
            return i
    return None


def extract_markdown(lines):
    """Split on horizontal-rule lines into blocks; drop footnote-only
    blocks; unwrap remaining paragraphs; convert Chapter headers."""
    blocks = []
    current = []
    for line in lines:
        if RULE_RE.match(line):
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)

    out_paragraphs = []
    for block in blocks:
        stripped = [l for l in block if l.strip()]
        if not stripped:
            continue

        # unwrap into paragraphs on blank lines within the block
        paras = []
        para_lines = []
        for line in block:
            if not line.strip():
                if para_lines:
                    paras.append(" ".join(l.strip() for l in para_lines))
                    para_lines = []
            else:
                para_lines.append(line)
        if para_lines:
            paras.append(" ".join(l.strip() for l in para_lines))

        for p in paras:
            if FOOTNOTE_LINE_RE.match(p):
                continue  # standalone "[123] footnote text" paragraph
            if CCEL_MARKER_RE.match(p) and "ccel.org" in p:
                continue  # internal slug/URL marker line
            p = INLINE_REF_RE.sub("", p).strip()
            if not p:
                continue
            m = CHAPTER_RE.match(p)
            if m:
                out_paragraphs.append(f"## Chapter {m.group(1)}. {m.group(2).strip()}")
                continue
            # a paragraph entirely wrapped in one set of brackets is an
            # editorial/translator aside in this text convention -- keep
            # the text, drop the cosmetic brackets
            if p.startswith("[") and p.endswith("]") and p.count("[") == 1:
                p = p[1:-1].strip()
            out_paragraphs.append(p)

    return "\n\n".join(out_paragraphs)


def scrape_one(volume, title, author, start_marker, end_marker, folder, category, subcategory):
    doc_label = title
    try:
        text = fetch_volume(volume)
        lines = text.split("\n")
        if volume in VOLUME_SKIP_TOC_BEFORE:
            marker = VOLUME_SKIP_TOC_BEFORE[volume]
            # exact (non-stripped) match -- the marker also appears
            # indented inside the table of contents itself
            skip_idx = next((i for i, l in enumerate(lines) if l == marker), None)
            if skip_idx is not None:
                lines = lines[skip_idx:]

        start_idx = find_line(lines, start_marker)
        if start_idx is None:
            log_error(doc_label, f"start marker not found: {start_marker!r}")
            return False

        if end_marker:
            end_idx = find_line(lines, end_marker, start=start_idx + 1)
            if end_idx is None:
                log_error(doc_label, f"end marker not found: {end_marker!r}")
                return False
        else:
            end_idx = len(lines)

        md_content = extract_markdown(lines[start_idx:end_idx])
        if len(md_content) < 400:
            log_error(doc_label, "extracted content too short")
            return False

        slug = slugify(title)
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "christian-theology",
            "category": category,
            "source": VOLUME_SOURCE_PAGE.get(volume, f"https://ccel.org/ccel/schaff/{volume}.html"),
            "author": author,
            "sourceName": SOURCE_NAME,
            "wordCount": word_count,
            "readTime": max(1, round(word_count / 200)),
            "license": LICENSE,
        }
        if subcategory:
            frontmatter["subcategory"] = subcategory
        if title in SERIES_NAME:
            frontmatter["series"] = SERIES_NAME[title]
            frontmatter["part"] = SERIES_PART[title]

        folder_path = os.path.join(CONTENT_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slug}.md")

        fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n{md_content}\n")

        print(f"  OK  {category} / {slug}.md ({word_count} words)", flush=True)
        return True
    except Exception as e:
        log_error(doc_label, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} documents from CCEL...")
    ok = 0
    for volume, title, author, start_marker, end_marker, folder, category, subcategory in SEED:
        if scrape_one(volume, title, author, start_marker, end_marker, folder, category, subcategory):
            ok += 1
        time.sleep(0.2)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
