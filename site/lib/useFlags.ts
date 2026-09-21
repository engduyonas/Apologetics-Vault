"use client";

import { useEffect, useState } from "react";
import {
  articleKey,
  getFlags,
  setFlags,
  type FlagEntry,
} from "./storage";

export function useFlags() {
  const [flags, setFlagsState] = useState<FlagEntry[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setFlagsState(getFlags());
    setMounted(true);
  }, []);

  function isFlagged(tradition: string, category: string, slug: string) {
    const key = articleKey(tradition, category, slug);
    return flags.some((f) => articleKey(f.tradition, f.category, f.slug) === key);
  }

  function toggleFlag(entry: Omit<FlagEntry, "flaggedAt">) {
    setFlagsState((prev) => {
      const key = articleKey(entry.tradition, entry.category, entry.slug);
      const exists = prev.some((f) => articleKey(f.tradition, f.category, f.slug) === key);
      const next = exists
        ? prev.filter((f) => articleKey(f.tradition, f.category, f.slug) !== key)
        : [...prev, { ...entry, flaggedAt: Date.now() }];
      setFlags(next);
      return next;
    });
  }

  return { flags, isFlagged, toggleFlag, mounted };
}
