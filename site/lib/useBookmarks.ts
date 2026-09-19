"use client";

import { useEffect, useState } from "react";
import {
  articleKey,
  getBookmarks,
  setBookmarks,
  type BookmarkEntry,
} from "./storage";

export function useBookmarks() {
  const [bookmarks, setBookmarksState] = useState<BookmarkEntry[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setBookmarksState(getBookmarks());
    setMounted(true);
  }, []);

  function isBookmarked(tradition: string, category: string, slug: string) {
    const key = articleKey(tradition, category, slug);
    return bookmarks.some((b) => articleKey(b.tradition, b.category, b.slug) === key);
  }

  function toggleBookmark(entry: Omit<BookmarkEntry, "bookmarkedAt">) {
    setBookmarksState((prev) => {
      const key = articleKey(entry.tradition, entry.category, entry.slug);
      const exists = prev.some((b) => articleKey(b.tradition, b.category, b.slug) === key);
      const next = exists
        ? prev.filter((b) => articleKey(b.tradition, b.category, b.slug) !== key)
        : [...prev, { ...entry, bookmarkedAt: Date.now() }];
      setBookmarks(next);
      return next;
    });
  }

  return { bookmarks, isBookmarked, toggleBookmark, mounted };
}
