#!/usr/bin/env python3
"""
Scraper for a curated set of Mormonism/LDS apologetics articles from
fairlatterdaysaints.org (FAIR — Foundation for Apologetic Information and
Research), a pro-LDS apologetics organization. Expands the Mormonism
tradition beyond the 3 articles that landed there incidentally during the
Islam/Christian Theology split.

MediaWiki site (standard #mw-content-text extraction, same pattern as the
Wikisource church-history scraper). Articles carry a standard "All Rights
Reserved" copyright notice (no explicit no-reproduction clause, same
ambiguous posture as most other ministry-site sources on this project),
and articles are collaboratively wiki-edited rather than individually
bylined, so author is recorded as the organization.

Run: python3 sources/fair_mormon.py
"""

import os
import re
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "mormonism")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://www.fairlatterdaysaints.org/answers/"
SOURCE_NAME = "FAIR (Foundation for Apologetic Information and Research)"
DEFAULT_AUTHOR = "FAIR"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (page title, category folder, category slug, subcategory)
SEED = [
    ("DNA_and_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Horses_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Hebraisms_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Chiasmus_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Book_of_Mormon_textual_changes", "02-book-of-mormon", "book-of-mormon", None),
    ("Eleven_official_witnesses_to_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Bible_passages_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),

    ("Alleged_false_prophecies_of_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_1826_trial", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Events_surrounding_the_death_of_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("1844_Succession_to_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_alleged_narcissism", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),

    ("Approaching_Anachronisms_in_the_Book_of_Abraham", "04-book-of-abraham", "book-of-abraham", None),
    ("The_Book_of_Abraham_and_the_Book_of_Genesis", "04-book-of-abraham", "book-of-abraham", None),
    ("Evidences_for_the_Book_of_Abraham%27s_Authenticity", "04-book-of-abraham", "book-of-abraham", None),

    ("1835_Doctrine_and_Covenants_denies_polygamy", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Possible_contradictions_in_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Overview_of_changes_to_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),

    ("Worship_different_Jesus", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Latter-day_Saints_and_the_symbol_of_the_cross", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("One_Nation_Under_Gods", "06-mormonism-and-christianity", "mormonism-and-christianity", None),

    # --- Expansion batch ---
    ("The_Spalding_Theory_of_Book_of_Mormon_authorship", "02-book-of-mormon", "book-of-mormon", None),
    ("View_of_the_Hebrews_theory_of_Book_of_Mormon_authorship", "02-book-of-mormon", "book-of-mormon", None),
    ("Seer_stones_and_the_Urim_and_Thummim", "02-book-of-mormon", "book-of-mormon", None),
    ("Gold_plates_and_the_translation_process", "02-book-of-mormon", "book-of-mormon", None),
    ("Statement_of_the_Three_Witnesses", "02-book-of-mormon", "book-of-mormon", None),
    ("Statement_of_the_Eight_Witnesses", "02-book-of-mormon", "book-of-mormon", None),
    ("Old_world_geography_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Mesoamerican_Model_of_Book_of_Mormon_geography", "02-book-of-mormon", "book-of-mormon", None),
    ("Heartland_Model_of_Book_of_Mormon_geography", "02-book-of-mormon", "book-of-mormon", None),
    ("The_Book_of_Mormon_as_an_ancient_text", "02-book-of-mormon", "book-of-mormon", None),
    ("Reformed_Egyptian_and_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Identity_of_the_Lamanites_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("The_great_and_abominable_church_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("The_nature_of_God_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Warfare_in_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("Isaiah_and_the_Book_of_Mormon", "02-book-of-mormon", "book-of-mormon", None),
    ("The_Book_of_Mormon_as_history", "02-book-of-mormon", "book-of-mormon", None),

    ("Joseph_Smith%27s_status_in_Latter-day_Saint_belief", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith_and_money_digging", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith_and_folk_magic_or_the_occult", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_First_Vision", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Personages_who_appeared_to_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Kinderhook_Plates", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_prophecy_of_the_Civil_War", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("The_White_Horse_prophecy", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_campaign_for_President_of_the_United_States", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Plural_wives_of_Joseph_Smith", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith_and_the_Nauvoo_Expositor", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),
    ("Joseph_Smith%27s_Introduction_and_Practice_of_Plural_Marriage", "03-joseph-smith-and-early-history", "joseph-smith-and-early-history", None),

    ("Mountain_Meadows_Massacre", "01-critical-perspectives", "critical-perspectives", None),
    ("Mark_Hofmann", "01-critical-perspectives", "critical-perspectives", None),
    ("Plural_Marriage_and_Church_Leaders%27_Underage_Wives", "01-critical-perspectives", "critical-perspectives", None),
    ("Brigham_Young%27s_statements_regarding_race", "01-critical-perspectives", "critical-perspectives", None),
    ("Fabricated_quotes_from_Brigham_Young", "01-critical-perspectives", "critical-perspectives", None),
    ("Alleged_whitewashing_of_Church_history", "01-critical-perspectives", "critical-perspectives", None),
    ("Alleged_whitewashing_of_polygamy_in_Church_history", "01-critical-perspectives", "critical-perspectives", None),

    ("Introduction_to_Book_of_Abraham_Documents", "04-book-of-abraham", "book-of-abraham", None),
    ("The_Church%27s_Treatment_of_Controversies_Surrounding_the_Book_of_Abraham", "04-book-of-abraham", "book-of-abraham", None),
    ("Joseph_Smith%27s_%22Incorrect%22_Translation_of_the_Book_of_Abraham_Papyri", "04-book-of-abraham", "book-of-abraham", None),
    ("Theological_Questions_Regarding_the_Book_of_Abraham", "04-book-of-abraham", "book-of-abraham", None),
    ("Production_of_the_Book_of_Abraham", "04-book-of-abraham", "book-of-abraham", None),

    ("Adding_sections_to_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Examples_of_changes_to_the_Doctrine_and_Covenants", "05-doctrine-and-covenants", "doctrine-and-covenants", None),
    ("Lectures_on_Faith", "05-doctrine-and-covenants", "doctrine-and-covenants", None),

    ("Mormonism_and_Christianity/Grace_and_works", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Characteristics_of_God", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/King_Follett_Discourse", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Corporeality_of_God", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Multiplicity_of_Gods", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Polytheism", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Trinity", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Nicene_creed", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Deification_of_man", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Mormonism_and_the_nature_of_God/Heavenly_Mother", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Apostasy/Evidence_of", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Apostasy/Reasons_for", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Jesus_Christ/Atonement", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Jesus_Christ/Is_Jesus_a_Created_Being", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Plan_of_salvation/Pre-mortal_existence", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Plan_of_salvation/Mortal_existence", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Plan_of_salvation/Post-mortal_existence", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Plan_of_salvation/Three_degrees_of_glory", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("The_Bible_as_the_word_of_God", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Biblical_inerrancy", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
    ("Doctrinal_completeness_of_the_Bible", "06-mormonism-and-christianity", "mormonism-and-christianity", None),
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
    text = text.replace("/", " ")  # MediaWiki subpage titles like "Jesus Christ/Worship"
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")[:120]


def html_to_markdown(html_content: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_images = True
    md = converter.handle(html_content)
    return re.sub(r"\n{4,}", "\n\n\n", md).strip()


NOISE_CLASS_RE = re.compile(r"^toc$|noprint|mw-editsection|printfooter")


def scrape_one(page_title, folder, category, subcategory):
    url = BASE_URL + page_title
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else page_title.replace("_", " ")

        content = soup.find(id="mw-content-text")
        if not content:
            log_error(url, "No #mw-content-text found")
            return False

        for tag in content.find_all(["style", "script"]):
            tag.decompose()
        for tag in content.find_all(class_=NOISE_CLASS_RE):
            tag.decompose()
        # drop the "< Back to FAIR Answers Index" nav link, always the first <p>/<a>
        back_link = content.find("a", string=re.compile(r"Back to FAIR", re.I))
        if back_link:
            back_link.decompose()

        md_content = html_to_markdown(str(content))
        if len(md_content) < 200:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title) or slugify(page_title)
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "mormonism",
            "category": category,
            "source": url,
            "author": DEFAULT_AUTHOR,
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

        print(f"  OK  {category} / {slug}.md ({word_count} words)", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from FAIR...")
    ok = 0
    for page_title, folder, category, subcategory in SEED:
        if scrape_one(page_title, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
