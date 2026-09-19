#!/usr/bin/env python3
"""
Scraper for Sam Shamoun articles from answeringislam.info and samshmnthelogy.net.
"""

import json
import os
import re
import sys
import time
import traceback
from urllib.parse import urljoin, urlparse

import html2text
import requests
import yaml
from bs4 import BeautifulSoup, NavigableString

from categories import (
    CATEGORIES,
    CATEGORY_FOLDER_MAP,
    detect_series,
    slugify,
)

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "islam")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

OLD_INDEX = "https://answeringislam.info/Shamoun/index.htm"
NEW_INDEX = "https://answeringislam.info/authors/shamoun.html"
BLOG_URL = "https://www.samshmnthelogy.net/blog"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 0.8
RETRY_COUNT = 2


def fetch(url, retries=RETRY_COUNT):
    for attempt in range(retries):
        try:
            resp = SESSION.get(url, timeout=20)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"    Retry {attempt+1} for {url}: {e}", flush=True)
                time.sleep(wait)
            else:
                raise


def normalize_url(url):
    parsed = urlparse(url)
    path = parsed.path.rstrip("/").lower()
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def setup_html2text():
    h = html2text.HTML2Text()
    h.body_width = 0
    h.unicode_snob = True
    h.protect_links = True
    h.wrap_links = False
    h.skip_internal_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    return h


# ---- OLD INDEX (Source 1) ----

OLD_INDEX_SECTIONS = [
    ("A Series of Answers to Common Questions and Claims", "answers-to-common-questions"),
    ("General Issues", "general-issues"),
    ("Theological Issues", "theological-issues"),
    ("Christological Issues", "christological-issues"),
    ("Quranic Issues", "quranic-issues"),
    ("Analysis of Muhammad", "analysis-of-muhammad"),
    ("Analysis of the Hadith Literature", "hadith-analysis"),
    ("Polemical Issues", "polemical-issues"),
    ("Debate Challenges", "general-issues"),
    ("Debate Material", "general-issues"),
]


def parse_old_index():
    print("\n=== Parsing Source 1: Old Index ===", flush=True)
    resp = fetch(OLD_INDEX)
    html = resp.text

    soup = BeautifulSoup(html, "lxml")
    body_text = soup.get_text("\n")

    section_ranges = []
    for section_name, cat_slug in OLD_INDEX_SECTIONS:
        pos = body_text.find(section_name)
        if pos >= 0:
            section_ranges.append((pos, section_name, cat_slug))

    section_ranges.sort(key=lambda x: x[0])

    all_links = soup.find_all("a", href=True)
    articles = []

    for link in all_links:
        href = link["href"]
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        if any(skip in href for skip in ["youtube.com", "wordpress.com", "answering-islam.org/Shamoun/index"]):
            continue

        title = link.get_text(strip=True)
        if not title or len(title) < 5:
            continue

        abs_url = urljoin(OLD_INDEX, href)
        if "answeringislam.info" not in abs_url and "answering-islam.org" not in abs_url:
            continue

        link_text_pos = body_text.find(title)
        if link_text_pos < 0:
            link_text_pos = 0

        cat = "general-issues"
        for i, (pos, name, slug) in enumerate(section_ranges):
            if link_text_pos >= pos:
                cat = slug

        articles.append({
            "url": abs_url,
            "title": title,
            "category": cat,
            "source_index": "old",
        })

    print(f"  Found {len(articles)} article links", flush=True)
    return articles


# ---- NEW INDEX (Source 2) ----

NEW_INDEX_SECTIONS = [
    ("Answers to Common Questions and Claims by Muslims", "answers-to-common-questions"),
    ("Short summary articles", "short-summaries"),
    ("Turning the Tables", "turning-the-tables"),
    ("Christological Issues", "christological-issues"),
    ("Theological Issues", "theological-issues"),
    ("Biblical Issues", "biblical-issues"),
    ("Quranic Issues", "quranic-issues"),
    ("Analysis of Muhammad", "analysis-of-muhammad"),
    ("Responses to Muslim authors, speakers and debaters", "responses-to-authors"),
]


def parse_new_index():
    print("\n=== Parsing Source 2: New Index ===", flush=True)
    resp = fetch(NEW_INDEX)
    soup = BeautifulSoup(resp.text, "lxml")

    body_text = soup.get_text("\n")

    section_ranges = []
    for section_name, cat_slug in NEW_INDEX_SECTIONS:
        pos = body_text.find(section_name)
        if pos >= 0:
            section_ranges.append((pos, section_name, cat_slug))

    section_ranges.sort(key=lambda x: x[0])

    all_links = soup.find_all("a", href=True)
    articles = []
    rebuttal_urls = []

    skip_texts = {"Contact Sam Shamoun", "former index page", "Youtube Channel",
                  "blog", "Paltalk", "ABN Broadcasting", "Islamic Dilemma",
                  "Does Acts", "Refutation of Yusuf"}

    for link in all_links:
        href = link["href"]
        if not href or href.startswith("#") or href.startswith("mailto:"):
            continue
        if any(skip in href for skip in ["youtube.com", "wordpress.com"]):
            continue

        title = link.get_text(strip=True)
        if not title or len(title) < 5:
            continue
        if any(s in title for s in skip_texts):
            continue

        abs_url = urljoin(NEW_INDEX, href)
        if "answeringislam.info" not in abs_url:
            continue

        # Fix doubled path: authors/authors/shamoun -> authors/shamoun
        abs_url = abs_url.replace("/authors/authors/shamoun/", "/authors/shamoun/")

        link_text_pos = body_text.find(title)
        if link_text_pos < 0:
            link_text_pos = 0

        cat = "general-issues"
        for i, (pos, name, slug) in enumerate(section_ranges):
            if link_text_pos >= pos:
                cat = slug

        if cat == "responses-to-authors" and "/rebuttals/" in abs_url and title.startswith("Rebuttals to"):
            author = title.replace("Rebuttals to ", "").strip()
            rebuttal_urls.append({"url": abs_url, "author": author})
            continue

        articles.append({
            "url": abs_url,
            "title": title,
            "category": cat,
            "source_index": "new",
        })

    print(f"  Found {len(articles)} article links", flush=True)
    print(f"  Found {len(rebuttal_urls)} rebuttal indexes to crawl", flush=True)

    return articles, rebuttal_urls


def parse_rebuttal_indexes(rebuttal_urls):
    print("\n=== Parsing Rebuttal Sub-Indexes ===", flush=True)
    articles = []

    for info in rebuttal_urls:
        url = info["url"]
        author = info["author"]
        print(f"  Crawling rebuttals to {author}...", flush=True)

        try:
            time.sleep(DELAY)
            resp = fetch(url)
            soup = BeautifulSoup(resp.text, "lxml")

            for link in soup.find_all("a", href=True):
                href = link["href"]
                if not href or href.startswith("#") or href.startswith("mailto:"):
                    continue

                title = link.get_text(strip=True)
                if not title or len(title) < 8:
                    continue

                abs_url = urljoin(url, href)
                if "answeringislam.info" not in abs_url:
                    continue
                if abs_url.rstrip("/") == url.rstrip("/"):
                    continue

                nav_words = {"home", "index", "contact", "top", "back", "next", "previous", "site topics"}
                if title.lower().strip() in nav_words:
                    continue

                articles.append({
                    "url": abs_url,
                    "title": title,
                    "category": "responses-to-authors",
                    "source_index": "rebuttal",
                    "rebuttal_to": author,
                })

            print(f"    OK", flush=True)

        except Exception as e:
            print(f"    FAILED: {e}", flush=True)
            log_error(url, e)

    print(f"  Total rebuttal articles: {len(articles)}", flush=True)
    return articles


# ---- BLOG (Source 3) ----

def parse_blog():
    print("\n=== Parsing Source 3: Blog ===", flush=True)
    articles = []

    try:
        resp = fetch(BLOG_URL)
        soup = BeautifulSoup(resp.text, "lxml")

        seen = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/post/" in href and "samshmnthelogy.net" in href:
                title = a.get_text(strip=True)
                if title and len(title) > 10:
                    abs_url = urljoin(BLOG_URL, href)
                    if abs_url not in seen:
                        seen.add(abs_url)
                        articles.append({
                            "url": abs_url,
                            "title": title,
                            "category": "blog-posts",
                            "source_index": "blog",
                        })

        print(f"  Found {len(articles)} blog posts", flush=True)

    except Exception as e:
        print(f"  ERROR: {e}", flush=True)
        log_error(BLOG_URL, e)

    return articles


# ---- ARTICLE FETCHING ----

def extract_content(soup, url):
    for tag in soup.find_all(["script", "style", "nav", "iframe"]):
        tag.decompose()

    if "samshmnthelogy.net" in url:
        content = soup.find("article") or soup.find("main") or soup.find("div", {"data-mesh-id": True})
        if content:
            return str(content)
        body = soup.find("body")
        return str(body) if body else ""

    for nav_el in soup.find_all(["table", "div"], recursive=True):
        text = nav_el.get_text(strip=True)
        if len(text) < 300 and any(kw in text for kw in ["Site Topics", "Introductory Articles", "Albanian", "Individual Authors"]):
            nav_el.decompose()

    candidates = []
    for tag in soup.find_all(["article", "main"]):
        candidates.append((len(tag.get_text()), tag))

    for tag in soup.find_all("div", {"class": re.compile(r"content|article|main|body", re.I)}):
        candidates.append((len(tag.get_text()), tag))

    for td in soup.find_all("td"):
        text_len = len(td.get_text())
        if text_len > 1000:
            candidates.append((text_len, td))

    if not candidates:
        body = soup.find("body")
        if body:
            candidates.append((len(body.get_text()), body))

    if not candidates:
        return ""

    candidates.sort(key=lambda x: x[0], reverse=True)
    return str(candidates[0][1])


def html_to_markdown(html_content):
    converter = setup_html2text()
    md = converter.handle(html_content)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    return md.strip()


def fetch_and_save(article, content_dir):
    url = article["url"]
    title = article["title"]
    category = article["category"]

    try:
        resp = fetch(url)
        if resp is None:
            return False

        soup = BeautifulSoup(resp.text, "lxml")

        page_title_tag = soup.find("title")
        if page_title_tag:
            pt = page_title_tag.get_text(strip=True)
            pt_clean = re.sub(r"\s*[-|]\s*(Answering Islam|Theology Sphere).*$", "", pt, flags=re.I).strip()
            if pt_clean and len(pt_clean) > 5:
                title = pt_clean

        html_content = extract_content(soup, url)
        if not html_content or len(html_content) < 100:
            log_error(url, "Content too short")
            return False

        md_content = html_to_markdown(html_content)
        if len(md_content) < 50:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title)
        if not slug:
            slug = slugify(url.split("/")[-1].replace(".html", ""))
        if not slug:
            log_error(url, "Could not derive a slug (non-ASCII title and URL)")
            return False

        series_name, part = detect_series(title)

        if "answeringislam.info" in url:
            source_name = "Answering Islam"
        elif "samshmnthelogy.net" in url:
            source_name = "Theology Sphere"
        else:
            source_name = "Answering Islam"

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "islam",
            "category": category,
            "source": url,
            "author": "Sam Shamoun",
            "sourceName": source_name,
        }
        if series_name:
            frontmatter["series"] = series_name
            frontmatter["part"] = part
        if article.get("rebuttal_to"):
            frontmatter["rebuttal_to"] = article["rebuttal_to"]

        word_count = len(md_content.split())
        frontmatter["wordCount"] = word_count
        frontmatter["readTime"] = max(1, round(word_count / 200))

        folder = CATEGORY_FOLDER_MAP.get(category, "09-general-issues")
        folder_path = os.path.join(content_dir, folder)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{slug}.md")
        counter = 1
        while os.path.exists(file_path):
            slug = f"{slugify(title)}-{counter}"
            file_path = os.path.join(folder_path, f"{slug}.md")
            counter += 1
        frontmatter["slug"] = slug

        fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{fm_str}---\n\n{md_content}\n")

        return True

    except Exception as e:
        log_error(url, e)
        return False


# ---- INDEX ----

def generate_index(content_dir):
    print("\n=== Generating index.json ===", flush=True)
    index = []

    for folder in sorted(os.listdir(content_dir)):
        folder_path = os.path.join(content_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        for filename in sorted(os.listdir(folder_path)):
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read(2000)

            fm_match = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
            if not fm_match:
                continue

            try:
                fm = yaml.safe_load(fm_match.group(1))
            except Exception:
                continue

            index.append({
                "title": fm.get("title", ""),
                "slug": fm.get("slug", filename.replace(".md", "")),
                "category": fm.get("category", ""),
                "folder": folder,
                "filename": filename,
                "series": fm.get("series"),
                "part": fm.get("part"),
                "rebuttal_to": fm.get("rebuttal_to"),
                "wordCount": fm.get("wordCount", 0),
                "readTime": fm.get("readTime", 0),
                "source": fm.get("source", ""),
            })

    with open(os.path.join(content_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"  Generated index with {len(index)} entries", flush=True)


def log_error(url, error):
    with open(ERRORS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{url}\t{error}\n")


# ---- MAIN ----

def main():
    if os.path.exists(ERRORS_LOG):
        os.remove(ERRORS_LOG)

    for folder in CATEGORY_FOLDER_MAP.values():
        os.makedirs(os.path.join(CONTENT_DIR, folder), exist_ok=True)

    all_articles = []

    old = parse_old_index()
    all_articles.extend(old)

    new, rebuttal_urls = parse_new_index()
    all_articles.extend(new)

    rebuttals = parse_rebuttal_indexes(rebuttal_urls)
    all_articles.extend(rebuttals)

    blog = parse_blog()
    all_articles.extend(blog)

    # Deduplicate, prefer Source 2 ("new") over Source 1 ("old")
    print(f"\n=== Deduplicating {len(all_articles)} total links ===", flush=True)
    seen = {}
    unique = []
    for art in all_articles:
        key = normalize_url(art["url"])
        if key not in seen:
            seen[key] = len(unique)
            unique.append(art)
        else:
            existing_idx = seen[key]
            if art["source_index"] == "new" and unique[existing_idx]["source_index"] == "old":
                unique[existing_idx] = art

    print(f"  {len(unique)} unique articles", flush=True)

    # Category breakdown
    cat_counts = {}
    for a in unique:
        cat_counts[a["category"]] = cat_counts.get(a["category"], 0) + 1
    print("\n  Category breakdown:", flush=True)
    for cat, count in sorted(cat_counts.items()):
        print(f"    {cat}: {count}", flush=True)

    print(f"\n=== Fetching {len(unique)} articles ===", flush=True)
    success = 0
    failed = 0

    for i, article in enumerate(unique):
        pct = (i + 1) / len(unique) * 100
        short_title = article["title"][:60]
        print(f"  [{i+1}/{len(unique)}] ({pct:.0f}%) [{article['category'][:15]}] {short_title}...", flush=True)

        ok = fetch_and_save(article, CONTENT_DIR)
        if ok:
            success += 1
        else:
            failed += 1

        time.sleep(DELAY)

    generate_index(CONTENT_DIR)

    print(f"\n{'='*60}", flush=True)
    print(f"DONE! Saved: {success}, Failed: {failed}", flush=True)
    print(f"Content: {CONTENT_DIR}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()
