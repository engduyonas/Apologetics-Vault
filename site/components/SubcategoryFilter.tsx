"use client";

import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { useEffect, useRef } from "react";
import CategoryIcon from "./CategoryIcon";

interface SubcategoryItem {
  name: string;
  icon: string;
  count: number;
}

interface ArticleItem {
  title: string;
  slug: string;
  category: string;
  readTime: number;
  subcategory?: string;
  series?: string;
  part?: string;
}

export default function SubcategoryFilter({
  subcategories,
  articles,
}: {
  subcategories: SubcategoryItem[];
  articles: ArticleItem[];
}) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const subParam = searchParams.get("sub");
  const active =
    subParam && subcategories.some((s) => s.name === subParam)
      ? subParam
      : null;

  const setActive = (name: string | null) => {
    if (name) {
      router.push(`${pathname}?sub=${encodeURIComponent(name)}`, {
        scroll: false,
      });
    } else {
      router.push(pathname, { scroll: false });
    }
  };

  const filtered = active
    ? articles.filter((a) => a.subcategory === active)
    : articles;

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (active && containerRef.current) {
      containerRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [active]);

  return (
    <div ref={containerRef} className="scroll-mt-20">
      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-8">
        <button
          onClick={() => setActive(null)}
          className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
            active === null
              ? "bg-slate-700 text-white dark:bg-slate-600"
              : "bg-cream-200 dark:bg-warm-800 text-warm-600 dark:text-warm-400 hover:bg-cream-300 dark:hover:bg-warm-700"
          }`}
        >
          All ({articles.length})
        </button>
        {subcategories.map((sub) => (
          <button
            key={sub.name}
            onClick={() => setActive(active === sub.name ? null : sub.name)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors flex items-center gap-1.5 ${
              active === sub.name
                ? "bg-slate-700 text-white dark:bg-slate-600"
                : "bg-cream-200 dark:bg-warm-800 text-warm-600 dark:text-warm-400 hover:bg-cream-300 dark:hover:bg-warm-700"
            }`}
          >
            <CategoryIcon icon={sub.icon} className="w-3.5 h-3.5" />
            {sub.name} ({sub.count})
          </button>
        ))}
      </div>

      {/* Article list */}
      <div>
        {active === null ? (
          subcategories.map((sub) => {
            const subArticles = articles.filter(
              (a) => a.subcategory === sub.name
            );
            if (subArticles.length === 0) return null;
            return (
              <div key={sub.name} className="mb-8">
                <h2 className="text-base font-semibold text-warm-700 dark:text-cream-200 mb-2 flex items-center gap-2 font-sans">
                  <CategoryIcon
                    icon={sub.icon}
                    className="w-4 h-4 text-slate-600 dark:text-slate-400"
                  />
                  {sub.name}
                  <span className="text-xs font-normal text-warm-400 dark:text-warm-500">
                    ({subArticles.length})
                  </span>
                </h2>
                <div className="pl-4 border-l-2 border-cream-400/60 dark:border-warm-600">
                  {subArticles.map((article, idx) => (
                    <a
                      key={`${article.slug}-${idx}`}
                      href={`/${article.category}/${article.slug}`}
                      className="group flex items-baseline justify-between gap-4 py-3 px-2 -mx-2 rounded-md hover:bg-cream-200/60 dark:hover:bg-warm-800/60 transition-colors border-b border-cream-300/50 dark:border-warm-700/50 last:border-b-0"
                    >
                      <span className="text-warm-800 dark:text-cream-200 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors leading-snug text-[0.95rem]">
                        {article.title}
                      </span>
                      <span className="shrink-0 text-xs text-warm-400 dark:text-warm-500 tabular-nums">
                        {article.readTime}m
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            );
          })
        ) : (
          <div>
            {filtered.map((article, idx) => (
              <a
                key={`${article.slug}-${idx}`}
                href={`/${article.category}/${article.slug}`}
                className="group flex items-baseline justify-between gap-4 py-3 px-2 -mx-2 rounded-md hover:bg-cream-200/60 dark:hover:bg-warm-800/60 transition-colors border-b border-cream-300/50 dark:border-warm-700/50 last:border-b-0"
              >
                <span className="text-warm-800 dark:text-cream-200 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors leading-snug text-[0.95rem]">
                  {article.title}
                </span>
                <span className="shrink-0 text-xs text-warm-400 dark:text-warm-500 tabular-nums">
                  {article.readTime}m
                </span>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
