"use client";

import { Flag } from "lucide-react";
import { useFlags } from "@/lib/useFlags";
import type { FlagEntry } from "@/lib/storage";

export default function FlagButton({
  article,
  size = "sm",
}: {
  article: Omit<FlagEntry, "flaggedAt">;
  size?: "sm" | "md";
}) {
  const { isFlagged, toggleFlag, mounted } = useFlags();

  if (!mounted) {
    return <div className={size === "sm" ? "w-7 h-7" : "w-9 h-9"} />;
  }

  const flagged = isFlagged(article.tradition, article.category, article.slug);
  const iconSize = size === "sm" ? "w-4 h-4" : "w-5 h-5";

  return (
    <button
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        toggleFlag(article);
      }}
      aria-label={flagged ? "Remove from review list" : "Flag for review"}
      aria-pressed={flagged}
      title={flagged ? "Flagged for review" : "Flag for review"}
      className={`shrink-0 rounded-md transition-colors ${
        size === "sm" ? "p-1.5" : "p-2"
      } ${
        flagged
          ? "text-amber-600 dark:text-amber-400"
          : "text-warm-400 dark:text-warm-500 hover:text-warm-600 dark:hover:text-cream-400"
      } hover:bg-cream-200 dark:hover:bg-warm-800`}
    >
      <Flag className={iconSize} fill={flagged ? "currentColor" : "none"} />
    </button>
  );
}
