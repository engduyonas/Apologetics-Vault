#!/usr/bin/env python3
"""
Assign subcategory tags to articles across ALL content folders.
Uses carefully ordered keyword rules with longer, more specific phrases
to minimize false matches. First match wins, so more specific rules
must come before general ones.
"""

import os
import re
import sys

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "islam")

# ── Shared keyword lists ────────────────────────────────────────────────────

CHURCH_FATHERS = [
    "augustine", "origen", "irenaeus", "tertullian", "athanasius",
    "cyril", "gregory", "basil", "ambrose", "hippolytus", "aphrahat",
    "chrysostom", "jerome", "clement", "polycarp", "ignatius",
    "justin martyr", "eusebius", "epiphanius", "theodoret", "didymus",
    "hilary", "amphilochi", "diognetus", "theophilus", "athenagoras",
    "barnabas", "hermas", "papias", "lactantius", "ambrosiaster",
    "novatian", "cyprian", "methodius", "rufinus", "maximus",
    "damascene", "bernard", "leo the great", "anselm",
]

NAMED_OPPONENTS = [
    "mohammed hijab", "hijab proves",
    "jamal badawi", "badawi's", "badawi ",
    "ahmed deedat", "deedat",
    "yasir qadhi", "qadhi's", "qadhi ",
    "adnan rashid",
    "bassam zawadi", "zawadi",
    "sami zaatari", "zaatari",
    "osama abdallah",
    "shabir ally",
    "nadir ahmed",
    "naik",
    "jalal abualrub",
    "taqiyyist",
    "shahid's",
]


def _rules_christological():
    """02-christological-issues: 256 articles about Christ."""
    return [
        ("Christ in the Quran", [
            "quran", "qur'an", "quranic",
            "islam agrees", "islam testifies",
            "islam\u2019s bad news", "islam's bad news",
            "islamic perspective", "islamic monotheism", "islamic theology",
            "muslim", "allah",
            "muhammad", "better than muhammad", "greater than muhammad",
            "prophet of islam",
            "jesus or muhammad",
            "60 questions",
            "did not teach islam",
            "christian response to",
            "islam\u2019s greatest", "islam's greatest",
        ]),
        ("Worship of Christ", [
            "worship", "worshiping", "worshipping",
            "latreuo", "sacred service",
            "carmen christi",
            "recipient of worship",
            "slaves of jesus",
            "worthy of all praise",
            "worthy of all honor",
        ]),
        ("Son of Man & Preexistence", [
            "son of man", "preexist", "pre-incarnate", "preincarnate",
            "as old as god",
            "eternal generation",
            "christological preexistence",
            "post-resurrection status",
        ]),
        ("Shema & Monotheism", [
            "shema", "one lord",
            "exclusive language",
            "binitarian", "uniplural",
            "anti-trinitarian",
        ]),
        ("Messianic Prophecies", [
            "messiah", "messianic",
            "psalm 82", "psalm 110",
            "daniel's son", "daniel",
            "appearances of christ",
            "ot appearances",
            "dead sea scroll", "melchizedek",
            "inter-testamental",
            "rabbinic", "rabbi",
            "jewish christology", "jewish traditions",
            "ot predict", "third day",
            "kinsman-redeemer",
            "seed of david", "seed shall",
            "isaiah and the glory",
            "the deity of the messiah in isaiah",
            "exaltation of the messiah",
            "divine messiah",
            "messiah most high",
            "messiah our righteousness",
            "messiah on yahweh\u2019s throne", "messiah on yahweh's throne",
            "messiah as israel's god", "messiah as israel\u2019s god",
            "glorious splendor", "king messiah",
            "shepherd king",
            "coming of israel's divine", "coming of israel\u2019s divine",
            "good shepherd", "chief shepherd",
            "arrival of israel",
            "faithful witness in the skies",
        ]),
        ("Christ's Deity & Identity", [
            "deity", "divine",
            "god-man", "god incarnate", "incarnation", "incarnate",
            "almighty", "omniscient", "incomprehensible",
            "equal to", "equal with",
            "is god", "be god",
            "god alone is good",
            "yahweh", "yhwh",
            "great i am", "i am",
            "john 1:1", "john 8:58",
            "colossians", "romans 9:5",
            "acts 20:28", "hebrews 1",
            "new world translation",
            "the name", "name of",
            "glory of", "lord of glory",
            "archangel michael",
            "amen", "life-giver",
            "occupier of god", "heavenly throne",
            "savior", "redeemer", "refuge",
            "forgiver", "justifier",
            "mighty god", "king of kings",
            "ruler of creation", "maker",
            "above all", "over all", "all in all",
            "criteria for deity",
            "kyrios",
            "the blood of god",
            "tempt the lord",
            "son of god",
            "son who voluntarily",
            "exalted", "exaltation",
            "superior to", "heavenly host",
            "judge of all",
            "unseen god", "seeing the",
            "word become flesh", "eternal word",
            "the uniqueness of christ",
            "an articulation",
            "first creature", "arianism",
            "similitude with adam",
            "like adam",
            "jesus saves exactly",
            "jesus meets the criteria",
            "mary the mother", "houri",
            "jesus christ in the bible",
            "god's salvation has come",
            "our hope and trust",
            "people that christ saves",
            "god's servant or son",
            "john 14:6",
            "patristic evidence",
            "early church fathers on john",
            "trusting in yahweh",
            "who did abraham see",
            "eternally praised",
            "god the son",
            "god of gods", "prince of princes",
            "god who knows",
            "ignorance of the day",
            "servant or son",
            "good and holy", "absolutely good",
            "sonship of christ",
            "glorious messenger",
            "more proof that",
        ]),
        ("NT Christology", [
            "christology of luke", "christology of mark",
            "christology of james", "christology of jude",
            "markan perspective",
            "scholars on the christology",
            "john macarthur",
            "gospel q ", "q and the identity",
            "thomas' god", "thomas\u2019 god",
            "paul's use of lord", "paul\u2019s use of lord",
            "apostle peter",
            "what did the apostle",
            "lukan",
            "the supremacy of jesus in hebrews",
            "origen's christology", "origen\u2019s christology",
            "tabari on jesus",
            "jesus from the seed",
            "jesus in the rabbinic",
            "bart ehrman",
            "response to bart",
        ]),
    ]


def _rules_theological():
    """03-theological-issues: 103 articles on theology."""
    return [
        ("Nature of Allah", [
            "allah", "where is allah",
            "immaterial", "invisible man",
            "deceiver", "misleader", "guessing",
            "oaths", "pride", "imperfection", "mutability",
            "aseity", "sufficient",
            "mushrik",
            "pre-islamic", "mecca",
            "prays", "worships",
            "shahadah",
            "satan on allah", "annihilation of allah",
            "inheritance",
            "quran as a divine conscious",
            "plurality issues",
        ]),
        ("Trinity & Monotheism", [
            "trinity", "trinitarian", "triune",
            "binitarian", "shema", "elohim",
            "monotheism", "plurality",
            "aaronic blessing",
            "genesis 19:24",
            "isaiah 6",
            "early church on",
            "divine person",
            "old testament on god becoming",
            "ot witness", "ot prophets",
            "personhood of the spirit",
            "identity of the only true god",
            "heavenly tabernacle",
            "gods of israel",
            "unitarian",
            "is the father god",
            "holy spirit", "gabriel",
            "christianization",
            "god's son and heir",
        ]),
        ("Islamic Theology Critiqued", [
            "islam", "muslim", "kabah",
            "quran", "quranic",
            "paganism",
            "arab", "muhammad",
            "eloquence",
            "uncreatedness", "unintelligibility",
            "as-samad",
            "angel gabriel",
            "criteria for god",
        ]),
        ("Salvation & Eschatology", [
            "salvation", "saved", "hell",
            "atonement", "vicarious",
            "matthew 25", "ninevite",
            "luke-acts", "sacrifice",
        ]),
        ("OT Theology", [
            "old testament", "hebrew bible",
            "baptismal formula",
        ]),
    ]


def _rules_answers():
    """01-answers-to-common-questions: 83 Q&A articles."""
    return [
        ("Rebuttals", [
            *NAMED_OPPONENTS,
        ]),
        ("Bible & Quran", [
            "quran", "qur'an", "quranic",
            "bible has never been corrupted",
            "biblical authority",
            "consummation versus islamic",
            "abrogation",
            "ishmael",
            "muhammad announced",
            "wasn't muhammad",
            "isn't muhammad",
            "on serving others besides allah",
        ]),
        ("Women & Ethics", [
            "women in islam",
            "degrade women",
            "rape", "deuteronomy 22",
            "annihilation of the amalekites",
        ]),
        ("Salvation & Atonement", [
            "sacrifice", "appease",
            "forgive sins", "forgiving sins",
            "forgiveness of sins",
            "baptism",
            "salvation",
            "law",
            "ezekiel 18",
            "melchizedek",
            "inspired",
        ]),
        ("Trinity & Godhead", [
            "trinity", "plurality",
            "three gods",
            "evolution in nt christology",
            "promise to abraham",
            "offspring",
        ]),
        ("Deity of Christ", [
            "jesus", "christ", "god",
            "deity", "divine",
            "kyrios", "lord",
            "son of god", "son of man",
            "tempt", "die",
            "pray", "slept",
            "hungry", "change",
            "greater", "emptied",
            "exaltation", "subjection",
            "miracles", "servant",
            "savior",
        ]),
    ]


def _rules_quranic():
    """05-quranic-issues: 86 articles on the Quran."""
    return [
        ("Quran & the Bible", [
            "bible", "biblical", "preservation",
            "confirms the trinity",
            "corruption", "crucifixion",
            "muhaymin", "guardian",
            "study quran speak",
            "surah 5:48",
            "stoning",
            "q. 29:46",
            "challenge of the quran",
        ]),
        ("Contradictions & Errors", [
            "contradiction", "error", "blunder",
            "incoherence", "fable",
            "shape of the earth",
            "incest", "sodomy",
        ]),
        ("Textual History", [
            "textual", "variant", "irreparable",
            "compilation", "loss",
            "caliph", "third caliph",
            "recitation",
            "ahruf", "qiraat",
            "incomplete", "imperfect",
            "composition", "stages",
            "damage control", "sura 3:7",
            "parallel passages", "conciliation",
            "seven wonders",
            "word of god issue",
            "burn or not",
        ]),
        ("Quran Stories & Figures", [
            "pharaoh", "noah",
            "angel or a jinn",
            "disciples muslim",
            "worship of allah alone",
        ]),
        ("Theology of the Quran", [
            "allah", "trinity",
            "muslim", "hell",
            "gods and lords",
            "violation", "teaching",
            "model for", "hypostatic",
            "conscious being",
            "tolerance", "unjust",
            "punishment", "unlettered",
            "christian", "jewish",
            "polytheist", "guided",
            "strayed", "tauhid", "i'jaz",
            "flat earth", "days of creation",
            "gods of islam",
            "moses as", "most high",
            "surat ar-rum",
            "praying not",
            "sins of another",
            "cosmology",
            "flood",
            "falsification test",
            "quran on muslims",
            "satan",
        ]),
    ]


def _rules_muhammad():
    """06-analysis-of-muhammad: 109 articles."""
    return [
        ("Muhammad's Wives & Marriages", [
            "wife", "wives",
            "aisha", "sauda", "umm kulthum",
            "zaynab", "zaid",
            "concubine", "marriage",
            "prepubescent", "age of",
            "adultery",
        ]),
        ("Deification of Muhammad", [
            "invoking muhammad", "invoke",
            "image of allah", "visible image",
            "superior to angels",
            "islam's other god", "divine savior",
            "obsessive", "devotion",
            "partner in praise", "partner in dispensing",
            "partner in receiving",
            "human voice", "mediator",
            "adviser", "counselor",
            "heir", "servant please stand",
            "allah & mo", "foundational partnership",
            "praise of all creation",
            "prophet of shirk",
            "al-amin",
            "blasphemies exposed",
            "muhammadan blasphemies",
        ]),
        ("Character & Morality", [
            "cruelty", "excessive",
            "terror", "mayhem",
            "compromiser", "doubter",
            "poison", "how allah killed",
            "chaos", "idolatry",
            "cursed", "abused",
            "beaten", "mistreated",
            "inconsisten",
            "silly", "ridiculous",
            "blondes", "antagoniz",
            "war-monger",
            "deceived", "sinful", "transgressor",
            "contemporaries",
            "death of asma", "abu afak",
            "night journey",
            "change of the qiblah",
        ]),
        ("False Prophecies", [
            "false prophet", "false prediction",
            "false prophecy", "false prophecie",
            "prophecy of isaiah 42",
            "revisiting isaiah 42",
            "song of solomon",
            "seal of prophethood",
            "true prophet",
            "test of prophethood",
            "predicted in the gospel of john",
            "last prophet",
            "ishmael is not the father",
            "prophet of islam",
            "arab paganism", "eradicate",
            "yahweh's servant revisited",
            "muhammad fails",
        ]),
        ("Muhammad & Scripture", [
            "bible", "torah",
            "affirmed the holy bible",
            "mosaic law",
            "ehrman proves",
            "true religion and guidance",
            "miracles",
        ]),
        ("Muhammad & Islamic Practice", [
            "sunna", "qiblah",
            "prophets and their bodies",
            "setting place of the sun",
            "salvation", "saved",
            "seal", "recite",
            "never shall he",
            "feel safe", "praying for",
            "will ", "wills",
            "women", "stupid", "inferior",
            "muhammad or abraham",
        ]),
    ]


def _rules_general():
    """09-general-issues: 50 mixed articles."""
    return [
        ("Translations", [
            "arabic", "amargna", "tamil",
            "telugu", "hindi", "indonesian",
            "farsi", "bosnian", "oromo",
            "deutsch", "soomaali", "shqip",
            "islamopas", "besvarar",
            "islama cevap",
            "ответ исламу",
            "përgjigjie",
        ]),
        ("Rebuttals & Debates", [
            *NAMED_OPPONENTS,
            "debate", "challenge",
            "response",
        ]),
        ("Women in Islam", [
            "women in islam",
        ]),
        ("Quran & Bible", [
            "quran", "qur'an", "quranic",
            "bible", "biblical",
            "authority", "guardian",
            "muhaymin",
            "mushriks",
            "holy war",
            "peace",
            "allah",
            "muhammad",
            "serving others besides",
        ]),
        ("Apologetics & Defense", [
            "christian defense",
            "christian answers",
            "answering islam",
            "articles by",
            "jonah",
            "christology",
            "divine claims",
            "deuteronomy",
            "rape",
            "resurrection",
            "jesus says",
        ]),
    ]


def _rules_blog():
    """13-blog-posts: 674 blog articles."""
    return [
        ("Rebuttals & Debates", [
            *NAMED_OPPONENTS,
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
            "limited atonement",
            "imputation of righteousness",
            "almsgiving",
            "faithful obedience",
            "justified by",
            "water baptism",
            "baptismal confession",
            "relation of belief",
            "pistis",
            "catholic faith on the son",
            "atoning blood",
            "god made jesus a sin",
            "true faith is",
        ]),
        ("Patristic Theology", [
            *CHURCH_FATHERS,
            "ante-nicene", "ante nicene",
            "church father", "patristic",
            "muratorian", "apostolic succession",
            "early church",
        ]),
        ("Church & Sacraments", [
            "mary ", "mary:", "mary'", "marian",
            "queen mother", "virgin's womb",
            "veneration of the saints", "veneration of icons",
            "catholic", "orthodox",
            "sacrament", "eucharist",
            "communion of saints", "theosis",
            "catechism",
            "infant baptism",
            "pouring or sprinkling",
            "call no man father",
            "why the church is called",
            "luther on the",
            "mediating", "interceding",
            "intercessor",
            "hierarchy",
            "roman see",
        ]),
        ("Trinity & Godhead", [
            "trinity", "triune", "trinitarian",
            "two powers", "godhead", "echad",
            "uni-plurality", "divine council",
            "divine name christology",
            "plurals for god", "use of plurals",
            "three gods", "tritheism",
            "monotheism",
            "monarchi",
            "tri-personal",
            "everlasting fire",
            "voice of yhvh",
        ]),
        ("Christology", [
            "christ", "christolog",
            "son of man", "son of god",
            "deity of jesus", "jesus is god", "jesus as god",
            "worship jesus", "worshiping jesus", "worshipping jesus",
            "incarnation", "incarnate", "pre-existence", "prehuman",
            "hypostatic union", "two natures",
            "messiah", "messianic",
            "nwt proves",
            "uncreated word", "word becomes",
            "theos is jesus",
            "jesus", "deity of",
            "jehovah", "yhwh", "yahweh",
            "arian", "unitarian",
            "ancient of days",
            "angel of the lord", "great angel",
            "god-man",
            "metatron", "second god",
            "created angelic beings",
            "enoch's",
            "favored one",
        ]),
        ("Biblical Studies", [
            "torah", "targum", "lxx",
            "genesis 3", "genesis ",
            "isaiah ", "deuteronomy ",
            "hebrews 2:",
            "corinthians", "thessalonians",
            "luke-acts",
            "acts 8:",
            "prophecy", "prophecie", "prophetic",
            "canon", "canonicity",
            "bible error", "bible errors",
            "biblical verses",
            "ot evidence", "old testament",
            "new testament", "gospel of",
            "vulgar", "graphic language",
            "wisdom of solomon", "sirach",
            "elohim",
            "solomon", "david worship",
            "balaam",
            "kjv", "sharp's first",
            "michael the ruler",
            "soul of yhwh",
            "sons of god of deuteronomy",
            "closed hebrew mem",
            "virgin birth in",
            "when was christ crucified",
            "punctuation of john",
            "seed that blesses",
            "god's love of gentiles",
        ]),
        ("Quranic Analysis", [
            "quran", "qur'an", "quranic", "sura",
            "variant that makes",
            "uncreated created",
            "syriac christianity",
        ]),
        ("Muhammad & Islam", [
            "muhammad", "prophet of shirk",
            "allah", "hadith", "aisha",
            "islam", "muslim", "mormonism", "mormon",
            "hubal", "baal", "umma",
            "sharia", "taqiyy",
            "caliph", "abu hanifa",
            "sunnah", "sunni", "shia",
            "bukhari",
            "insha allah",
        ]),
    ]


FOLDER_RULES: dict[str, list[tuple[str, list[str]]]] = {
    "01-answers-to-common-questions": _rules_answers(),
    "02-christological-issues": _rules_christological(),
    "03-theological-issues": _rules_theological(),
    "05-quranic-issues": _rules_quranic(),
    "06-analysis-of-muhammad": _rules_muhammad(),
    "09-general-issues": _rules_general(),
    "13-blog-posts": _rules_blog(),
}


def classify_title(title: str, rules: list[tuple[str, list[str]]]) -> str:
    t = title.lower()
    for category, keywords in rules:
        for kw in keywords:
            if kw.lower() in t:
                return category
    return "General Topics"


def process_file(filepath: str, rules: list[tuple[str, list[str]]]) -> str | None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    end_idx = content.index("---", 3)
    frontmatter = content[3:end_idx]
    body = content[end_idx:]

    title_match = re.search(r"^title:\s*['\"]?(.*?)['\"]?\s*$", frontmatter, re.MULTILINE)
    if not title_match:
        return None

    title = title_match.group(1)
    subcategory = classify_title(title, rules)

    frontmatter = re.sub(r"\nsubcategory:.*\n", "\n", frontmatter)
    frontmatter = frontmatter.rstrip("\n") + f"\nsubcategory: {subcategory}\n"

    new_content = "---" + frontmatter + body
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return subcategory


def main():
    if not os.path.isdir(CONTENT_DIR):
        print(f"Content directory not found: {CONTENT_DIR}")
        sys.exit(1)

    grand_total = 0

    for folder_name in sorted(FOLDER_RULES):
        rules = FOLDER_RULES[folder_name]
        folder_path = os.path.join(CONTENT_DIR, folder_name)
        if not os.path.isdir(folder_path):
            print(f"  Skipping {folder_name} (not found)")
            continue

        files = sorted(f for f in os.listdir(folder_path) if f.endswith(".md"))
        counts: dict[str, int] = {}
        total = 0

        for filename in files:
            filepath = os.path.join(folder_path, filename)
            subcat = process_file(filepath, rules)
            if subcat:
                counts[subcat] = counts.get(subcat, 0) + 1
                total += 1

        print(f"\n{'=' * 60}")
        print(f"  {folder_name}  ({total} articles)")
        print(f"{'=' * 60}")
        for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {cat:40s}  {count:>4d}")

        grand_total += total

    print(f"\n{'=' * 60}")
    print(f"  GRAND TOTAL: {grand_total} articles categorized")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
