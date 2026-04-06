# Shamoun Study Library

A structured study library of Sam Shamoun's articles on Christian theology, Christology, and comparative religion with Islam. Includes a Python scraper to collect articles and a Next.js course-style reading site.

## Sources

- **answeringislam.info/Shamoun/index.htm** -- Old article index (~150 articles)
- **answeringislam.info/authors/shamoun.html** -- New article index (~450 articles)
- **samshmnthelogy.net/blog** -- Theology Sphere blog posts

## Quick Start

### 1. Run the Scraper

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scraper/requirements.txt
python scraper/scrape.py
```

This scrapes all articles, converts them to markdown, and saves them in `content/` organized by category. Takes ~10-15 minutes with rate limiting.

### 2. Start the Site

```bash
cd site
npm install
npm run dev
```

Visit **http://localhost:3000** to browse the library.

## Project Structure

```
answers/
  scraper/           -- Python scraper
    scrape.py        -- Main scraper script
    categories.py    -- Category definitions and utilities
    requirements.txt
  content/           -- Scraped markdown articles (generated)
    01-answers-to-common-questions/
    02-christological-issues/
    03-theological-issues/
    04-biblical-issues/
    05-quranic-issues/
    06-analysis-of-muhammad/
    07-hadith-analysis/
    08-polemical-issues/
    09-general-issues/
    10-responses-to-authors/
    11-turning-the-tables/
    12-short-summaries/
    13-blog-posts/
    index.json       -- Article metadata index
  site/              -- Next.js reading site
    app/             -- App Router pages
    components/      -- React components
    lib/             -- Content utilities
```

## Features

- 700+ articles organized into 13 categories
- Series detection with prev/next navigation
- Full-text search across all articles
- Auto-generated table of contents per article
- Reading progress bar
- Dark/light mode
- Mobile responsive with collapsible sidebar
- Estimated read time per article
