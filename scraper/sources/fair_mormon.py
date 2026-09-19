#!/usr/bin/env python3
"""
Scraper for a curated set of Mormonism/LDS apologetics articles from
fairlatterdaysaints.org (FAIR — Foundation for Apologetic Information and
Research), a pro-LDS apologetics organization. Expands the Mormonism
tradition beyond the 3 articles that landed there incidentally during the
Islam/Christian Theology split.

MediaWiki site (standard #mw-content-text extraction, same pattern as the
Wikisource church-history scraper). Articles carry a standard "All Rights
Reserved" copyright notice (no explicit no-reproduction clause, same
ambiguous posture as most other ministry-site sources on this project),
and articles are collaboratively wiki-edited rather than individually
bylined, so author is recorded as the organization.

Run: python3 sources/fair_mormon.py
"""

import os
import re
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "mormonism")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://www.fairlatterdaysaints.org/answers/"
SOURCE_NAME = "FAIR (Foundation for Apologetic Information and Research)"
DEFAULT_AUTHOR = "FAIR"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (page title, category folder, category slug, subcategory)
SEED = [
    ("DNA_and_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Horses_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Hebraisms_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Chiasmus_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Book_of_Mormon_textual_changes", "02-book-of-mormon", "book-of-mormon", None),
    ("Eleven_official_witnesses_to_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Bible_passages_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),

    ("Alleged_false_prophecies_of_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_1826_trial", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Events_surrounding_the_death_of_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("1844_Succession_to_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_alleged_narcissism", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),

    ("Approaching_Anachronisms_in_the_Book_of_Abraham", "04-book-of-abraham", "book-of-abraham", None),
    ("The_Book_of_Abraham_and_the_Book_of_Genesis", "04-book-of-abraham", "book-of-abraham", None),
    ("Evidences_for_the_Book_of_Abraham%27s_Authenticity", "04-book-of-abraham", "book-of-abraham", None),

    ("1835_Doctrine_and_Covenants_denies_polygamy", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Possible_contradictions_in_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Overview_of_changes_to_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),

    ("Worship_different_Jesus", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Latter-day_Saints_and_the_symbol_of_the_cross", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("One_Nation_Under_Gods", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
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
        except Exception:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
            else:
                raise


def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = text.replace("/", " ")  # MediaWiki subpage titles like "Jesus Christ/Worship"
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    md = converter.handle(html_content)
    return re.sub(r"\n{4,}", "\n\n\n", md).strip()


NOISE_CLASS_RE = re.compile(r"^toc$|noprint|mw-editsection|printfooter")


def scrape_one(page_title, folder, category, subcategory):
    url = BASE_URL + page_title
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else page_title.replace("_", " ")

        content = soup.find(id="mw-content-text")
        if not content:
            log_error(url, "No #mw-content-text found")
            return False

        for tag in content.find_all(["style", "script"]):
            tag.decompose()
        for tag in content.find_all(class_=NOISE_CLASS_RE):
            tag.decompose()
        # drop the "< Back to FAIR Answers Index" nav link, always the first <p>/<a>
        back_link = content.find("a", string=re.compile(r"Back to FAIR", re.I))
        if back_link:
            back_link.decompose()

        md_content = html_to_markdown(str(content))
        if len(md_content) < 200:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title) or slugify(page_title)
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "mormonism",
            "category": category,
            "source": url,
            "author": DEFAULT_AUTHOR,
            "sourceName": SOURCE_NAME,
            "wordCount": word_count,
            "readTime": max(1, round(word_count / 200)),
        }
        if subcategory:
            frontmatter["subcategory"] = subcategory

        folder_path = os.path.join(CONTENT_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slug}.md")

        fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n{md_content}\n")

        print(f"  OK  {category} / {slug}.md ({word_count} words)", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from FAIR...")
    ok = 0
    for page_title, folder, category, subcategory in SEED:
        if scrape_one(page_title, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
