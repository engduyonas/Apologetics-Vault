export interface GuideStep {
  category: string;
  slug: string;
  note: string;
}

export interface Guide {
  tradition: string;
  title: string;
  description: string;
  steps: GuideStep[];
}

export const GUIDES: Record<string, Guide> = {
  islam: {
    tradition: "islam",
    title: "Start Here: Islam",
    description:
      "A guided tour through the site's examination of Islamic sources and claims, one piece from each major topic area.",
    steps: [
      {
        category: "answers-to-common-questions",
        slug: "isnt-muhammad-that-prophet-awaited-by-the-jews",
        note: "A common claim about Muhammad's place in prophetic expectation, examined closely.",
      },
      {
        category: "theological-issues",
        slug: "more-merciful-than-the-most-merciful",
        note: "The nature of Allah as understood in Islamic theology.",
      },
      {
        category: "quranic-issues",
        slug: "the-gods-of-islam-unveiled",
        note: "A claim from the Islamic text examined directly.",
      },
      {
        category: "analysis-of-muhammad",
        slug: "how-will-a-muslim-be-saved-according-to-the-hadiths",
        note: "Looks at what the hadith literature says about salvation in Islam.",
      },
      {
        category: "hadith-analysis",
        slug: "islamic-science-fiction-the-thunder-and-the-moon",
        note: "A closer look at specific claims within the hadith corpus.",
      },
      {
        category: "turning-the-tables",
        slug: "turning-the-tables-pt-1a",
        note: "Applies standards Muslim polemicists use against other faiths back onto Islamic sources.",
      },
      {
        category: "polemical-issues",
        slug: "sunni-islams-real-shahadah",
        note: "A close examination of Islam's central confession of faith.",
      },
      {
        category: "general-issues",
        slug: "muhammad-as-al-amin-the-trustworthy",
        note: "A well-known epithet for Muhammad, examined against the historical record.",
      },
    ],
  },
  "christian-theology": {
    tradition: "christian-theology",
    title: "Start Here: Christian Theology",
    description:
      "A guided tour through the site's exposition of Christian doctrine, one piece from each major topic area.",
    steps: [
      {
        category: "answers-to-common-questions",
        slug: "is-the-savior-necessarily-god",
        note: "A common objection to the deity of Christ, and the case for why it doesn't hold up — a good entry point.",
      },
      {
        category: "christological-issues",
        slug: "ot-appearances-of-christ-as-the-angel-of-god",
        note: "Moves from the general question of Christ's deity into a specific, concrete line of evidence for it.",
      },
      {
        category: "theological-issues",
        slug: "is-gabriel-really-the-holy-spirit",
        note: "A question at the intersection of Christology and the doctrine of the Trinity.",
      },
      {
        category: "biblical-issues",
        slug: "does-the-holy-bible-claim-to-be-the-inspired-word-of-god",
        note: "Addresses the reliability and self-understanding of the Bible, foundational to everything argued from it.",
      },
      {
        category: "polemical-issues",
        slug: "the-apostles-of-christ-messengers-of-god-or-mere-disciples",
        note: "A close look at how the New Testament itself frames the apostles' role and authority.",
      },
      {
        category: "general-issues",
        slug: "the-historicity-of-jonah-examined",
        note: "A test case for how the site handles questions of biblical historicity.",
      },
      {
        category: "church-history-and-denominations",
        slug: "the-reformation",
        note: "Steps outside Shamoun's own writing into the site's public-domain reference material on church history.",
      },
      {
        category: "short-summaries",
        slug: "jesus-christ-the-absolutely-and-essentially-good-god",
        note: "A concise closing statement of the section's central claim.",
      },
    ],
  },
  "eastern-traditions": {
    tradition: "eastern-traditions",
    title: "Start Here: Buddhism",
    description:
      "One piece from each category, tracing a natural path from core doctrine through practice to community and lineage.",
    steps: [
      {
        category: "core-teachings",
        slug: "the-four-noble-truths",
        note: "The foundational framework the rest of the teaching builds on.",
      },
      {
        category: "meditation-and-mental-development",
        slug: "basic-breath-meditation-instructions",
        note: "A concrete, practical instruction — moving from doctrine to practice.",
      },
      {
        category: "ethics-and-conduct",
        slug: "the-healing-power-of-the-precepts",
        note: "The ethical framework that supports both practice and doctrine.",
      },
      {
        category: "kamma-and-rebirth",
        slug: "kamma",
        note: "The causal framework underlying Buddhist ethics and practice.",
      },
      {
        category: "not-self-and-liberation",
        slug: "no-self-or-not-self",
        note: "One of Buddhism's most distinctive and often misunderstood ideas.",
      },
      {
        category: "sutta-translations",
        slug: "dhammacakkappavattana-sutta",
        note: "The Buddha's first recorded teaching — seeing the doctrine in its original canonical form.",
      },
      {
        category: "monastic-life-and-the-sangha",
        slug: "vinaya-pitaka",
        note: "An overview of the monastic community and the code that shapes it.",
      },
      {
        category: "teachers-and-traditions",
        slug: "thai-forest-traditions",
        note: "How this teaching has been carried forward by a living lineage of practitioners.",
      },
    ],
  },
};

export function getGuide(tradition: string): Guide | undefined {
  return GUIDES[tradition];
}
