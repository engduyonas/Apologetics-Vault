"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import ArticleCard from "@/components/ArticleCard";
import { Search } from "lucide-react";

interface SearchArticle {
  title: string;
  slug: string;
  category: string;
  categoryLabel: string;
  readTime: number;
  series?: string;
  part?: string;
  subcategory?: string;
}

function Results({ articles }: { articles: SearchArticle[] }) {
  const searchParams = useSearchParams();
  const q = searchParams.get("q") || "";

  const results = q.trim().length >= 2
    ? articles.filter(
        (a) =>
          a.title.toLowerCase().includes(q.toLowerCase()) ||
          (a.series && a.series.toLowerCase().includes(q.toLowerCase()))
      )
    : [];

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
      <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
        Search Results
      </h1>

      {q ? (
        <p className="text-warm-500 dark:text-warm-400 mb-6">
          {results.length} result{results.length !== 1 ? "s" : ""} for &quot;
          <span className="font-medium text-warm-700 dark:text-cream-200">
            {q}
          </span>
          &quot;
        </p>
      ) : (
        <p className="text-warm-500 dark:text-warm-400 mb-6">
          Type a query in the search bar above.
        </p>
      )}

      {results.length > 0 ? (
        <div>
          {results.map((article) => (
            <ArticleCard
              key={`${article.category}/${article.slug}`}
              title={article.title}
              slug={article.slug}
              category={article.category}
              categoryLabel={article.categoryLabel}
              readTime={article.readTime}
              series={article.series}
              part={article.part}
              subcategory={article.subcategory}
            />
          ))}
        </div>
      ) : q ? (
        <div className="text-center py-16">
          <Search className="w-12 h-12 mx-auto text-cream-300 dark:text-warm-600 mb-4" />
          <p className="text-warm-500 dark:text-warm-400">
            No articles matching your search. Try a different query.
          </p>
        </div>
      ) : null}
    </div>
  );
}

export default function SearchResults({ articles }: { articles: SearchArticle[] }) {
  return (
    <Suspense fallback={
      <div className="max-w-6xl mx-auto px-6 lg:px-10 py-8">
        <h1 className="text-2xl font-bold text-warm-800 dark:text-cream-50 mb-2 font-serif">
          Search Results
        </h1>
        <p className="text-warm-500 dark:text-warm-400 mb-6">Loading...</p>
      </div>
    }>
      <Results articles={articles} />
    </Suspense>
  );
}
