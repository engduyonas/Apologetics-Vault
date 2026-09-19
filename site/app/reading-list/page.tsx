"use client";

import { Bookmark } from "lucide-react";
import ArticleCard from "@/components/ArticleCard";
import { useBookmarks } from "@/lib/useBookmarks";

export default function ReadingListPage() {
  const { bookmarks, mounted } = useBookmarks();

  const sorted = [...bookmarks].sort((a, b) => b.bookmarkedAt - a.bookmarkedAt);

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
      <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
        Reading List
      </h1>
      <p className="text-warm-500 dark:text-warm-400 mb-6">
        Articles you&apos;ve bookmarked, saved in this browser.
      </p>

      {!mounted ? null : sorted.length > 0 ? (
        <div>
          {sorted.map((b) => (
            <ArticleCard
              key={`${b.category}/${b.slug}`}
              title={b.title}
              slug={b.slug}
              category={b.category}
              categoryLabel={b.categoryLabel}
              readTime={b.readTime}
              series={b.series}
              part={b.part}
              subcategory={b.subcategory}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Bookmark className="w-12 h-12 mx-auto text-cream-300 dark:text-warm-600 mb-4" />
          <p className="text-warm-500 dark:text-warm-400">
            No bookmarks yet. Tap the bookmark icon on any article to save it
            here.
          </p>
        </div>
      )}
    </div>
  );
}
