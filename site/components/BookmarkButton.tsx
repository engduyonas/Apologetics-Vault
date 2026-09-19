"use client";

import { Bookmark, BookmarkCheck } from "lucide-react";
import { useBookmarks } from "@/lib/useBookmarks";
import type { BookmarkEntry } from "@/lib/storage";

export default function BookmarkButton({
  article,
  size = "sm",
}: {
  article: Omit<BookmarkEntry, "bookmarkedAt">;
  size?: "sm" | "md";
}) {
  const { isBookmarked, toggleBookmark, mounted } = useBookmarks();

  if (!mounted) {
    return <div className={size === "sm" ? "w-7 h-7" : "w-9 h-9"} />;
  }

  const bookmarked = isBookmarked(article.tradition, article.category, article.slug);
  const iconSize = size === "sm" ? "w-4 h-4" : "w-5 h-5";

  return (
    <button
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleBookmark(article);
      }}
      aria-label={bookmarked ? "Remove bookmark" : "Add bookmark"}
      aria-pressed={bookmarked}
      className={`shrink-0 rounded-md transition-colors ${
        size === "sm" ? "p-1.5" : "p-2"
      } ${
        bookmarked
          ? "text-slate-700 dark:text-slate-400"
          : "text-warm-400 dark:text-warm-500 hover:text-warm-600 dark:hover:text-cream-400"
      } hover:bg-cream-200 dark:hover:bg-warm-800`}
    >
      {bookmarked ? (
        <BookmarkCheck className={iconSize} fill="currentColor" />
      ) : (
        <Bookmark className={iconSize} />
      )}
    </button>
  );
}
