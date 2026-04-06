"""Category mapping and slug utilities for article organization."""

import re
import unicodedata

CATEGORIES = {
    "answers-to-common-questions": {
        "order": 1,
        "title": "Answers to Common Questions",
        "description": "Responses to frequently asked questions and common claims about Christianity and Islam.",
        "icon": "help-circle",
    },
    "christological-issues": {
        "order": 2,
        "title": "Christological Issues",
        "description": "The deity, nature, and identity of Jesus Christ examined from biblical and Islamic perspectives.",
        "icon": "crown",
    },
    "theological-issues": {
        "order": 3,
        "title": "Theological Issues",
        "description": "The Trinity, monotheism, the nature of God, and comparative theology.",
        "icon": "book-open",
    },
    "biblical-issues": {
        "order": 4,
        "title": "Biblical Issues",
        "description": "Biblical inspiration, canon, textual criticism, and scriptural authority.",
        "icon": "book",
    },
    "quranic-issues": {
        "order": 5,
        "title": "Quranic Issues",
        "description": "Analysis of Quranic claims, contradictions, textual history, and theological problems.",
        "icon": "scroll",
    },
    "analysis-of-muhammad": {
        "order": 6,
        "title": "Analysis of Muhammad",
        "description": "Examination of Muhammad's character, teachings, prophecies, and historical record.",
        "icon": "user",
    },
    "hadith-analysis": {
        "order": 7,
        "title": "Hadith Analysis",
        "description": "Examination of the hadith literature, its cosmology, and fantastical claims.",
        "icon": "file-text",
    },
    "polemical-issues": {
        "order": 8,
        "title": "Polemical Issues",
        "description": "Cross-topic debates on Abraham, the Holy Spirit, atonement, and ethical comparisons.",
        "icon": "message-square",
    },
    "general-issues": {
        "order": 9,
        "title": "General Issues",
        "description": "Women in Islam, tolerance, historical analysis, and broad comparative topics.",
        "icon": "globe",
    },
    "responses-to-authors": {
        "order": 10,
        "title": "Responses to Muslim Authors",
        "description": "Rebuttals and responses to specific Muslim scholars, speakers, and debaters.",
        "icon": "users",
    },
    "turning-the-tables": {
        "order": 11,
        "title": "Turning the Tables",
        "description": "Series applying Muslim argumentation standards back to Islamic sources.",
        "icon": "rotate-ccw",
    },
    "short-summaries": {
        "order": 12,
        "title": "Short Summaries",
        "description": "Concise summary articles on key theological points.",
        "icon": "align-left",
    },
    "blog-posts": {
        "order": 13,
        "title": "Blog Posts",
        "description": "Recent blog posts from Theology Sphere covering patristic theology and advanced topics.",
        "icon": "pen-tool",
    },
}

# Maps section header text found in the HTML to category slugs
SECTION_TO_CATEGORY_OLD = {
    "A Series of Answers to Common Questions and Claims": "answers-to-common-questions",
    "General Issues": "general-issues",
    "Theological Issues": "theological-issues",
    "Christological Issues": "christological-issues",
    "Quranic Issues": "quranic-issues",
    "Analysis of Muhammad": "analysis-of-muhammad",
    "Analysis of the Hadith Literature": "hadith-analysis",
    "Polemical Issues": "polemical-issues",
    "Debate Challenges": "general-issues",
    "Debate Material": "general-issues",
}

SECTION_TO_CATEGORY_NEW = {
    "Answers to Common Questions and Claims by Muslims": "answers-to-common-questions",
    "Short summary articles": "short-summaries",
    "Turning the Tables": "turning-the-tables",
    "Christological Issues": "christological-issues",
    "Theological Issues": "theological-issues",
    "Biblical Issues": "biblical-issues",
    "Quranic Issues": "quranic-issues",
    "Analysis of Muhammad": "analysis-of-muhammad",
    "Responses to Muslim authors, speakers and debaters": "responses-to-authors",
}

CATEGORY_FOLDER_MAP = {
    "answers-to-common-questions": "01-answers-to-common-questions",
    "christological-issues": "02-christological-issues",
    "theological-issues": "03-theological-issues",
    "biblical-issues": "04-biblical-issues",
    "quranic-issues": "05-quranic-issues",
    "analysis-of-muhammad": "06-analysis-of-muhammad",
    "hadith-analysis": "07-hadith-analysis",
    "polemical-issues": "08-polemical-issues",
    "general-issues": "09-general-issues",
    "responses-to-authors": "10-responses-to-authors",
    "turning-the-tables": "11-turning-the-tables",
    "short-summaries": "12-short-summaries",
    "blog-posts": "13-blog-posts",
}


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text[:120]


def detect_series(title: str):
    """Returns (series_name, part_label) or (None, None)."""
    patterns = [
        (r"^(.*?)\s*[\[\(]?\s*(?:Part|Pt\.?)\s+(\d+[a-z]?)\s*[\]\)]?\s*$", None),
        (r"^(.*?)\s*[\[\(]?\s*(?:Part|Pt\.?)\s+([A-C])\s*[\]\)]?\s*$", None),
        (r"^(.*?)\s*[\[\(]?\s*(?:Addendum|Appendix)\s*([A-Z]?)?\s*[\]\)]?\s*$", "addendum"),
        (r"^(.*?)\s*[\[\(]?\s*(?:Excursus)\s*[\]\)]?\s*$", "excursus"),
        (r"^(.*?)\s*[\[\(]?\s*(?:Postscript)\s*[\]\)]?\s*$", "postscript"),
    ]
    for pattern, default_part in patterns:
        match = re.match(pattern, title, re.IGNORECASE)
        if match:
            series = match.group(1).strip().rstrip("-\u2013\u2014:").strip()
            if match.lastindex and match.lastindex >= 2 and match.group(2):
                part = match.group(2)
            else:
                part = default_part or "1"
            return series, part
    return None, None
