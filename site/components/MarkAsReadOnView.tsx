"use client";

import { useEffect } from "react";
import { useReadStatus } from "@/lib/useReadStatus";

export default function MarkAsReadOnView({
  category,
  slug,
}: {
  category: string;
  slug: string;
}) {
  const { markRead, mounted } = useReadStatus();

  useEffect(() => {
    if (mounted) markRead(category, slug);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted, category, slug]);

  return null;
}
