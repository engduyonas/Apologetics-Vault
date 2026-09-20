#!/usr/bin/env python3
"""
Scraper for a curated set of essays from the Secular Web (infidels.org),
the flagship atheism/secularism library run by Internet Infidels. Builds
the new Atheism & Secularism tradition: nontheistic arguments, critiques
of theistic arguments, secular ethics, agnosticism, biblical criticism
from a skeptical angle, and church-state/society issues.

Copyright posture (checked https://infidels.org/contact-us/copyright/,
2026-09-20): "The contents of the Secular Web may not be reproduced
without the express written consent of the acting President of the
Internet Infidels." The page goes on to say Internet Infidels
"generally grant[s] permission to groups with similar aims who wish to
reprint or distribute materials ... so long as ... the material is not
sold for profit, and the following notice is included": a line pointing
back to https://infidels.org/. This is the most explicit no-reproduction
notice of any source in this project (contrast the ambiguous-but-silent
posture of Jews for Judaism/FAIR) -- proceeding anyway per the project
owner's explicit direction, given full knowledge of the restriction.
Each document's own end-of-article copyright notice (e.g. "Copyright
(c)2000 Keith Parsons...") is captured verbatim into the `license`
frontmatter field, matching the Access to Insight pattern of recording
per-document terms rather than asserting one blanket license.

WordPress site: article body lives in div.entry-content. Author bylines
are individual (unlike the collaboratively-wiki-edited FAIR/Wikisource
sources), so `author` is the credited essay author, not the org.

Run: python3 sources/secular_web.py
"""

import os
import re
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "atheism-secularism")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

SOURCE_NAME = "Secular Web (Internet Infidels)"
ATTRIBUTION_NOTICE = "This article is available at the Secular Web: https://infidels.org/"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (url path, title override or None, author, folder, category slug, subcategory)
SEED = [
    ("library/modern/atheism-and-society/", None, "Doug Krueger", "01-arguments-for-atheism", "arguments-for-atheism", None),
    ("library/modern/is-atheism-a-faith/", None, "Internet Infidels", "01-arguments-for-atheism", "arguments-for-atheism", None),
    ("library/modern/seven-common-misconceptions-about-atheism/", None, "Keith M. Parsons", "01-arguments-for-atheism", "arguments-for-atheism", None),
    ("library/modern/keith-parsons-twilight/", "Atheism: Twilight or Dawn?", "Keith M. Parsons", "01-arguments-for-atheism", "arguments-for-atheism", None),
    ("library/historical/percy-shelley-necessity-of-atheism/", "The Necessity of Atheism", "Percy Bysshe Shelley", "01-arguments-for-atheism", "arguments-for-atheism", None),

    ("library/modern/keith-parsons-varghese/", "No Creator Need Apply: A Reply to Roy Abraham Varghese", "Keith M. Parsons", "02-critiques-of-theistic-arguments", "critiques-of-theistic-arguments", None),
    ("library/modern/a-simple-statement-of-the-problem-of-evil/", None, "Internet Infidels", "02-critiques-of-theistic-arguments", "critiques-of-theistic-arguments", None),
    ("library/modern/keith-parsons-hume-on-miracles/", "Hume's Beautiful Argument", "Keith M. Parsons", "02-critiques-of-theistic-arguments", "critiques-of-theistic-arguments", None),
    ("library/modern/the-argument-from-reason/", None, "Internet Infidels", "02-critiques-of-theistic-arguments", "critiques-of-theistic-arguments", None),
    ("library/modern/edouard-tahmizian-the-origin-of-evil/", "The Origin of Evil", "Edouard Tahmizian", "02-critiques-of-theistic-arguments", "critiques-of-theistic-arguments", None),

    ("library/modern/keith-parsons-whymoral/", "Why Be Moral?", "Keith M. Parsons", "03-secular-ethics-and-morality", "secular-ethics-and-morality", None),
    ("library/modern/aristotelian-naturalism/", "Neo-Aristotelian Ethical Naturalism", "Keith M. Parsons", "03-secular-ethics-and-morality", "secular-ethics-and-morality", None),
    ("library/modern/do-atheists-bear-a-burden-of-proof-a-reply-to-prof-ralph-mcinerny/", None, "Internet Infidels", "03-secular-ethics-and-morality", "secular-ethics-and-morality", None),

    ("library/modern/weak-agnosticism-defended/", None, "Theodore M. Drange", "04-faith-reason-and-agnosticism", "faith-reason-and-agnosticism", None),
    ("library/modern/is-faith-a-path-to-knowledge/", None, "Internet Infidels", "04-faith-reason-and-agnosticism", "faith-reason-and-agnosticism", None),
    ("library/modern/constructing-a-logical-argument/", "Logic FAQ", "Internet Infidels", "04-faith-reason-and-agnosticism", "faith-reason-and-agnosticism", None),

    ("library/modern/donald-morgan-contradictions/", "Bible Inconsistencies: Bible Contradictions?", "Donald Morgan", "05-biblical-criticism", "biblical-criticism", None),
    ("library/modern/best-selling-errancy-an-essay-on-inconsistencies-in-the-bible/", None, "Internet Infidels", "05-biblical-criticism", "biblical-criticism", None),
    ("library/modern/what-is-a-gospel/", None, "Internet Infidels", "05-biblical-criticism", "biblical-criticism", None),
    ("library/modern/the-arguments-from-confusion-and-biblical-defects/", None, "Internet Infidels", "05-biblical-criticism", "biblical-criticism", None),

    ("library/modern/the-christian-nation-myth/", None, "Internet Infidels", "06-church-state-and-society", "church-state-and-society", None),
    ("library/modern/keith-parsons-kingdom/", "Review of Kingdom Coming", "Keith M. Parsons", "06-church-state-and-society", "church-state-and-society", None),

    ("library/modern/keith-augustine-immortality/", "The Case Against Immortality", "Keith Augustine", "07-death-mind-and-the-afterlife", "death-mind-and-the-afterlife", None),
    ("library/modern/nde-historian-answers-critic/", None, "Internet Infidels", "07-death-mind-and-the-afterlife", "death-mind-and-the-afterlife", None),
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
    text = text.replace("/", " ")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    md = converter.handle(html_content)
    return re.sub(r"\n{4,}", "\n\n\n", md).strip()


COPYRIGHT_RE = re.compile(r"copyright\s*[©c]", re.I)


def extract_license(paragraphs):
    """The per-document copyright notice is conventionally the final
    paragraph(s) of entry-content, starting with a "Copyright ..." line."""
    for i in range(len(paragraphs) - 1, max(-1, len(paragraphs) - 4), -1):
        text = paragraphs[i].strip()
        if text and COPYRIGHT_RE.search(text):
            return text
    return None


def scrape_one(path, title_override, author, folder, category, subcategory):
    url = "https://infidels.org/" + path
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        h1 = soup.find("h1")
        title = title_override or (h1.get_text(strip=True) if h1 else path.rstrip("/").rsplit("/", 1)[-1])

        byline = soup.select_one(".author.vcard a")
        actual_author = byline.get_text(strip=True) if byline else author

        content = soup.select_one(".entry-content")
        if not content:
            log_error(url, "No .entry-content found")
            return False

        for tag in content.find_all(["style", "script", "form"]):
            tag.decompose()

        paragraph_texts = [p.get_text(" ", strip=True) for p in content.find_all(["p", "div"], recursive=False)]
        if not paragraph_texts:
            paragraph_texts = [p.get_text(" ", strip=True) for p in content.find_all("p")]
        license_notice = extract_license(paragraph_texts)

        md_content = html_to_markdown(str(content))
        if len(md_content) < 400:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title)
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "atheism-secularism",
            "category": category,
            "source": url,
            "author": actual_author,
            "sourceName": SOURCE_NAME,
            "wordCount": word_count,
            "readTime": max(1, round(word_count / 200)),
        }
        if subcategory:
            frontmatter["subcategory"] = subcategory
        if license_notice:
            frontmatter["license"] = f"{license_notice} {ATTRIBUTION_NOTICE}"
        else:
            frontmatter["license"] = ATTRIBUTION_NOTICE

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
    print(f"Scraping {len(SEED)} pages from the Secular Web...")
    ok = 0
    for path, title_override, author, folder, category, subcategory in SEED:
        if scrape_one(path, title_override, author, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
