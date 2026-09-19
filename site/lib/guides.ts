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
      "A guided tour through the core of the site's case, one representative question from each major topic area.",
    steps: [
      {
        category: "answers-to-common-questions",
        slug: "is-the-savior-necessarily-god",
        note: "A common objection to the deity of Christ, and the case for why it doesn't hold up — a good entry point into the site's central argument.",
      },
      {
        category: "christological-issues",
        slug: "ot-appearances-of-christ-as-the-angel-of-god",
        note: "Moves from the general question of Christ's deity into a specific, concrete line of evidence for it.",
      },
      {
        category: "theological-issues",
        slug: "more-merciful-than-the-most-merciful",
        note: "Shifts focus from Christology to the nature of God as understood in Islamic theology.",
      },
      {
        category: "biblical-issues",
        slug: "does-the-holy-bible-claim-to-be-the-inspired-word-of-god",
        note: "Addresses the reliability and self-understanding of the Bible, foundational to everything argued from it.",
      },
      {
        category: "quranic-issues",
        slug: "the-gods-of-islam-unveiled",
        note: "Turns to the Quran itself, examining a claim from the Islamic text directly.",
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
