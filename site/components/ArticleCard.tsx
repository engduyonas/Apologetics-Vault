import Link from "next/link";
import { Clock } from "lucide-react";
import BookmarkButton from "./BookmarkButton";
import FlagButton from "./FlagButton";
import ReadIndicator from "./ReadIndicator";

interface ArticleCardProps {
  title: string;
  slug: string;
  tradition: string;
  category: string;
  categoryLabel?: string;
  readTime: number;
  series?: string;
  part?: string;
  subcategory?: string;
}

export default function ArticleCard({
  title,
  slug,
  tradition,
  category,
  categoryLabel,
  readTime,
  series,
  part,
  subcategory,
}: ArticleCardProps) {
  return (
    <Link
      href={`/${tradition}/${category}/${slug}`}
      className="group flex items-center justify-between gap-4 py-3.5 px-3 -mx-3 rounded-md hover:bg-cream-200/60 dark:hover:bg-warm-800/60 transition-colors border-b border-cream-300/50 dark:border-warm-700/50 last:border-b-0"
    >
      <div className="min-w-0">
        <h3 className="flex items-center gap-2 text-warm-800 dark:text-cream-200 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors leading-snug text-base">
          <ReadIndicator tradition={tradition} category={category} slug={slug} />
          {series && part && (
            <span className="text-warm-400 dark:text-warm-500 text-sm font-medium font-sans">
              Pt. {part}
            </span>
          )}
          {title}
        </h3>
        <div className="flex items-center gap-2 mt-1.5">
          {categoryLabel && (
            <span className="text-xs px-2 py-0.5 rounded bg-cream-200 dark:bg-warm-800 text-warm-500 dark:text-warm-400 font-sans">
              {categoryLabel}
            </span>
          )}
          {subcategory && (
            <span className="text-xs px-2 py-0.5 rounded bg-slate-100/50 dark:bg-slate-900/10 text-slate-700 dark:text-slate-400 font-sans">
              {subcategory}
            </span>
          )}
        </div>
      </div>
      <div className="shrink-0 flex items-center gap-3">
        <span className="text-sm text-warm-400 dark:text-warm-500 flex items-center gap-1 font-sans tabular-nums">
          <Clock className="w-3.5 h-3.5" />
          {readTime}m
        </span>
        <FlagButton
          article={{ title, slug, tradition, category, categoryLabel: categoryLabel || category, readTime, series, part, subcategory }}
        />
        <BookmarkButton
          article={{ title, slug, tradition, category, categoryLabel: categoryLabel || category, readTime, series, part, subcategory }}
        />
      </div>
    </Link>
  );
}
