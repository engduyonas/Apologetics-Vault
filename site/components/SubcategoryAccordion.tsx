"use client";

import { useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ChevronDown, Search } from "lucide-react";
import CategoryIcon from "./CategoryIcon";
import ReadIndicator from "./ReadIndicator";

interface ArticleItem {
  title: string;
  slug: string;
  category: string;
  readTime: number;
  subcategory?: string;
  series?: string;
  part?: string;
}

interface SubcategoryDef {
  name: string;
  icon: string;
  count: number;
}

export default function SubcategoryAccordion({
  subcategories,
  articles,
  ungrouped,
}: {
  subcategories: SubcategoryDef[];
  articles: ArticleItem[];
  ungrouped: ArticleItem[];
}) {
  const searchParams = useSearchParams();
  const subParam = searchParams.get("sub");
  const initialOpen = subParam && subcategories.some((s) => s.name === subParam)
    ? subParam
    : null;

  const [openSections, setOpenSections] = useState<Record<string, boolean>>(
    initialOpen ? { [initialOpen]: true } : {}
  );
  const [filter, setFilter] = useState("");
  const q = filter.trim().toLowerCase();

  const toggle = (name: string) =>
    setOpenSections((prev) => ({ ...prev, [name]: !prev[name] }));

  const matchesFilter = (a: ArticleItem) => a.title.toLowerCase().includes(q);

  const totalMatches = useMemo(() => {
    if (!q) return 0;
    return (
      articles.filter(matchesFilter).length +
      ungrouped.filter(matchesFilter).length
    );
  }, [q, articles, ungrouped]);

  const renderArticles = (items: ArticleItem[]) => {
    const seriesMap = new Map<string, ArticleItem[]>();
    const standalone: ArticleItem[] = [];

    for (const a of items) {
      if (a.series) {
        const existing = seriesMap.get(a.series) || [];
        existing.push(a);
        seriesMap.set(a.series, existing);
      } else {
        standalone.push(a);
      }
    }

    for (const [, parts] of seriesMap) {
      parts.sort((a, b) =>
        (a.part || "").localeCompare(b.part || "", undefined, { numeric: true })
      );
    }

    const sortedSeries = Array.from(seriesMap.entries()).sort(([a], [b]) =>
      a.localeCompare(b)
    );

    const entries: { type: "series"; name: string; parts: ArticleItem[] }[] | { type: "single"; article: ArticleItem }[] = [];

    const mixed: ({ type: "series"; name: string; parts: ArticleItem[] } | { type: "single"; article: ArticleItem })[] = [];

    for (const [name, parts] of sortedSeries) {
      mixed.push({ type: "series", name, parts });
    }
    for (const article of standalone) {
      mixed.push({ type: "single", article });
    }

    return (
      <>
        {mixed.map((entry, idx) => {
          if (entry.type === "series") {
            return (
              <div key={entry.name} className="mb-4">
                <h4 className="text-base font-semibold text-warm-600 dark:text-warm-300 mb-2 flex items-center gap-2.5 font-sans">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-500 dark:bg-slate-400" />
                  {entry.name}
                </h4>
                <div className="pl-4 border-l border-cream-400/40 dark:border-warm-600/60">
                  {entry.parts.map((article) => (
                    <ArticleRow key={`${article.slug}-${article.part}`} article={article} showPart />
                  ))}
                </div>
              </div>
            );
          }
          return (
            <div key={`${entry.article.slug}-${idx}`} className="mb-4">
              <div className="flex items-center gap-2.5">
                <span className="w-1.5 h-1.5 rounded-full bg-slate-500 dark:bg-slate-400 shrink-0" />
                <ArticleRow article={entry.article} />
              </div>
            </div>
          );
        })}
      </>
    );
  };

  return (
    <div>
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-warm-400 dark:text-warm-500" />
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter articles in this category..."
          className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-cream-300 dark:border-warm-600 bg-cream-50 dark:bg-warm-800 text-warm-800 dark:text-cream-200 placeholder-warm-400 dark:placeholder-warm-500 focus:outline-none focus:ring-2 focus:ring-slate-500/50 dark:focus:ring-slate-600/40 text-sm"
        />
        {q && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-warm-400 dark:text-warm-500 tabular-nums">
            {totalMatches} match{totalMatches !== 1 ? "es" : ""}
          </span>
        )}
      </div>

      {q && totalMatches === 0 ? (
        <p className="text-center text-warm-400 dark:text-warm-500 py-10 text-sm">
          No articles match &quot;{filter.trim()}&quot;.
        </p>
      ) : (
        <div className="space-y-2">
      {subcategories.map((sub) => {
        const allSubArticles = articles.filter((a) => a.subcategory === sub.name);
        const subArticles = q ? allSubArticles.filter(matchesFilter) : allSubArticles;
        if (subArticles.length === 0) return null;
        const isOpen = q ? true : openSections[sub.name] ?? false;

        return (
          <div
            key={sub.name}
            className="rounded-lg border border-cream-300/50 dark:border-warm-700/50 overflow-hidden"
          >
            <button
              onClick={() => !q && toggle(sub.name)}
              className={`w-full flex items-center gap-3 px-5 py-4 text-left transition-colors ${
                isOpen
                  ? "bg-slate-50/50 dark:bg-slate-900/10"
                  : "hover:bg-cream-200/40 dark:hover:bg-warm-800/40"
              }`}
            >
              <CategoryIcon
                icon={sub.icon}
                className={`w-5 h-5 shrink-0 ${
                  isOpen
                    ? "text-slate-600 dark:text-slate-400"
                    : "text-warm-400 dark:text-warm-500"
                }`}
              />
              <span className={`flex-1 text-lg font-medium ${
                isOpen
                  ? "text-slate-800 dark:text-slate-300"
                  : "text-warm-700 dark:text-cream-200"
              }`}>
                {sub.name}
              </span>
              <span className="text-sm text-warm-400 dark:text-warm-500 tabular-nums mr-2">
                {subArticles.length}
              </span>
              <ChevronDown
                className={`w-5 h-5 text-warm-400 dark:text-warm-500 transition-transform duration-150 ${
                  isOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {isOpen && (
              <div className="px-5 pb-5 pt-3">
                {renderArticles(subArticles)}
              </div>
            )}
          </div>
        );
      })}

      {(() => {
        const filteredUngrouped = q ? ungrouped.filter(matchesFilter) : ungrouped;
        if (filteredUngrouped.length === 0) return null;
        const isUngroupedOpen = q ? true : openSections["__ungrouped__"] ?? false;

        return (
          <div className="rounded-lg border border-cream-300/50 dark:border-warm-700/50 overflow-hidden">
            <button
              onClick={() => !q && toggle("__ungrouped__")}
              className={`w-full flex items-center gap-3 px-4 py-3 text-left transition-colors ${
                isUngroupedOpen
                  ? "bg-slate-50/50 dark:bg-slate-900/10"
                  : "hover:bg-cream-200/40 dark:hover:bg-warm-800/40"
              }`}
            >
              <CategoryIcon
                icon="file-text"
                className={`w-4 h-4 shrink-0 ${
                  isUngroupedOpen
                    ? "text-slate-600 dark:text-slate-400"
                    : "text-warm-400 dark:text-warm-500"
                }`}
              />
              <span className={`flex-1 text-base font-medium ${
                isUngroupedOpen
                  ? "text-slate-800 dark:text-slate-300"
                  : "text-warm-700 dark:text-cream-200"
              }`}>
                Other
              </span>
              <span className="text-xs text-warm-400 dark:text-warm-500 tabular-nums mr-2">
                {filteredUngrouped.length}
              </span>
              <ChevronDown
                className={`w-4 h-4 text-warm-400 dark:text-warm-500 transition-transform duration-150 ${
                  isUngroupedOpen ? "rotate-180" : ""
                }`}
              />
            </button>

            {isUngroupedOpen && (
              <div className="px-4 pb-4 pt-2">
                {renderArticles(filteredUngrouped)}
              </div>
            )}
          </div>
        );
      })()}
        </div>
      )}
    </div>
  );
}

function ArticleRow({
  article,
  showPart,
}: {
  article: { title: string; slug: string; category: string; readTime: number; part?: string };
  showPart?: boolean;
}) {
  return (
    <a
      href={`/${article.category}/${article.slug}`}
      className="group flex items-center justify-between gap-4 py-3 px-3 -mx-3 rounded-md hover:bg-cream-200/60 dark:hover:bg-warm-800/60 transition-colors border-b border-cream-300/30 dark:border-warm-700/30 last:border-b-0"
    >
      <span className="flex items-center gap-2 text-warm-800 dark:text-cream-200 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors leading-snug text-[1.05rem]">
        <ReadIndicator category={article.category} slug={article.slug} />
        {showPart && article.part && (
          <span className="text-warm-400 dark:text-warm-500 text-sm font-medium font-sans">
            Pt. {article.part}
          </span>
        )}
        {article.title}
      </span>
      <span className="shrink-0 text-sm text-warm-400 dark:text-warm-500 tabular-nums">
        {article.readTime}m
      </span>
    </a>
  );
}
