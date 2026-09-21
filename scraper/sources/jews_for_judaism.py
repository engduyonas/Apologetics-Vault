#!/usr/bin/env python3
"""
Scraper for a curated set of Judaism articles from jewsforjudaism.org
(Judaism tradition pilot content — Jewish responses to Christian
missionary/messianic-prophecy claims, Talmudic defense, and Jewish
theology, from a counter-missionary organization staffed by rabbis).

No explicit reuse/copyright statement is posted on the site (checked the
article pages and footer); this is the same "ambiguous, not explicit
permission" posture as most of this project's other ministry-site
sources, treated the same informal way per the project owner's direction.

Works from a fixed, hand-vetted seed list — same pattern as the other
sources/ scrapers.

Run: python3 sources/jews_for_judaism.py
"""

import os
import re
import time

import html2text
import requests
import yaml
from bs4 import BeautifulSoup

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "content", "judaism")
ERRORS_LOG = os.path.join(os.path.dirname(__file__), "errors.log")

BASE_URL = "https://jewsforjudaism.org/knowledge/articles/"
SOURCE_NAME = "Jews for Judaism"

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

DELAY = 1.0

# (slug, category folder, category slug, subcategory)
SEED = [
    ("isaiah-53-jesus-not-suffering-servant", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-teaches-jesus-not-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("the-truth-about-psalms-22-17", "01-messianic-prophecy", "messianic-prophecy", None),
    ("rabbinic-commentators-rashi-isaiah-53", "01-messianic-prophecy", "messianic-prophecy", None),
    ("rabbi-moshe-al-sheich-isaiah-53", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel-9-verse-by-verse", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel-9-problem-with-christian-interpretative-credibility", "01-messianic-prophecy", "messianic-prophecy", None),

    ("new-testament-refutations-trinity-doctrine-part-1", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-2", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("three-divine-echoes-singularity-plurality-oneness", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("oneness-of-god-the-meaning-of-elohim", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("a-remarkable-discovery-two-paths-to-one-god", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("israels-god-real-know", "02-trinity-and-monotheism", "trinity-and-monotheism", None),

    ("defending-the-talmud-against-centuries-of-misinterpretation", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("biblical-basis-rabbinic-authority", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("what-are-the-jewish-holy-books", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("answering-dr-brown-s-objections-to-judaism", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),

    ("does-the-death-of-the-righteous-atone", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("sin-sacrifices-and-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("finding-substitutes-for-sacrifice", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("blood-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("the-dimensions-of-sin-and-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),

    ("who-was-jesus", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jewish-people-rejected-christian-messiah", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("you-are-my-witnesses-a-traditional-response-to-missionaries", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("you-turn-the-jewish-response-to-a-christian-challenge", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("journey-home-judaism-part-1", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),

    # --- Expansion batch: Isaiah 53 "not the suffering servant" series ---
    ("isaiah-53-jesus-not-suffering-servant-part-2", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-3", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-4", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-5", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-6", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-7", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-8", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-9", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-10", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-12", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-14", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-15", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-16", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-17", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-18", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-19", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-20", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-21", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-22", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-23", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-24", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-25", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-26", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-27", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-28", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-29", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-jesus-not-suffering-servant-part-30", "01-messianic-prophecy", "messianic-prophecy", None),

    # --- Daniel 9 / messianic-age series ---
    ("daniel-9-the-messianic-age", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel927-roman-persecution-jewish-people-part-2", "01-messianic-prophecy", "messianic-prophecy", None),
    ("roman-persecution-of-jewish-people-part-1", "01-messianic-prophecy", "messianic-prophecy", None),
    ("anointing-the-holy-of-holies", "01-messianic-prophecy", "messianic-prophecy", None),
    ("daniel926-historical-synopsis-of-events", "01-messianic-prophecy", "messianic-prophecy", None),
    ("troubled-times-sixty-two-weeks", "01-messianic-prophecy", "messianic-prophecy", None),
    ("anointed-one-that-shall-be-cut-off", "01-messianic-prophecy", "messianic-prophecy", None),
    ("who-is-gods-anointed", "01-messianic-prophecy", "messianic-prophecy", None),
    ("expectations-for-the-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("getting-second-chance", "01-messianic-prophecy", "messianic-prophecy", None),

    # --- Other messianic-prophecy standalone articles ---
    ("isaiah-53-the-jewish-perspective", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-and-the-suffering-servant", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-explained", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-verse-verse", "01-messianic-prophecy", "messianic-prophecy", None),
    ("isaiah-53-micah-7-isaiah-62", "01-messianic-prophecy", "messianic-prophecy", None),
    ("the-scepter-of-judah-shiloh-and-the-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("messiah-the-criteria", "01-messianic-prophecy", "messianic-prophecy", None),
    ("will-real-messiah-please-stand", "01-messianic-prophecy", "messianic-prophecy", None),
    ("moshiach-ben-yosef", "01-messianic-prophecy", "messianic-prophecy", None),
    ("jewish-belief-in-messiah-and-the-messianic-age", "01-messianic-prophecy", "messianic-prophecy", None),
    ("what-are-the-criteria-that-judaism-has-established-about-the-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("maimonides-laws-pertaining-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("was-the-last-supper-a-seder", "01-messianic-prophecy", "messianic-prophecy", None),
    ("was-there-a-resurrection-of-the-dead-when-jesus-died", "01-messianic-prophecy", "messianic-prophecy", None),
    ("council-nation-scripture-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("council-nation-scripture-introduction", "01-messianic-prophecy", "messianic-prophecy", None),
    ("council-nation-scripture-law-moses", "01-messianic-prophecy", "messianic-prophecy", None),
    ("jews-jewish-christianity-jesus-messiah", "01-messianic-prophecy", "messianic-prophecy", None),
    ("jews-jewish-christianity-proofs-christianity-hebrew-bible", "01-messianic-prophecy", "messianic-prophecy", None),

    # --- New Testament / Trinity refutations series ---
    ("new-testament-refutations-trinity-doctrine-part-3", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-of-the-trinity-doctrine-part-4", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-5", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-6", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-of-the-trinity-doctrine-part-7", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-8", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-10", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-11", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-12", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-13", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-14", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-15", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-16", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-17", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-18", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-19", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-of-the-trinity-doctrine-part-20", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-21", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-22", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-23", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-24", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-25", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-26", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-27", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-28", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-29", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-30", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-31", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-of-the-trinity-doctrine-part-32", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-33", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-34", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-refutations-trinity-doctrine-part-35", "02-trinity-and-monotheism", "trinity-and-monotheism", None),

    # --- Other trinity-and-monotheism standalone articles ---
    ("god-as-one-vs-the-trinity", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("the-jewish-view-of-satan", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("satan-and-the-trinity", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("can-you-help-clarify-the-jewish-concept-of-satan-for-me", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("why-jews-reject-incarnation", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("new-testament-passages-that-refute-the-christian-doctrine-of-the-trinity", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-anthropomorphisms", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-traditional-sources", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-angel-lord", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-plural-terminology", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-introduction", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-exalted-king-exalted-nation", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-conclusion", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-idolatry-divine-names", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("council-nation-scripture-idolatry", "02-trinity-and-monotheism", "trinity-and-monotheism", None),
    ("jews-jewish-christianity-jesus-god", "02-trinity-and-monotheism", "trinity-and-monotheism", None),

    # --- Talmud / rabbinic authority & Council of My Nation "Law and Chosenness" ---
    ("does-the-talmud-talk-about-a-ressurection-3-days-after-the-end-of-the-world", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("jesus-in-the-talmud", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("what-is-the-mishnah-and-talmud-s-purpose", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("how-has-the-talmud-had-an-influence-on-jewish-history", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("critical-thinking-and-the-talmud", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("do-the-jewish-people-keep-the-torah-because-they-fear-god", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("eternity-torah-mitzvos", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-conclusion", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-conclusion-2", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-christian-objections-jewish-emphasis-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-talmudic-application-scripture", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("identifying-teachers-law-excerpt-council-nation", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-scriptural-evidence", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-christian-objections-structure-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-historical-objections", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-identifying-teachers-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-application-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-factions-judaism-second-temple-era", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("council-nation-law-chosenness-preservation-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),
    ("christian-objections-observance-law", "03-talmud-and-rabbinic-judaism", "talmud-and-rabbinic-judaism", None),

    # --- Sin, atonement & sacrifice additions ---
    ("council-nation-scripture-atonement", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("jews-jewish-christianity-forgiveness-sin", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("judaism-and-reincarnation", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),
    ("messianic-age-will-resurrected", "04-sin-atonement-and-sacrifice", "sin-atonement-and-sacrifice", None),

    # --- Jewish identity & practice additions ---
    ("13-principles-of-faith", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("imitating-god-the-basis-of-jewish-morality", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("repentance-tshuvah", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("almah-virgin-and-parthenos", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("who-is-melchizedek", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("christianity-vs-judaism-major-differences", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("why-jews-cannot-accept-the-new-testament", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("the-new-testament", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("manufacturing-verses", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("paul-the-father-of-a-new-religion", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("mistranslations-of-text", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("christian-proof-texting", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("an-introduction-to-prooftexting", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-as-gods-chosen-people", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("personal-relationship-with-god", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("believer-still-jewish", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("sin-atonement-and-salvation", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("council-nation-preface", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("the-council-of-my-nation-an-articulation-of-judaism", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-jewish-christianity-introduction", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-and-jewish-christianity-preface-to-the-first-printing", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-jewish-christianity-final-word", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-jewish-christianity-suggestions-reading", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-jewish-christianity-jews-gentiles-jewish-christians", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("maimonides-eight-levels-charity", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("jews-christmas-bad-match", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("noachide", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("shared-values-noahide-laws", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
    ("biblical-sources-7-noachide-laws", "05-jewish-identity-and-practice", "jewish-identity-and-practice", None),
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


def scrape_one(page_slug, folder, category, subcategory):
    url = BASE_URL + page_slug
    try:
        resp = fetch(url)
        soup = BeautifulSoup(resp.text, "lxml")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else page_slug

        author_el = soup.find(class_="post-author")
        author = author_el.get_text(strip=True) if author_el else "Jews for Judaism"

        content = soup.find(class_="post-wrapper")
        if not content:
            log_error(url, "No .post-wrapper found")
            return False

        # drop the PDF-download link list and share/like icon rows
        for tag in content.find_all("ul"):
            if tag.find("a", href=re.compile(r"active_storage/blobs")):
                tag.decompose()

        md_content = html_to_markdown(str(content))
        if len(md_content) < 200:
            log_error(url, "Markdown too short")
            return False

        slug = slugify(title) or page_slug
        word_count = len(md_content.split())

        frontmatter = {
            "title": title,
            "slug": slug,
            "tradition": "judaism",
            "category": category,
            "source": url,
            "author": author,
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

        print(f"  OK  {category} / {slug}.md ({word_count} words, {author})", flush=True)
        return True
    except Exception as e:
        log_error(url, str(e))
        return False


def main():
    print(f"Scraping {len(SEED)} pages from Jews for Judaism...")
    ok = 0
    for page_slug, folder, category, subcategory in SEED:
        if scrape_one(page_slug, folder, category, subcategory):
            ok += 1
        time.sleep(DELAY)
    print(f"\nDone: {ok}/{len(SEED)} succeeded.")


if __name__ == "__main__":
    main()
