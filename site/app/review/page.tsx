"use client";

import { Flag } from "lucide-react";
import ArticleCard from "@/components/ArticleCard";
import { useFlags } from "@/lib/useFlags";

export default function ReviewPage() {
  const { flags, mounted } = useFlags();

  const sorted = [...flags].sort((a, b) => b.flaggedAt - a.flaggedAt);

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
      <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
        Review List
      </h1>
      <p className="text-warm-500 dark:text-warm-400 mb-6">
        Articles you&apos;ve flagged as weak spots to revisit until you can
        explain them fluently.
      </p>

      {!mounted ? null : sorted.length > 0 ? (
        <div>
          {sorted.map((f) => (
            <ArticleCard
              key={`${f.tradition}/${f.category}/${f.slug}`}
              title={f.title}
              slug={f.slug}
              tradition={f.tradition}
              category={f.category}
              categoryLabel={f.categoryLabel}
              readTime={f.readTime}
              series={f.series}
              part={f.part}
              subcategory={f.subcategory}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Flag className="w-12 h-12 mx-auto text-cream-300 dark:text-warm-600 mb-4" />
          <p className="text-warm-500 dark:text-warm-400">
            Nothing flagged yet. Tap the flag icon on any article you don&apos;t
            feel solid on yet, and it&apos;ll show up here to revisit.
          </p>
        </div>
      )}
    </div>
  );
}
