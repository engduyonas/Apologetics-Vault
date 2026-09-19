"use client";

import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import MiniSearch from "minisearch";
import Link from "next/link";
import { Search, Clock, X } from "lucide-react";
import CategoryIcon from "@/components/CategoryIcon";
import { CATEGORIES } from "@/lib/categories";
import type { SearchDoc } from "@/lib/content";

function highlight(text: string, terms: string[]) {
  if (terms.length === 0) return text;
  const pattern = new RegExp(
    `(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`,
    "gi"
  );
  const parts = text.split(pattern);
  return parts.map((part, i) =>
    terms.some((t) => part.toLowerCase() === t.toLowerCase()) ? (
      <mark
        key={i}
        className="bg-slate-200/70 dark:bg-slate-700/50 text-warm-800 dark:text-cream-100 rounded-sm"
      >
        {part}
      </mark>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

function Results() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const q = searchParams.get("q") || "";
  const categoryFilter = searchParams.get("category") || "";

  const [docs, setDocs] = useState<SearchDoc[] | null>(null);
  const [index, setIndex] = useState<MiniSearch<SearchDoc> | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("/search-index.json")
      .then((res) => {
        if (!res.ok) throw new Error("failed to load search index");
        return res.json();
      })
      .then((data: SearchDoc[]) => {
        setDocs(data);
        const mini = new MiniSearch<SearchDoc>({
          idField: "id",
          fields: ["title", "excerpt", "series"],
          storeFields: [
            "title",
            "slug",
            "category",
            "categoryLabel",
            "subcategory",
            "series",
            "part",
            "readTime",
            "excerpt",
          ],
          searchOptions: {
            boost: { title: 3, series: 1.5 },
            fuzzy: 0.15,
            prefix: true,
          },
        });
        mini.addAll(data);
        setIndex(mini);
      })
      .catch(() => setError(true));
  }, []);

  const results = useMemo(() => {
    if (!index || q.trim().length < 2) return [];
    const hits = index.search(q.trim());
    return categoryFilter
      ? hits.filter((h) => h.category === categoryFilter)
      : hits;
  }, [index, q, categoryFilter]);

  const availableCategories = useMemo(() => {
    if (!index || q.trim().length < 2) return [];
    const hits = index.search(q.trim());
    const counts = new Map<string, number>();
    for (const h of hits) {
      counts.set(h.category, (counts.get(h.category) || 0) + 1);
    }
    return CATEGORIES.filter((c) => counts.has(c.slug)).map((c) => ({
      ...c,
      count: counts.get(c.slug)!,
    }));
  }, [index, q]);

  const terms = q.trim().length >= 2 ? q.trim().split(/\s+/) : [];

  function setCategoryFilter(slug: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (slug === categoryFilter) {
      params.delete("category");
    } else {
      params.set("category", slug);
    }
    router.push(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
      <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
        Search Results
      </h1>

      {!q ? (
        <p className="text-warm-500 dark:text-warm-400 mb-6">
          Type a query in the search bar above.
        </p>
      ) : error ? (
        <p className="text-warm-500 dark:text-warm-400 mb-6">
          Couldn&apos;t load the search index. Try refreshing the page.
        </p>
      ) : !docs ? (
        <p className="text-warm-500 dark:text-warm-400 mb-6">Loading…</p>
      ) : (
        <>
          <p className="text-warm-500 dark:text-warm-400 mb-4">
            {results.length} result{results.length !== 1 ? "s" : ""} for &quot;
            <span className="font-medium text-warm-700 dark:text-cream-200">
              {q}
            </span>
            &quot;
          </p>

          {availableCategories.length > 1 && (
            <div className="flex flex-wrap gap-2 mb-6">
              {availableCategories.map((c) => (
                <button
                  key={c.slug}
                  onClick={() => setCategoryFilter(c.slug)}
                  className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                    categoryFilter === c.slug
                      ? "bg-slate-700 dark:bg-slate-600 text-white"
                      : "bg-cream-200 dark:bg-warm-800 text-warm-600 dark:text-warm-400 hover:bg-cream-300 dark:hover:bg-warm-700"
                  }`}
                >
                  <CategoryIcon icon={c.icon} className="w-3 h-3" />
                  {c.title}
                  <span className="tabular-nums opacity-70">{c.count}</span>
                  {categoryFilter === c.slug && <X className="w-3 h-3" />}
                </button>
              ))}
            </div>
          )}

          {results.length > 0 ? (
            <div className="space-y-1">
              {results.map((r) => (
                <Link
                  key={r.id}
                  href={`/${r.category}/${r.slug}`}
                  className="group block py-3.5 px-3 -mx-3 rounded-md hover:bg-cream-200/60 dark:hover:bg-warm-800/60 transition-colors border-b border-cream-300/50 dark:border-warm-700/50 last:border-b-0"
                >
                  <div className="flex items-center justify-between gap-4">
                    <h3 className="text-warm-800 dark:text-cream-200 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors leading-snug text-base min-w-0">
                      {highlight(r.title as string, terms)}
                    </h3>
                    <span className="shrink-0 text-sm text-warm-400 dark:text-warm-500 flex items-center gap-1 font-sans tabular-nums">
                      <Clock className="w-3.5 h-3.5" />
                      {r.readTime}m
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                    <span className="text-xs px-2 py-0.5 rounded bg-cream-200 dark:bg-warm-800 text-warm-500 dark:text-warm-400 font-sans">
                      {r.categoryLabel}
                    </span>
                    {r.subcategory && (
                      <span className="text-xs px-2 py-0.5 rounded bg-slate-100/50 dark:bg-slate-900/10 text-slate-700 dark:text-slate-400 font-sans">
                        {r.subcategory}
                      </span>
                    )}
                  </div>
                  {r.excerpt && (
                    <p className="text-sm text-warm-500 dark:text-warm-400 mt-1.5 leading-snug line-clamp-2">
                      {highlight(r.excerpt as string, terms)}
                    </p>
                  )}
                </Link>
              ))}
            </div>
          ) : q.trim().length >= 2 ? (
            <div className="text-center py-16">
              <Search className="w-12 h-12 mx-auto text-cream-300 dark:text-warm-600 mb-4" />
              <p className="text-warm-500 dark:text-warm-400">
                No articles matching your search. Try a different query.
              </p>
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}

export default function SearchResults() {
  return (
    <Suspense
      fallback={
        <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
          <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
            Search Results
          </h1>
          <p className="text-warm-500 dark:text-warm-400 mb-6">Loading...</p>
        </div>
      }
    >
      <Results />
    </Suspense>
  );
}
