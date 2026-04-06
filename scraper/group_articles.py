#!/usr/bin/env python3
"""
Assign standalone articles (those without a series) to either an existing
series or a new topical group, by analysing title keyword overlap.

For each content folder that has subcategories:
  1. Collect existing series names per subcategory.
  2. For each standalone article, try to match it to an existing series
     using significant-word overlap in the title.
  3. For remaining unmatched articles, cluster them by common keywords
     and assign meaningful group names.
  4. Write `series` and `part` fields back to the YAML frontmatter.
"""

import os
import re
import sys
from collections import defaultdict

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

STOP_WORDS = {
    "a", "an", "the", "of", "in", "on", "to", "and", "or", "for", "is",
    "it", "its", "by", "as", "at", "from", "with", "that", "this", "be",
    "are", "was", "were", "been", "being", "has", "have", "had", "do",
    "does", "did", "but", "not", "so", "if", "no", "nor", "up", "out",
    "his", "her", "he", "she", "they", "them", "we", "our", "their",
    "more", "most", "some", "than", "into", "can", "all", "s", "vs",
    "pt", "part", "vol", "i", "ii", "iii", "iv", "v", "vi",
}

# Per-subcategory keyword -> group name mappings for clustering unmatched articles
TOPIC_CLUSTERS = {
    # Christological subcategories
    "Christ's Deity & Identity": [
        ("John & Johannine Theology", ["john 1", "john 8", "john 5", "john 10", "john 17", "john 20", "johannine", "logos"]),
        ("Incarnation & Two Natures", ["incarnat", "two natures", "god-man", "god incarnate", "human nature", "divine nature"]),
        ("Hebrews Christology", ["hebrews", "melchizedek"]),
        ("Pauline Christology", ["paul", "colossians", "philippians", "romans 9", "corinthians", "galatians", "ephesians"]),
        ("Omniscience & Attributes", ["omnisci", "omnipoten", "omnipres", "attribute", "all-knowing"]),
        ("Eternal Sonship", ["eternal son", "eternal generation", "sonship", "son of god", "begotten"]),
        ("Servant & Lord", ["servant", "lord", "kurios"]),
        ("Trinitarian Defense", ["trinit", "triune", "anti-trinitarian", "unitarian"]),
        ("Deity in the Gospels", ["gospel", "synoptic", "matthew", "mark", "luke"]),
        ("Responding to Critics", ["response", "rebuttal", "refut", "objection", "reply", "answer", "scholar"]),
        ("Names & Titles of Christ", ["name", "title", "alpha", "omega", "first and last", "almighty", "i am"]),
    ],
    "Messianic Prophecies": [
        ("Psalmic Prophecies", ["psalm"]),
        ("Isaiah & the Messiah", ["isaiah"]),
        ("Daniel & Prophecy", ["daniel"]),
        ("Messiah in Jewish Literature", ["rabbinic", "jewish", "inter-testamental", "talmud", "midrash"]),
        ("Resurrection Prophecies", ["resurrect", "third day", "risen"]),
        ("Davidic Prophecies", ["david", "seed of"]),
        ("Shepherd & King", ["shepherd", "king"]),
    ],
    "Christ in the Quran": [
        ("Badawi Responses", ["badawi"]),
        ("Islamic View of Jesus", ["islam", "muslim", "quran", "qur'an"]),
    ],
    "NT Christology": [
        ("Gospel Studies", ["gospel", "mark", "luke", "matthew", "john"]),
        ("Apostolic Christology", ["james", "jude", "peter", "paul"]),
    ],
    "Worship of Christ": [
        ("OT Worship", ["old testament", "ot ", "hebrew"]),
        ("NT Worship", ["new testament", "nt ", "latreuo", "carmen"]),
    ],
    "Son of Man & Preexistence": [
        ("Preexistence", ["preexist", "pre-exist", "pre-incarnate"]),
        ("Son of Man", ["son of man", "daniel"]),
    ],
    "Shema & Monotheism": [
        ("Shema Studies", ["shema"]),
        ("Monotheism & Plurality", ["uniplural", "monothe", "binitarian"]),
    ],

    # Theological subcategories
    "Nature of Allah": [
        ("Allah's Attributes", ["attribute", "names of", "al-"]),
        ("Allah & Deception", ["decei", "deceiv", "makr", "liar"]),
        ("Allah & Morality", ["moral", "evil", "sin"]),
    ],
    "Trinity & Monotheism": [
        ("Biblical Trinity", ["biblical", "scripture", "genesis", "ot "]),
        ("Patristic Trinity", ["father", "church father", "patristic", "nicene"]),
        ("Responding to Objections", ["objection", "response", "refut", "rebuttal"]),
    ],
    "Islamic Theology Critiqued": [
        ("Tawhid & Shirk", ["tawhid", "shirk", "monotheism"]),
        ("Predestination & Free Will", ["predestination", "free will", "qadr"]),
    ],
    "Salvation & Eschatology": [
        ("Atonement", ["atonement", "atone", "sacrifice", "blood"]),
        ("Intercession", ["intercession", "interced"]),
        ("Eschatology", ["judgment", "hell", "paradise", "afterlife"]),
    ],
    "OT Theology": [
        ("Genesis Studies", ["genesis"]),
        ("Prophetic Books", ["isaiah", "jeremiah", "ezekiel", "daniel"]),
    ],

    # Quranic subcategories
    "Theology of the Quran": [
        ("Allah in the Quran", ["allah"]),
        ("Quranic Monotheism", ["monothe", "tawhid", "shirk"]),
    ],
    "Contradictions & Errors": [
        ("Scientific Errors", ["scien", "earth", "flat", "sun"]),
        ("Historical Errors", ["histor", "anachroni"]),
        ("Internal Contradictions", ["contradict"]),
    ],
    "Quran & the Bible": [
        ("Gospel in the Quran", ["gospel", "injil"]),
        ("Torah in the Quran", ["torah", "tawrat", "moses"]),
    ],
    "Quran Stories & Figures": [
        ("Mary in the Quran", ["mary", "maryam"]),
        ("Abraham in the Quran", ["abraham", "ibrahim"]),
    ],

    # Analysis of Muhammad subcategories
    "Deification of Muhammad": [
        ("Muhammad's Exaltation", ["exalt", "praise", "honor", "glorif"]),
        ("Muhammad as Intercessor", ["intercess"]),
    ],
    "Character & Morality": [
        ("Violence & Warfare", ["violen", "war", "fight", "kill", "battle", "sword"]),
        ("Honesty & Integrity", ["honest", "lie", "lying", "liar", "decei", "oath"]),
        ("Treatment of Others", ["slave", "captive", "prisoner", "enemy"]),
    ],
    "Muhammad's Wives & Marriages": [
        ("Aisha", ["aisha", "ayesha"]),
        ("Zainab", ["zainab", "zaynab"]),
        ("Multiple Wives", ["wives", "marriage", "polygam"]),
    ],
    "False Prophecies": [
        ("Failed Predictions", ["predict", "prophec", "foretold", "fulfilled"]),
    ],

    # General issues subcategories
    "Rebuttals & Debates": [
        ("Named Opponents", ["hijab", "deedat", "naik", "zawadi", "zaatari", "ally"]),
    ],
    "Women in Islam": [
        ("Women's Rights", ["right", "status", "equal"]),
        ("Veiling & Modesty", ["veil", "hijab", "modest"]),
    ],

    # Blog subcategories
    "Christology": [
        ("Deity of Christ", ["deity", "divine", "god"]),
        ("Humanity of Christ", ["human", "nature"]),
    ],
    "Trinity & Godhead": [
        ("Biblical Basis", ["biblic", "scripture"]),
        ("Patristic Views", ["father", "patristic", "nicene", "council"]),
    ],
    "Holy Spirit": [
        ("Personhood", ["person", "he ", "personal"]),
        ("Deity", ["deity", "divine", "god"]),
    ],
    "Patristic Theology": [
        ("Early Church", ["early", "ante-nicene", "apostolic"]),
        ("Councils & Creeds", ["council", "creed", "nicene", "chalcedon"]),
    ],
    "Biblical Studies": [
        ("Old Testament", ["old testament", "hebrew bible", "ot ", "genesis", "exodus"]),
        ("New Testament", ["new testament", "nt ", "gospel", "epistle"]),
    ],
    "Quranic Analysis": [
        ("Textual Issues", ["text", "manuscrip", "variant"]),
        ("Theological Issues", ["theolog", "contradict"]),
    ],
    "Muhammad & Islam": [
        ("Character", ["character", "moral", "conduct"]),
        ("Claims", ["claim", "prophet", "prophec"]),
    ],
}


def extract_words(text):
    """Extract significant words from a title."""
    text = text.lower()
    text = re.sub(r"[''`]", "'", text)
    text = re.sub(r"[^a-z0-9' ]", " ", text)
    words = text.split()
    return {w for w in words if w not in STOP_WORDS and len(w) > 1}


def title_similarity(title_words, series_words):
    """Score overlap between article title and series name."""
    if not series_words:
        return 0
    overlap = title_words & series_words
    return len(overlap)


def read_frontmatter(filepath):
    """Read YAML frontmatter as raw text + body."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", content, re.S)
    if not m:
        return None, content
    return m.group(1), m.group(2)


def get_field(fm_text, field):
    """Extract a field value from raw frontmatter text."""
    for line in fm_text.split("\n"):
        if line.startswith(f"{field}:"):
            val = line.split(":", 1)[1].strip()
            return val.strip("'\"")
    return None


def set_field(fm_text, field, value):
    """Set or add a field in raw frontmatter text."""
    needs_quotes = any(c in value for c in ":{}[],'\"&*?|>!%@`#")
    quoted = f"'{value}'" if needs_quotes else value

    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith(f"{field}:"):
            lines[i] = f"{field}: {quoted}"
            return "\n".join(lines)
    lines.append(f"{field}: {quoted}")
    return "\n".join(lines)


def write_frontmatter(filepath, fm_text, body):
    """Write back frontmatter + body."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"---\n{fm_text}\n---\n{body}")


def process_folder(folder_path):
    """Process all articles in a folder."""
    files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
    if not files:
        return 0

    articles = []
    for fname in files:
        fpath = os.path.join(folder_path, fname)
        fm, body = read_frontmatter(fpath)
        if fm is None:
            continue
        title = get_field(fm, "title") or fname
        series = get_field(fm, "series")
        subcategory = get_field(fm, "subcategory") or ""
        articles.append({
            "path": fpath,
            "fname": fname,
            "fm": fm,
            "body": body,
            "title": title,
            "series": series,
            "subcategory": subcategory,
        })

    by_subcat = defaultdict(list)
    for a in articles:
        by_subcat[a["subcategory"]].append(a)

    updated = 0

    for subcat, sub_articles in by_subcat.items():
        series_articles = [a for a in sub_articles if a["series"]]
        standalone = [a for a in sub_articles if not a["series"]]

        if not standalone:
            continue

        series_names = list({a["series"] for a in series_articles})
        series_word_map = {s: extract_words(s) for s in series_names}

        # Step 1: match standalone to existing series
        unmatched = []
        for a in standalone:
            title_words = extract_words(a["title"])
            best_series = None
            best_score = 0

            for sname, swords in series_word_map.items():
                score = title_similarity(title_words, swords)
                if score > best_score:
                    best_score = score
                    best_series = sname

            if best_score >= 2 and best_series:
                existing_parts = [
                    sa for sa in series_articles if sa["series"] == best_series
                ]
                max_part = 0
                for sa in existing_parts:
                    p = get_field(sa["fm"], "part") or "0"
                    try:
                        max_part = max(max_part, int(re.sub(r"[^0-9]", "", p) or "0"))
                    except ValueError:
                        pass

                part_num = str(max_part + 1)
                a["fm"] = set_field(a["fm"], "series", best_series)
                a["fm"] = set_field(a["fm"], "part", part_num)
                write_frontmatter(a["path"], a["fm"], a["body"])
                a["series"] = best_series
                series_articles.append(a)
                updated += 1
            else:
                unmatched.append(a)

        # Step 2: cluster unmatched by topic keywords
        if not unmatched:
            continue

        cluster_rules = TOPIC_CLUSTERS.get(subcat, [])
        still_unmatched = []

        cluster_counters = defaultdict(int)
        for a in unmatched:
            title_lower = a["title"].lower()
            assigned = False

            for group_name, keywords in cluster_rules:
                if any(kw in title_lower for kw in keywords):
                    cluster_counters[group_name] += 1
                    a["fm"] = set_field(a["fm"], "series", group_name)
                    a["fm"] = set_field(a["fm"], "part", str(cluster_counters[group_name]))
                    write_frontmatter(a["path"], a["fm"], a["body"])
                    updated += 1
                    assigned = True
                    break

            if not assigned:
                still_unmatched.append(a)

        # Step 3: group remaining by shared significant words
        if len(still_unmatched) >= 2:
            word_to_articles = defaultdict(list)
            for a in still_unmatched:
                for w in extract_words(a["title"]):
                    if len(w) >= 4:
                        word_to_articles[w].append(a)

            grouped = set()
            clusters = []
            sorted_words = sorted(
                word_to_articles.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )

            for word, word_articles in sorted_words:
                cluster_articles = [
                    a for a in word_articles if id(a) not in grouped
                ]
                if len(cluster_articles) >= 2:
                    group_name = f"{word.capitalize()} Studies"
                    clusters.append((group_name, cluster_articles))
                    for a in cluster_articles:
                        grouped.add(id(a))

            for group_name, cluster_articles in clusters:
                for i, a in enumerate(cluster_articles, 1):
                    a["fm"] = set_field(a["fm"], "series", group_name)
                    a["fm"] = set_field(a["fm"], "part", str(i))
                    write_frontmatter(a["path"], a["fm"], a["body"])
                    updated += 1

    return updated


def main():
    if not os.path.isdir(CONTENT_DIR):
        print(f"Content directory not found: {CONTENT_DIR}")
        sys.exit(1)

    folders = sorted(
        f
        for f in os.listdir(CONTENT_DIR)
        if os.path.isdir(os.path.join(CONTENT_DIR, f))
    )

    total = 0
    for folder in folders:
        folder_path = os.path.join(CONTENT_DIR, folder)
        count = process_folder(folder_path)
        if count > 0:
            print(f"  {folder}: grouped {count} articles")
        total += count

    print(f"\nTotal: {total} articles grouped")


if __name__ == "__main__":
    main()
