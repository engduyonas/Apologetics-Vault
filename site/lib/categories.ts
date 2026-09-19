export interface Tradition {
  slug: string;
  order: number;
  title: string;
  description: string;
  icon: string;
}

export const TRADITIONS: Tradition[] = [
  {
    slug: "islam",
    order: 1,
    title: "Islam",
    description:
      "Christian apologetics and comparative theology addressing Islam, drawn from Sam Shamoun's work.",
    icon: "moon-star",
  },
  {
    slug: "eastern-traditions",
    order: 2,
    title: "Eastern Traditions",
    description:
      "Theravada Buddhist teachings and texts, drawn from Access to Insight.",
    icon: "flower",
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
        "Responses to frequently asked questions and common claims about Christianity and Islam.",
      icon: "help-circle",
    },
    {
      slug: "christological-issues",
      folder: "02-christological-issues",
      order: 2,
      title: "Christological Issues",
      description:
        "The deity, nature, and identity of Jesus Christ examined from biblical and Islamic perspectives.",
      icon: "crown",
    },
    {
      slug: "theological-issues",
      folder: "03-theological-issues",
      order: 3,
      title: "Theological Issues",
      description:
        "The Trinity, monotheism, the nature of God, and comparative theology.",
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
    {
      slug: "short-summaries",
      folder: "12-short-summaries",
      order: 12,
      title: "Short Summaries",
      description: "Concise summary articles on key theological points.",
      icon: "align-left",
    },
    {
      slug: "blog-posts",
      folder: "13-blog-posts",
      order: 13,
      title: "Blog Posts",
      description:
        "Recent blog posts from Theology Sphere covering patristic theology and advanced topics.",
      icon: "pen-tool",
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
    "christological-issues": [
      { name: "Christ's Deity & Identity", icon: "crown" },
      { name: "Messianic Prophecies", icon: "scroll" },
      { name: "NT Christology", icon: "book-open" },
      { name: "Christ in the Quran", icon: "globe" },
      { name: "Worship of Christ", icon: "heart" },
      { name: "Son of Man & Preexistence", icon: "wind" },
      { name: "Shema & Monotheism", icon: "book" },
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
      { name: "General Topics", icon: "file-text" },
    ],
    "analysis-of-muhammad": [
      { name: "Deification of Muhammad", icon: "crown" },
      { name: "Character & Morality", icon: "alert-triangle" },
      { name: "Muhammad's Wives & Marriages", icon: "users" },
      { name: "False Prophecies", icon: "scroll" },
      { name: "Muhammad & Islamic Practice", icon: "globe" },
      { name: "Muhammad & Scripture", icon: "book" },
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
    "blog-posts": [
      { name: "Christology", icon: "crown" },
      { name: "Trinity & Godhead", icon: "book-open" },
      { name: "Holy Spirit", icon: "wind" },
      { name: "Atonement & Salvation", icon: "heart" },
      { name: "Patristic Theology", icon: "landmark" },
      { name: "Church & Sacraments", icon: "church" },
      { name: "Biblical Studies", icon: "book" },
      { name: "Quranic Analysis", icon: "scroll" },
      { name: "Muhammad & Islam", icon: "alert-triangle" },
      { name: "Rebuttals & Debates", icon: "message-square" },
      { name: "General Topics", icon: "file-text" },
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
