#!/usr/bin/env python3
"""
Scraper for a curated set of Theravada Buddhist texts from accesstoinsight.org
(Eastern Traditions pilot content).

Unlike scrape.py (which crawls an author's full article index), this works
from a fixed, hand-vetted seed list — accesstoinsight.org is a large site
with several differently-structured content namespaces (tipitaka suttas,
lib/authors essays, lib/thai teacher pages, etc.), and each page carries its
own per-document copyright/license notice in a structured HTML comment
("ATIDoc metadata dump"). This script parses that comment for AUTHOR,
MY_TITLE, and the license notice (DERIVED_LICENSE_DATA), and extracts the
page body from the #COPYRIGHTED_TEXT_CHUNK div.

Run: python3 sources/access_to_insight.py
"""

import html
import os
import re
import sys
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "eastern-traditions")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://accesstoinsight.org"
SOURCE_NAME = "Access to Insight"
DEFAULT_AUTHOR = "Access to Insight"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (path, category folder, category slug, subcategory or None)
SEED = [
    ("lib/study/truths", "01-core-teachings", "core-teachings", None),
    ("lib/authors/bodhi/waytoend", "01-core-teachings", "core-teachings", None),
    ("lib/authors/bodhi/abhiman", "01-core-teachings", "core-teachings", None),

    ("lib/authors/thanissaro/breathmed", "02-meditation-and-mental-development", "meditation-and-mental-development", None),
    ("lib/authors/thanissaro/painhelp", "02-meditation-and-mental-development", "meditation-and-mental-development", None),
    ("lib/authors/thanissaro/guided", "02-meditation-and-mental-development", "meditation-and-mental-development", None),
    ("lib/authors/nyanaponika/wheel026", "02-meditation-and-mental-development", "meditation-and-mental-development", None),

    ("lib/authors/thanissaro/precepts", "03-ethics-and-conduct", "ethics-and-conduct", None),
    ("lib/authors/thanissaro/refuge", "03-ethics-and-conduct", "ethics-and-conduct", None),
    ("lib/study/nonviolence", "03-ethics-and-conduct", "ethics-and-conduct", None),
    ("lib/study/conversation", "03-ethics-and-conduct", "ethics-and-conduct", None),
    ("lib/authors/khantipalo/wheel206", "03-ethics-and-conduct", "ethics-and-conduct", None),

    ("lib/study/kamma", "04-kamma-and-rebirth", "kamma-and-rebirth", None),

    ("lib/authors/thanissaro/notself2", "05-not-self-and-liberation", "not-self-and-liberation", None),
    ("lib/authors/thanissaro/nibbana", "05-not-self-and-liberation", "not-self-and-liberation", None),
    ("lib/authors/thanissaro/wings", "05-not-self-and-liberation", "not-self-and-liberation", None),

    ("tipitaka/sn/sn56/sn56.011.than", "06-sutta-translations", "sutta-translations", "Samyutta Nikaya"),
    ("tipitaka/sn/sn22/sn22.059.than", "06-sutta-translations", "sutta-translations", "Samyutta Nikaya"),
    ("tipitaka/kn/dhp/dhp.11.than", "06-sutta-translations", "sutta-translations", "Khuddaka Nikaya"),
    ("tipitaka/mn/mn.010.than", "06-sutta-translations", "sutta-translations", "Majjhima Nikaya"),
    ("tipitaka/an/an04/an04.036.than", "06-sutta-translations", "sutta-translations", "Anguttara Nikaya"),
    ("tipitaka/dn/dn.22.0.than", "06-sutta-translations", "sutta-translations", "Digha Nikaya"),

    ("tipitaka/vin/index", "07-monastic-life-and-the-sangha", "monastic-life-and-the-sangha", None),
    ("tipitaka/vin/sv/index", "07-monastic-life-and-the-sangha", "monastic-life-and-the-sangha", None),

    ("lib/thai/lee/eyeof", "08-teachers-and-traditions", "teachers-and-traditions", None),
    ("lib/thai/chah/index", "08-teachers-and-traditions", "teachers-and-traditions", None),
    ("lib/thai/index", "08-teachers-and-traditions", "teachers-and-traditions", None),
    ("lib/thai/fuang/index", "08-teachers-and-traditions", "teachers-and-traditions", None),
]


def log_error(url, reason):
    with open(ERRORS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{url}\t{reason}\n")
    print(f"    ERROR: {url} - {reason}", flush=True)


def fetch(url, retries=2):
    for attempt in range(retries):
        try:
            resp = SESSION.get(url, timeout=20)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def extract_atidoc_field(raw_html: str, field: str) -> str:
    """Extract the first {...} block after [FIELD]= in the ATIDoc metadata comment."""
    m = re.search(rf"\[{field}\]=\s*\n?\{{(.*?)\}}", raw_html, re.DOTALL)
    if not m:
        return ""
    text = m.group(1)
    text = re.sub(r"<[^>]+>", "", text)  # strip embedded HTML tags/links
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    md = converter.handle(html_content)
    return re.sub(r"\n{4,}", "\n\n\n", md).strip()


def scrape_one(path, folder, category, subcategory):
    url = f"{BASE_URL}/{path}.html"
    try:
        resp = fetch(url)
        raw_html = resp.text
        soup = BeautifulSoup(raw_html, "lxml")

        title = extract_atidoc_field(raw_html, "MY_TITLE")
        if not title:
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else path

        author = extract_atidoc_field(raw_html, "AUTHOR") or DEFAULT_AUTHOR
        license_text = extract_atidoc_field(raw_html, "DERIVED_LICENSE_DATA")

        content_div = soup.find(id="COPYRIGHTED_TEXT_CHUNK")
        if not content_div:
            log_error(url, "No #COPYRIGHTED_TEXT_CHUNK found")
            return False

        md_content = html_to_markdown(str(content_div))
        if len(md_content) < 50:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title) or slugify(path.split("/")[-1])
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "eastern-traditions",
            "category": category,
            "source": url,
            "author": author,
            "sourceName": SOURCE_NAME,
            "wordCount": word_count,
            "readTime": max(1, round(word_count / 200)),
        }
        if subcategory:
            frontmatter["subcategory"] = subcategory
        if license_text:
            frontmatter["license"] = license_text

        folder_path = os.path.join(CONTENT_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slug}.md")

        fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n{md_content}\n")

        print(f"  OK  {category}/{slug}.md ({word_count} words)", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from Access to Insight...")
    ok = 0
    for path, folder, category, subcategory in SEED:
        if scrape_one(path, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")
    if ok < len(SEED):
        sys.exit(1)


if __name__ == "__main__":
    main()
