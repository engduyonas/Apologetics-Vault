import { ListChecks } from "lucide-react";
import { KEY_POINTS } from "@/lib/key-points";

export default function KeyPoints({
  tradition,
  category,
  slug,
}: {
  tradition: string;
  category: string;
  slug: string;
}) {
  const points = KEY_POINTS[`${tradition}/${category}/${slug}`];
  if (!points || points.length === 0) return null;

  return (
    <div className="max-w-[58rem] mx-auto mb-8 p-5 rounded-xl bg-slate-50/60 dark:bg-slate-900/15 border border-slate-300/40 dark:border-slate-700/40 font-sans">
      <h2 className="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-400 uppercase tracking-wide mb-3">
        <ListChecks className="w-4 h-4" />
        Key Points
      </h2>
      <ul className="space-y-2">
        {points.map((point, i) => (
          <li
            key={i}
            className="flex items-start gap-2.5 text-sm text-warm-700 dark:text-cream-200 leading-snug"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-slate-500 dark:bg-slate-400 mt-1.5 shrink-0" />
            {point}
          </li>
        ))}
      </ul>
    </div>
  );
}
