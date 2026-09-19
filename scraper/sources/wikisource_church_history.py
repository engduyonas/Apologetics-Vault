#!/usr/bin/env python3
"""
Scraper for a curated set of Church History & Denominations articles from
Wikisource (Catholic Encyclopedia 1913, 1911 Encyclopaedia Britannica).

Both source works are public domain (pre-1923 publication); Wikisource's
own transcription/markup is separately CC BY-SA, which is noted in each
article's `license` field for transparency even though we're reproducing
the underlying PD text. This works from a fixed, hand-vetted seed list
rather than crawling — same pattern as sources/access_to_insight.py.

Run: python3 sources/wikisource_church_history.py
"""

import os
import re
import time
import urllib.parse

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "..", "content", "christian-theology"
)
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://en.wikisource.org/wiki/"
FOLDER = "14-church-history-and-denominations"
CATEGORY = "church-history-and-denominations"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

LICENSE_NOTE = (
    "Original text published {year} and in the public domain in the United States. "
    "Wikisource's transcription/formatting is separately available under the Creative "
    "Commons Attribution-ShareAlike License."
)

# (display title, Wikisource page title, subcategory, publication year)
SEED = [
    ("The Papacy", "Catholic Encyclopedia (1913)/Pope", "Roman Catholic", 1913),
    ("Purgatory", "Catholic Encyclopedia (1913)/Purgatory", "Roman Catholic", 1913),
    ("The Council of Trent", "Catholic Encyclopedia (1913)/Council of Trent", "Roman Catholic", 1913),
    ("The Immaculate Conception", "Catholic Encyclopedia (1913)/Immaculate Conception", "Roman Catholic", 1913),
    ("The Sacraments", "Catholic Encyclopedia (1913)/Sacraments", "Roman Catholic", 1913),
    ("Papal Infallibility", "Catholic Encyclopedia (1913)/Infallibility", "Roman Catholic", 1913),
    ("The Real Presence of Christ in the Eucharist", "Catholic Encyclopedia (1913)/The Real Presence of Christ in the Eucharist", "Roman Catholic", 1913),
    ("Indulgences", "Catholic Encyclopedia (1913)/Indulgences", "Roman Catholic", 1913),

    ("The Orthodox Eastern Church", "1911 Encyclopædia Britannica/Orthodox Eastern Church", "Eastern Orthodox", 1911),
    ("The Orthodox Church", "Catholic Encyclopedia (1913)/Orthodox Church", "Eastern Orthodox", 1913),
    ("The Eastern Schism", "Catholic Encyclopedia (1913)/The Eastern Schism", "Eastern Orthodox", 1913),

    ("The Council of Chalcedon", "1911 Encyclopædia Britannica/Chalcedon, Council of", "Oriental Orthodox & Christological Councils", 1911),
    ("The Monophysites", "1911 Encyclopædia Britannica/Monophysites", "Oriental Orthodox & Christological Councils", 1911),
    ("Nestorius", "1911 Encyclopædia Britannica/Nestorius", "Oriental Orthodox & Christological Councils", 1911),
    ("The Nestorians", "1911 Encyclopædia Britannica/Nestorians", "Oriental Orthodox & Christological Councils", 1911),

    ("The Reformation", "1911 Encyclopædia Britannica/Reformation, The", "Protestant Reformation & Denominations", 1911),
    ("Martin Luther", "1911 Encyclopædia Britannica/Luther, Martin", "Protestant Reformation & Denominations", 1911),
    ("John Calvin", "1911 Encyclopædia Britannica/Calvin, John", "Protestant Reformation & Denominations", 1911),
    ("The Anglican Communion", "1911 Encyclopædia Britannica/Anglican Communion", "Protestant Reformation & Denominations", 1911),
    ("The Baptists", "1911 Encyclopædia Britannica/Baptists", "Protestant Reformation & Denominations", 1911),
    ("Methodism", "1911 Encyclopædia Britannica/Methodism", "Protestant Reformation & Denominations", 1911),
    ("Presbyterianism", "1911 Encyclopædia Britannica/Presbyterianism", "Protestant Reformation & Denominations", 1911),
    ("The Reformed Churches", "1911 Encyclopædia Britannica/Reformed Churches", "Protestant Reformation & Denominations", 1911),

    ("The Council of Nicaea", "1911 Encyclopædia Britannica/Nicaea, Council of", "Ecumenical Councils", 1911),
    ("The Council of Ephesus", "1911 Encyclopædia Britannica/Ephesus, Council of", "Ecumenical Councils", 1911),
    ("The Councils of Constantinople", "1911 Encyclopædia Britannica/Constantinople, Councils of", "Ecumenical Councils", 1911),
    ("Church History: An Overview", "1911 Encyclopædia Britannica/Church History", "Ecumenical Councils", 1911),
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


NOISE_CLASS_RE = re.compile(r"ws-noexport|ws-header|noprint|printfooter|mw-editsection")


def scrape_one(display_title, page_title, subcategory, year):
    url = BASE_URL + urllib.parse.quote(page_title.replace(" ", "_"))
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        contributor = soup.find(class_="contributor-text")
        if contributor:
            raw = contributor.get_text().replace("\xa0", " ")
            author = re.sub(r"\s+", " ", raw).strip()
            author = re.sub(r"^by\s+", "", author)
        else:
            author = "Unknown"
        if not author:
            author = "Unknown"

        content = soup.find(id="mw-content-text")
        if not content:
            log_error(url, "No #mw-content-text found")
            return False

        for tag in content.find_all(["style", "script"]):
            tag.decompose()
        for tag in content.find_all(class_=NOISE_CLASS_RE):
            tag.decompose()

        md_content = html_to_markdown(str(content))
        if len(md_content) < 200:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(display_title)
        word_count = len(md_content.split())
        source_name = "Catholic Encyclopedia (1913)" if "Catholic Encyclopedia" in page_title else "1911 Encyclopædia Britannica"

        frontmatter = {
            "title": display_title,
            "slug": slug,
            "tradition": "christian-theology",
            "category": CATEGORY,
            "source": url,
            "author": author,
            "sourceName": source_name,
            "wordCount": word_count,
            "readTime": max(1, round(word_count / 200)),
            "subcategory": subcategory,
            "license": LICENSE_NOTE.format(year=year),
        }

        folder_path = os.path.join(CONTENT_DIR, FOLDER)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{slug}.md")

        fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n# {display_title}\n\n{md_content}\n")

        print(f"  OK  {subcategory} / {slug}.md ({word_count} words, {author})", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from Wikisource...")
    ok = 0
    for display_title, page_title, subcategory, year in SEED:
        if scrape_one(display_title, page_title, subcategory, year):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
