#!/usr/bin/env python3
"""
Categorize blog posts into sub-categories by analyzing their titles.
Reads each .md file, matches the title against keyword rules,
and writes a 'subcategory' field into the YAML frontmatter.
"""

import os
import re
import sys

BLOG_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "islam", "13-blog-posts")

# Church father names used for patristic detection
CHURCH_FATHERS = [
    "augustine", "origen", "irenaeus", "tertullian", "athanasius",
    "cyril", "gregory", "basil", "ambrose", "hippolytus", "aphrahat",
    "chrysostom", "jerome", "clement", "polycarp", "ignatius",
    "justin", "eusebius", "epiphanius", "theodoret", "didymus",
    "hilary", "amphilochi", "diognetus", "theophilus", "athenagoras",
    "barnabas", "hermas", "papias", "lactantius", "ambrosiaster",
    "novatian", "cyprian", "methodius", "rufinus", "maximus",
    "damascene", "bernard", "leo ", "anselm",
]

# Named Muslim debaters/authors for rebuttals detection
NAMED_OPPONENTS = [
    "hijab", "badawi", "deedat", "qadhi", "rashid", "zawadi",
    "zaatari", "osama abdallah", "shabir ally", "bassam",
    "naik", "jalal", "sami zaatari", "taqiyyist",
]

RULES = [
    # Order matters: first match wins. More specific rules come first.

    ("Rebuttals & Debates", [
        # Named opponents
        *NAMED_OPPONENTS,
        "debate", "rebuttal", "response to",
        "turning the tables",
    ]),

    ("Holy Spirit", [
        "holy spirit", "paraclete", "filioque", "pneumatology",
        "spirit of god", "spirit is god", "spirit as god",
        "biblical witness to the deity of the holy spirit",
    ]),

    ("Atonement & Salvation", [
        "atonement", "justification", "vicarious", "scapegoat",
        "sin-offering", "sin offering", "soteriology",
        "limited atonement", "saved by", "salvation",
        "imputation", "almsgiving", "faithfulness",
        "faith ", "faithful obedience",
        "justified by", "baptismal", "baptism",
        "water baptism",
    ]),

    ("Patristic Theology", [
        *CHURCH_FATHERS,
        "ante-nicene", "ante nicene", "nicene",
        "church father", "patristic",
        "muratorian", "apostolic succession",
        "early church",
    ]),

    ("Church & Sacraments", [
        "mary ", "mary:", "mary'", "marian",
        "queen mother", "virgin's womb",
        "saints", "veneration", "icons",
        "catholic", "orthodox",
        "sacrament", "eucharist",
        "communion of saints", "theosis",
        "catechism",
    ]),

    ("Trinity & Godhead", [
        "trinity", "triune", "trinitarian",
        "two powers", "godhead", "echad",
        "uni-plurality", "divine council",
        "divine name christology",
        "plurals for god", "plurals",
        "three gods", "tritheism",
        "filioque",
        "monotheism",
        "monarchi",
    ]),

    ("Christology", [
        "christ", "christolog", "christos",
        "son of man", "son of god",
        "deity of jesus", "jesus is god", "jesus as god",
        "worship jesus", "worshiping jesus", "worshipping jesus",
        "incarnation", "incarnate", "pre-existence", "prehuman",
        "hypostatic union", "two natures",
        "messiah", "messianic",
        "nwt ", "nwt'",
        "uncreated word", "word becomes",
        "logos", "theos",
        "jesus", "deity of",
        "jehovah", "yhwh", "yahweh",
        "arian", "unitarian",
        "ancient of days",
        "angel of the lord", "great angel",
        "god-man",
    ]),

    ("Biblical Studies", [
        "torah", "targum", "lxx", "apocrypha",
        "genesis", "isaiah", "deuteronomy", "psalm",
        "proverbs", "daniel", "hebrews ",
        "corinthians", "thessalonians",
        "matthew", "luke-acts", "acts ",
        "prophecy", "prophecie", "prophetic",
        "canon", "canonicity",
        "bible error", "bible errors",
        "biblical", "scripture",
        "ot evidence", "old testament",
        "new testament", "gospel",
        "revelation", "enoch",
        "septuagint", "vulgate",
        "wisdom of solomon", "sirach",
        "elohim",
        "solomon", "david ",
        "abraham", "isaac", "jacob",
        "moses", "balaam",
        "israel", "seed that",
        "satan ", "satan:", "satan'",
        "kjv ", "sharp's",
    ]),

    ("Quranic Analysis", [
        "quran", "qur'an", "quranic", "sura",
        "variant", "recitation",
    ]),

    ("Muhammad & Islam", [
        "muhammad", "prophet of shirk",
        "allah", "hadith", "aisha",
        "islam", "muslim", "mormonism", "mormon",
        "hubal", "baal", "umma",
        "sharia", "taqiyy",
        "caliph", "abu hanifa",
        "sunnah", "sunni", "shia",
        "arabic", "syriac",
        "bukhari",
    ]),
]


def classify_title(title: str) -> str:
    t = title.lower()
    for category, keywords in RULES:
        for kw in keywords:
            if kw.lower() in t:
                return category
    return "General Topics"


def process_file(filepath: str) -> str | None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    end_idx = content.index("---", 3)
    frontmatter = content[3:end_idx]
    body = content[end_idx:]

    # Extract title from frontmatter
    title_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?\s*$", frontmatter, re.MULTILINE)
    if not title_match:
        return None

    title = title_match.group(1)
    subcategory = classify_title(title)

    # Remove existing subcategory if present
    frontmatter = re.sub(r"\nsubcategory:.*\n", "\n", frontmatter)

    # Add subcategory before the closing ---
    frontmatter = frontmatter.rstrip("\n") + f"\nsubcategory: {subcategory}\n"

    new_content = "---" + frontmatter + body
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return subcategory


def main():
    if not os.path.isdir(BLOG_DIR):
        print(f"Blog directory not found: {BLOG_DIR}")
        sys.exit(1)

    files = sorted(f for f in os.listdir(BLOG_DIR) if f.endswith(".md"))
    counts: dict[str, int] = {}
    total = 0

    for filename in files:
        filepath = os.path.join(BLOG_DIR, filename)
        subcat = process_file(filepath)
        if subcat:
            counts[subcat] = counts.get(subcat, 0) + 1
            total += 1

    print(f"\nCategorized {total} blog posts:\n")
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:30s}  {count:>4d}")
    print(f"  {'TOTAL':30s}  {total:>4d}")


if __name__ == "__main__":
    main()
