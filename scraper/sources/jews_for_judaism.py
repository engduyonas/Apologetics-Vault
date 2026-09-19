#!/usr/bin/env python3
"""
Scraper for a curated set of Judaism articles from jewsforjudaism.org
(Judaism tradition pilot content — Jewish responses to Christian
missionary/messianic-prophecy claims, Talmudic defense, and Jewish
theology, from a counter-missionary organization staffed by rabbis).

No explicit reuse/copyright statement is posted on the site (checked the
article pages and footer); this is the same "ambiguous, not explicit
permission" posture as most of this project's other ministry-site
sources, treated the same informal way per the project owner's direction.

Works from a fixed, hand-vetted seed list — same pattern as the other
sources/ scrapers.

Run: python3 sources/jews_for_judaism.py
"""

import os
import re
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "judaism")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://jewsforjudaism.org/knowledge/articles/"
SOURCE_NAME = "Jews for Judaism"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (slug, category folder, category slug, subcategory)
SEED = [
    ("isaiah-53-jesus-not-suffering-servant", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-teaches-jesus-not-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("the-truth-about-psalms-22-17", "01-messianic-prophecy", "messianic-prophecy", None),
    ("rabbinic-commentators-rashi-isaiah-53", "01-messianic-prophecy", "messianic-prophecy", None),
    ("rabbi-moshe-al-sheich-isaiah-53", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel-9-verse-by-verse", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel-9-problem-with-christian-interpretative-credibility", "01-messianic-prophecy", "messianic-prophecy", None),

    ("new-testament-refutations-trinity-doctrine-part-1", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-2", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("three-divine-echoes-singularity-plurality-oneness", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("oneness-of-god-the-meaning-of-elohim", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("a-remarkable-discovery-two-paths-to-one-god", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("israels-god-real-know", "02-trinity-and-monotheism", "trinity-and-monotheism", None),

    ("defending-the-talmud-against-centuries-of-misinterpretation", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("biblical-basis-rabbinic-authority", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("what-are-the-jewish-holy-books", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("answering-dr-brown-s-objections-to-judaism", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),

    ("does-the-death-of-the-righteous-atone", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("sin-sacrifices-and-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("finding-substitutes-for-sacrifice", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("blood-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("the-dimensions-of-sin-and-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),

    ("who-was-jesus", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jewish-people-rejected-christian-messiah", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("you-are-my-witnesses-a-traditional-response-to-missionaries", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("you-turn-the-jewish-response-to-a-christian-challenge", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("journey-home-judaism-part-1", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
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
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    md = converter.handle(html_content)
    return re.sub(r"\n{4,}", "\n\n\n", md).strip()


def scrape_one(page_slug, folder, category, subcategory):
    url = BASE_URL + page_slug
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else page_slug

        author_el = soup.find(class_="post-author")
        author = author_el.get_text(strip=True) if author_el else "Jews for Judaism"

        content = soup.find(class_="post-wrapper")
        if not content:
            log_error(url, "No .post-wrapper found")
            return False

        # drop the PDF-download link list and share/like icon rows
        for tag in content.find_all("ul"):
            if tag.find("a", href=re.compile(r"active_storage/blobs")):
                tag.decompose()

        md_content = html_to_markdown(str(content))
        if len(md_content) < 200:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title) or page_slug
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "judaism",
            "category": category,
            "source": url,
            "author": author,
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

        print(f"  OK  {category} / {slug}.md ({word_count} words, {author})", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from Jews for Judaism...")
    ok = 0
    for page_slug, folder, category, subcategory in SEED:
        if scrape_one(page_slug, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
