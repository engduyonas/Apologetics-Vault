"use client";

import { useReadStatus } from "@/lib/useReadStatus";

export default function ReadIndicator({
  tradition,
  category,
  slug,
}: {
  tradition: string;
  category: string;
  slug: string;
}) {
  const { isRead, mounted } = useReadStatus();

  if (!mounted || !isRead(tradition, category, slug)) return null;

  return (
    <span
      className="shrink-0 w-1.5 h-1.5 rounded-full bg-slate-500 dark:bg-slate-400"
      title="Read"
      aria-label="Read"
    />
  );
}
