"use client";

import { useEffect } from "react";
import { useReadStatus } from "@/lib/useReadStatus";

export default function MarkAsReadOnView({
  tradition,
  category,
  slug,
}: {
  tradition: string;
  category: string;
  slug: string;
}) {
  const { markRead, mounted } = useReadStatus();

  useEffect(() => {
    if (mounted) markRead(tradition, category, slug);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted, tradition, category, slug]);

  return null;
}
