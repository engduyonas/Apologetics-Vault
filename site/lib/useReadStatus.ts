"use client";

import { useEffect, useState } from "react";
import { articleKey, getReadMap, setReadMap } from "./storage";

export function useReadStatus() {
  const [readMap, setReadMapState] = useState<Record<string, number>>({});
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setReadMapState(getReadMap());
    setMounted(true);
  }, []);

  function isRead(category: string, slug: string) {
    return Boolean(readMap[articleKey(category, slug)]);
  }

  function markRead(category: string, slug: string) {
    const key = articleKey(category, slug);
    setReadMapState((prev) => {
      if (prev[key]) return prev;
      const next = { ...prev, [key]: Date.now() };
      setReadMap(next);
      return next;
    });
  }

  return { isRead, markRead, mounted };
}
