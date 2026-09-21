export interface Tradition {
  slug: string;
  order: number;
  title: string;
  description: string;
  icon: string;
}

export const TRADITIONS: Tradition[] = [
  {
    slug: "christian-theology",
    order: 1,
    title: "Christian Theology",
    description:
      "Christian doctrine on its own terms — Christology, the Trinity, biblical reliability, church history, and patristic theology.",
    icon: "cross",
  },
  {
    slug: "islam",
    order: 2,
    title: "Islam",
    description:
      "Examination of Islamic sources and claims — the Quran, Muhammad, hadith, and Islamic theology — drawn from Sam Shamoun's work.",
    icon: "moon-star",
  },
  {
    slug: "judaism",
    order: 3,
    title: "Judaism",
    description:
      "Jewish responses to Christian messianic-prophecy claims, Talmudic defense, and Jewish theology, drawn from Jews for Judaism.",
    icon: "star",
  },
  {
    slug: "eastern-traditions",
    order: 4,
    title: "Eastern Traditions",
    description:
      "Theravada Buddhist teachings and texts, drawn from Access to Insight.",
    icon: "flower",
  },
  {
    slug: "mormonism",
    order: 5,
    title: "Mormonism",
    description:
      "Examination of Joseph Smith's claims and foundational LDS doctrine, drawn from Sam Shamoun's work.",
    icon: "landmark",
  },
  {
    slug: "atheism-secularism",
    order: 6,
    title: "Atheism & Secularism",
    description:
      "Nontheistic arguments, critiques of theistic arguments, secular ethics, and skeptical biblical criticism, drawn from the Secular Web.",
    icon: "brain",
  },
];

export interface Category {
  slug: string;
  folder: string;
  order: number;
  title: string;
  description: string;
  icon: string;
}

export const CATEGORIES: Record<string, Category[]> = {
  islam: [
    {
      slug: "answers-to-common-questions",
      folder: "01-answers-to-common-questions",
      order: 1,
      title: "Answers to Common Questions",
      description:
        "Responses to frequently asked questions and common claims about Islam.",
      icon: "help-circle",
    },
    {
      slug: "theological-issues",
      folder: "03-theological-issues",
      order: 3,
      title: "Theological Issues",
      description: "The nature of Allah and Islamic theology critiqued.",
      icon: "book-open",
    },
    {
      slug: "quranic-issues",
      folder: "05-quranic-issues",
      order: 5,
      title: "Quranic Issues",
      description:
        "Analysis of Quranic claims, contradictions, textual history, and theological problems.",
      icon: "scroll",
    },
    {
      slug: "analysis-of-muhammad",
      folder: "06-analysis-of-muhammad",
      order: 6,
      title: "Analysis of Muhammad",
      description:
        "Examination of Muhammad's character, teachings, prophecies, and historical record.",
      icon: "user",
    },
    {
      slug: "hadith-analysis",
      folder: "07-hadith-analysis",
      order: 7,
      title: "Hadith Analysis",
      description:
        "Examination of the hadith literature, its cosmology, and fantastical claims.",
      icon: "file-text",
    },
    {
      slug: "polemical-issues",
      folder: "08-polemical-issues",
      order: 8,
      title: "Polemical Issues",
      description:
        "Cross-topic debates on Abraham, the Holy Spirit, atonement, and ethical comparisons.",
      icon: "message-square",
    },
    {
      slug: "general-issues",
      folder: "09-general-issues",
      order: 9,
      title: "General Issues",
      description:
        "Women in Islam, tolerance, historical analysis, and broad comparative topics.",
      icon: "globe",
    },
    {
      slug: "responses-to-authors",
      folder: "10-responses-to-authors",
      order: 10,
      title: "Responses to Muslim Authors",
      description:
        "Rebuttals and responses to specific Muslim scholars, speakers, and debaters.",
      icon: "users",
    },
    {
      slug: "turning-the-tables",
      folder: "11-turning-the-tables",
      order: 11,
      title: "Turning the Tables",
      description:
        "Series applying Muslim argumentation standards back to Islamic sources.",
      icon: "rotate-ccw",
    },
    // 10-responses-to-authors intentionally has 0 scraped articles; the category
    // auto-hides via getCategoriesWithCounts()'s articleCount > 0 filter.
    // 13-blog-posts was retired as its own category — its articles were
    // redistributed into the topical categories above by subcategory.
  ],
  "christian-theology": [
    {
      slug: "answers-to-common-questions",
      folder: "01-answers-to-common-questions",
      order: 1,
      title: "Answers to Common Questions",
      description:
        "Responses to common questions and objections raised about Christian doctrine.",
      icon: "help-circle",
    },
    {
      slug: "christological-issues",
      folder: "02-christological-issues",
      order: 2,
      title: "Christological Issues",
      description: "The deity, nature, and identity of Jesus Christ.",
      icon: "crown",
    },
    {
      slug: "theological-issues",
      folder: "03-theological-issues",
      order: 3,
      title: "Theological Issues",
      description: "The Trinity, salvation, and Christian theology proper.",
      icon: "book-open",
    },
    {
      slug: "biblical-issues",
      folder: "04-biblical-issues",
      order: 4,
      title: "Biblical Issues",
      description:
        "Biblical inspiration, canon, textual criticism, and scriptural authority.",
      icon: "book",
    },
    {
      slug: "church-history-and-denominations",
      folder: "14-church-history-and-denominations",
      order: 5,
      title: "Church History & Denominations",
      description:
        "Doctrine and history across Catholic, Orthodox, and Protestant traditions, drawn from public-domain reference works.",
      icon: "landmark",
    },
    {
      slug: "polemical-issues",
      folder: "08-polemical-issues",
      order: 6,
      title: "Polemical Issues",
      description:
        "Cross-topic essays on Abraham, angels, and biblical interpretation.",
      icon: "message-square",
    },
    {
      slug: "general-issues",
      folder: "09-general-issues",
      order: 7,
      title: "General Issues",
      description: "Broader topics in Christian apologetics and biblical ethics.",
      icon: "globe",
    },
    {
      slug: "short-summaries",
      folder: "12-short-summaries",
      order: 8,
      title: "Short Summaries",
      description: "Concise summary articles on key theological points.",
      icon: "align-left",
    },
    // 13-blog-posts was retired as its own category — its articles were
    // redistributed into the topical categories above by subcategory.
  ],
  judaism: [
    {
      slug: "messianic-prophecy",
      folder: "01-messianic-prophecy",
      order: 1,
      title: "Messianic Prophecy",
      description: "Jewish responses to Christian messianic-prophecy claims — Isaiah 53, Daniel 9, and Psalm 22.",
      icon: "scroll",
    },
    {
      slug: "trinity-and-monotheism",
      folder: "02-trinity-and-monotheism",
      order: 2,
      title: "Trinity & Monotheism",
      description: "Jewish arguments for strict monotheism against the Christian Trinity.",
      icon: "book-open",
    },
    {
      slug: "talmud-and-rabbinic-judaism",
      folder: "03-talmud-and-rabbinic-judaism",
      order: 3,
      title: "Talmud & Rabbinic Judaism",
      description: "Defense of the Talmud and the authority of rabbinic tradition.",
      icon: "book",
    },
    {
      slug: "sin-atonement-and-sacrifice",
      folder: "04-sin-atonement-and-sacrifice",
      order: 4,
      title: "Sin, Atonement & Sacrifice",
      description: "Jewish theology of sin, atonement, and sacrifice without a temple.",
      icon: "heart",
    },
    {
      slug: "jewish-identity-and-practice",
      folder: "05-jewish-identity-and-practice",
      order: 5,
      title: "Jewish Identity & Practice",
      description: "Responses to Christian missionary outreach, and Jewish identity more broadly.",
      icon: "users",
    },
  ],
  mormonism: [
    {
      slug: "critical-perspectives",
      folder: "01-critical-perspectives",
      order: 1,
      title: "Critical Perspectives",
      description: "Examination of Joseph Smith's claims and foundational LDS doctrine, drawn from Sam Shamoun's work.",
      icon: "user",
    },
    {
      slug: "book-of-mormon",
      folder: "02-book-of-mormon",
      order: 2,
      title: "Book of Mormon",
      description: "LDS apologetic responses to historical, textual, and scientific criticisms of the Book of Mormon.",
      icon: "book",
    },
    {
      slug: "joseph-smith-and-early-history",
      folder: "03-joseph-smith-and-early-history",
      order: 3,
      title: "Joseph Smith & Early History",
      description: "LDS apologetic treatment of Joseph Smith's life and the early Church's history.",
      icon: "scroll",
    },
    {
      slug: "book-of-abraham",
      folder: "04-book-of-abraham",
      order: 4,
      title: "Book of Abraham",
      description: "LDS apologetic responses to Egyptological and textual criticisms of the Book of Abraham.",
      icon: "scroll",
    },
    {
      slug: "doctrine-and-covenants",
      folder: "05-doctrine-and-covenants",
      order: 5,
      title: "Doctrine & Covenants",
      description: "LDS apologetic treatment of the Doctrine and Covenants and its revisions.",
      icon: "book-open",
    },
    {
      slug: "mormonism-and-christianity",
      folder: "06-mormonism-and-christianity",
      order: 6,
      title: "Mormonism & Christianity",
      description: "How LDS doctrine relates to and differs from historic Christianity.",
      icon: "cross",
    },
  ],
  "eastern-traditions": [
    {
      slug: "core-teachings",
      folder: "01-core-teachings",
      order: 1,
      title: "Core Teachings",
      description:
        "The Four Noble Truths, the Eightfold Path, and dependent origination.",
      icon: "compass",
    },
    {
      slug: "meditation-and-mental-development",
      folder: "02-meditation-and-mental-development",
      order: 2,
      title: "Meditation & Mental Development",
      description:
        "Jhana, mindfulness of breathing, and the practice of mental cultivation.",
      icon: "brain",
    },
    {
      slug: "ethics-and-conduct",
      folder: "03-ethics-and-conduct",
      order: 3,
      title: "Ethics & Conduct",
      description: "Precepts, right speech, and the moral foundations of practice.",
      icon: "scale",
    },
    {
      slug: "kamma-and-rebirth",
      folder: "04-kamma-and-rebirth",
      order: 4,
      title: "Kamma & Rebirth",
      description: "Cause and effect, and the cycle of rebirth.",
      icon: "refresh-cw",
    },
    {
      slug: "not-self-and-liberation",
      folder: "05-not-self-and-liberation",
      order: 5,
      title: "Not-Self & Liberation",
      description: "Anatta, the five aggregates, and nibbana.",
      icon: "sparkles",
    },
    {
      slug: "sutta-translations",
      folder: "06-sutta-translations",
      order: 6,
      title: "Sutta Translations",
      description: "Canonical discourse translations, organized by Nikaya.",
      icon: "scroll",
    },
    {
      slug: "monastic-life-and-the-sangha",
      folder: "07-monastic-life-and-the-sangha",
      order: 7,
      title: "Monastic Life & the Sangha",
      description: "Vinaya-derived material and monastic training guides.",
      icon: "users",
    },
    {
      slug: "teachers-and-traditions",
      folder: "08-teachers-and-traditions",
      order: 8,
      title: "Teachers & Traditions",
      description:
        "Essays and commentary from featured authors and Thai Forest tradition teachers.",
      icon: "user",
    },
  ],
  "atheism-secularism": [
    {
      slug: "arguments-for-atheism",
      folder: "01-arguments-for-atheism",
      order: 1,
      title: "Arguments for Atheism",
      description: "The positive case for nontheism, and what it means to live without belief in God.",
      icon: "sparkles",
    },
    {
      slug: "critiques-of-theistic-arguments",
      folder: "02-critiques-of-theistic-arguments",
      order: 2,
      title: "Critiques of Theistic Arguments",
      description: "Responses to cosmological, design, and miracle arguments, and the problem of evil.",
      icon: "scale",
    },
    {
      slug: "secular-ethics-and-morality",
      folder: "03-secular-ethics-and-morality",
      order: 3,
      title: "Secular Ethics & Morality",
      description: "Grounding morality without God, and whether atheists bear a burden of proof.",
      icon: "heart",
    },
    {
      slug: "faith-reason-and-agnosticism",
      folder: "04-faith-reason-and-agnosticism",
      order: 4,
      title: "Faith, Reason & Agnosticism",
      description: "Agnosticism, the reliability of faith as a path to knowledge, and logical reasoning.",
      icon: "help-circle",
    },
    {
      slug: "biblical-criticism",
      folder: "05-biblical-criticism",
      order: 5,
      title: "Biblical Criticism",
      description: "Skeptical analysis of biblical inconsistencies, errancy, and the Gospels.",
      icon: "scroll",
    },
    {
      slug: "church-state-and-society",
      folder: "06-church-state-and-society",
      order: 6,
      title: "Church, State & Society",
      description: "Secularism in public life, and the myth of America as a Christian nation.",
      icon: "landmark",
    },
    {
      slug: "death-mind-and-the-afterlife",
      folder: "07-death-mind-and-the-afterlife",
      order: 7,
      title: "Death, Mind & the Afterlife",
      description: "Secular treatments of near-death experiences and the case against immortality.",
      icon: "wind",
    },
  ],
};

export interface Subcategory {
  name: string;
  icon: string;
}

export const SUBCATEGORIES: Record<string, Record<string, Subcategory[]>> = {
  islam: {
    "answers-to-common-questions": [
      { name: "Deity of Christ", icon: "crown" },
      { name: "Bible & Quran", icon: "book" },
      { name: "Salvation & Atonement", icon: "heart" },
      { name: "Trinity & Godhead", icon: "book-open" },
      { name: "Women & Ethics", icon: "users" },
      { name: "Rebuttals", icon: "message-square" },
      { name: "General Topics", icon: "file-text" },
    ],
    "theological-issues": [
      { name: "Nature of Allah", icon: "alert-triangle" },
      { name: "Trinity & Monotheism", icon: "book-open" },
      { name: "Islamic Theology Critiqued", icon: "globe" },
      { name: "Salvation & Eschatology", icon: "heart" },
      { name: "OT Theology", icon: "book" },
      { name: "General Topics", icon: "file-text" },
    ],
    "quranic-issues": [
      { name: "Theology of the Quran", icon: "book-open" },
      { name: "Contradictions & Errors", icon: "alert-triangle" },
      { name: "Quran & the Bible", icon: "book" },
      { name: "Textual History", icon: "scroll" },
      { name: "Quran Stories & Figures", icon: "users" },
      { name: "Quranic Analysis", icon: "scroll" },
      { name: "General Topics", icon: "file-text" },
    ],
    "analysis-of-muhammad": [
      { name: "Deification of Muhammad", icon: "crown" },
      { name: "Character & Morality", icon: "alert-triangle" },
      { name: "Muhammad's Wives & Marriages", icon: "users" },
      { name: "False Prophecies", icon: "scroll" },
      { name: "Muhammad & Islamic Practice", icon: "globe" },
      { name: "Muhammad & Scripture", icon: "book" },
      { name: "Muhammad & Islam", icon: "alert-triangle" },
      { name: "General Topics", icon: "file-text" },
    ],
    "general-issues": [
      { name: "Translations", icon: "globe" },
      { name: "Rebuttals & Debates", icon: "message-square" },
      { name: "Apologetics & Defense", icon: "book-open" },
      { name: "Quran & Bible", icon: "scroll" },
      { name: "Women in Islam", icon: "users" },
      { name: "General Topics", icon: "file-text" },
    ],
  },
  "christian-theology": {
    "answers-to-common-questions": [
      { name: "Deity of Christ", icon: "crown" },
      { name: "Bible & Quran", icon: "book" },
      { name: "Salvation & Atonement", icon: "heart" },
      { name: "Trinity & Godhead", icon: "book-open" },
      { name: "Women & Ethics", icon: "users" },
      { name: "Rebuttals", icon: "message-square" },
      { name: "General Topics", icon: "file-text" },
    ],
    "christological-issues": [
      { name: "Christ's Deity & Identity", icon: "crown" },
      { name: "Messianic Prophecies", icon: "scroll" },
      { name: "NT Christology", icon: "book-open" },
      { name: "Christ in the Quran", icon: "globe" },
      { name: "Worship of Christ", icon: "heart" },
      { name: "Son of Man & Preexistence", icon: "wind" },
      { name: "Shema & Monotheism", icon: "book" },
      { name: "Christology", icon: "crown" },
      { name: "General Topics", icon: "file-text" },
    ],
    "theological-issues": [
      { name: "Trinity & Monotheism", icon: "book-open" },
      { name: "Salvation & Eschatology", icon: "heart" },
      { name: "OT Theology", icon: "book" },
      { name: "Trinity & Godhead", icon: "book-open" },
      { name: "Holy Spirit", icon: "wind" },
      { name: "Atonement & Salvation", icon: "heart" },
      { name: "General Topics", icon: "file-text" },
    ],
    "biblical-issues": [
      { name: "Biblical Studies", icon: "book" },
    ],
    "general-issues": [
      { name: "Rebuttals & Debates", icon: "message-square" },
      { name: "Apologetics & Defense", icon: "book-open" },
      { name: "Quran & Bible", icon: "scroll" },
      { name: "General Topics", icon: "file-text" },
    ],
    "church-history-and-denominations": [
      { name: "Roman Catholic", icon: "landmark" },
      { name: "Eastern Orthodox", icon: "church" },
      { name: "Oriental Orthodox & Christological Councils", icon: "scroll" },
      { name: "Protestant Reformation & Denominations", icon: "book-open" },
      { name: "Ecumenical Councils", icon: "users" },
      { name: "Patristic Theology", icon: "landmark" },
      { name: "Church & Sacraments", icon: "church" },
    ],
  },
  "eastern-traditions": {
    "sutta-translations": [
      { name: "Digha Nikaya", icon: "book" },
      { name: "Majjhima Nikaya", icon: "book" },
      { name: "Samyutta Nikaya", icon: "book" },
      { name: "Anguttara Nikaya", icon: "book" },
      { name: "Khuddaka Nikaya", icon: "book" },
    ],
  },
};

export function getTraditionBySlug(slug: string): Tradition | undefined {
  return TRADITIONS.find((t) => t.slug === slug);
}

export function getCategoryBySlug(
  tradition: string,
  slug: string
): Category | undefined {
  return (CATEGORIES[tradition] ?? []).find((c) => c.slug === slug);
}

export function getCategoryByFolder(
  tradition: string,
  folder: string
): Category | undefined {
  return (CATEGORIES[tradition] ?? []).find((c) => c.folder === folder);
}
