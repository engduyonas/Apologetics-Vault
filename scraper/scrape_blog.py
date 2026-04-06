#!/usr/bin/env python3
"""
Comprehensive scraper for ALL samshmnthelogy.net blog posts.
Reads slugs from all_blog_slugs.txt (extracted from fully-scrolled HTML)
and also discovers new posts from inter-post links.
"""

import os
import re
import time
import yaml
import html2text
import requests
from bs4 import BeautifulSoup
from categories import CATEGORY_FOLDER_MAP, slugify, detect_series

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")
BLOG_FOLDER = os.path.join(CONTENT_DIR, CATEGORY_FOLDER_MAP["blog-posts"])
SLUGS_FILE = os.path.join(os.path.dirname(__file__), "all_blog_slugs.txt")
BASE = "https://www.samshmnthelogy.net/post/"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 0.6


def setup_h2t():
    h = html2text.HTML2Text()
    h.body_width = 0
    h.unicode_snob = True
    h.protect_links = True
    h.wrap_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    return h


def load_seed_slugs():
    slugs = set()
    if os.path.exists(SLUGS_FILE):
        with open(SLUGS_FILE) as f:
            for line in f:
                s = line.strip()
                if s:
                    slugs.add(s)
    print(f"Loaded {len(slugs)} seed slugs from {SLUGS_FILE}", flush=True)
    return slugs


def extract_post_links(html_text):
    slugs = set()
    for match in re.findall(r'/post/([a-z0-9][-a-z0-9]*)', html_text):
        if len(match) > 3:
            slugs.add(match)
    return slugs


def fetch_and_save(slug):
    url = BASE + slug

    try:
        resp = SESSION.get(url, timeout=25)
        if resp.status_code != 200:
            return None, set()

        linked = extract_post_links(resp.text)

        soup = BeautifulSoup(resp.text, "lxml")

        for tag in soup.find_all(["script", "style", "nav", "iframe"]):
            tag.decompose()

        title = slug.replace("-", " ").title()

        page_title = soup.find("title")
        if page_title:
            pt = page_title.get_text(strip=True)
            pt = re.sub(r"\s*\|\s*Theology Sphere.*$", "", pt).strip()
            if pt and len(pt) > 5:
                title = pt

        h1 = soup.find("h1")
        if h1:
            h1t = h1.get_text(strip=True)
            if h1t and len(h1t) > 3:
                title = h1t

        content_el = (
            soup.find("article") or
            soup.find("div", {"data-mesh-id": True}) or
            soup.find("main") or
            soup.find("body")
        )

        if not content_el:
            return None, linked

        converter = setup_h2t()
        md = converter.handle(str(content_el))
        md = re.sub(r"\n{4,}", "\n\n\n", md).strip()

        if len(md) < 100:
            return None, linked

        word_count = len(md.split())
        series_name, part = detect_series(title)

        fm = {
            "title": title,
            "slug": slugify(title),
            "category": "blog-posts",
            "source": url,
        }
        if series_name:
            fm["series"] = series_name
            fm["part"] = part
        fm["wordCount"] = word_count
        fm["readTime"] = max(1, round(word_count / 200))

        file_slug = fm["slug"]
        if not file_slug:
            file_slug = slugify(slug)
        file_path = os.path.join(BLOG_FOLDER, f"{file_slug}.md")
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(BLOG_FOLDER, f"{file_slug}-{counter}.md")
            counter += 1

        fm_str = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n{md}\n")

        return fm, linked

    except Exception as e:
        return None, set()


def main():
    os.makedirs(BLOG_FOLDER, exist_ok=True)

    for f in os.listdir(BLOG_FOLDER):
        if f.endswith(".md"):
            os.remove(os.path.join(BLOG_FOLDER, f))
    print("Cleared existing blog posts\n", flush=True)

    all_slugs = load_seed_slugs()
    processed = set()
    saved = 0
    failed = 0

    wave = 0
    while True:
        wave += 1
        to_process = sorted(all_slugs - processed)
        if not to_process:
            break

        print(f"\n=== Wave {wave}: {len(to_process)} posts to process ===", flush=True)

        for i, slug in enumerate(to_process):
            processed.add(slug)
            total = saved + failed + 1
            pct = total / max(len(all_slugs), 1) * 100
            print(f"  [{total}/{len(all_slugs)}] ({pct:.0f}%) {slug[:60]}...", end="", flush=True)

            result, linked = fetch_and_save(slug)

            new_found = linked - all_slugs
            all_slugs.update(linked)

            if result:
                saved += 1
                print(f" OK ({result['wordCount']}w)", end="", flush=True)
            else:
                failed += 1
                print(f" FAIL", end="", flush=True)

            if new_found:
                print(f" [+{len(new_found)} new]", end="", flush=True)

            print("", flush=True)
            time.sleep(DELAY)

    print(f"\n{'='*60}", flush=True)
    print(f"COMPLETE!", flush=True)
    print(f"  Saved: {saved}", flush=True)
    print(f"  Failed: {failed}", flush=True)
    print(f"  Total slugs discovered: {len(all_slugs)}", flush=True)
    print(f"  Blog folder: {BLOG_FOLDER}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()
