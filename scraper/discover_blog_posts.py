#!/usr/bin/env python3
"""
Use Playwright to scroll through the Wix infinite-scroll blog
and discover all post URLs.
"""

import json
import os
import time
from playwright.sync_api import sync_playwright

BLOG_URL = "https://www.samshmnthelogy.net/blog"
OUTPUT = os.path.join(os.path.dirname(__file__), "blog_slugs.json")


def discover_all_posts():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Loading {BLOG_URL}...", flush=True)
        page.goto(BLOG_URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)

        all_slugs = set()
        prev_count = 0
        stale_rounds = 0

        for scroll_round in range(200):
            links = page.query_selector_all('a[href*="/post/"]')
            for link in links:
                href = link.get_attribute("href") or ""
                if "/post/" in href:
                    slug = href.rstrip("/").split("/post/")[-1]
                    if slug:
                        all_slugs.add(slug)

            current_count = len(all_slugs)
            print(f"  Scroll {scroll_round + 1}: found {current_count} unique posts so far", flush=True)

            if current_count == prev_count:
                stale_rounds += 1
                if stale_rounds >= 5:
                    print("  No new posts after 5 scrolls, stopping.", flush=True)
                    break
            else:
                stale_rounds = 0

            prev_count = current_count

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

        browser.close()

    sorted_slugs = sorted(all_slugs)
    print(f"\nTotal unique posts discovered: {len(sorted_slugs)}", flush=True)

    with open(OUTPUT, "w") as f:
        json.dump(sorted_slugs, f, indent=2)
    print(f"Saved to {OUTPUT}", flush=True)

    return sorted_slugs


if __name__ == "__main__":
    slugs = discover_all_posts()
    for s in slugs:
        print(f"  https://www.samshmnthelogy.net/post/{s}")
