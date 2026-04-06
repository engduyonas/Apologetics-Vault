import Link from "next/link";
import { getCategoriesWithCounts, getTotalStats } from "@/lib/content";
import CategoryIcon from "@/components/CategoryIcon";
import { BookOpen, Clock, Layers } from "lucide-react";

export default function HomePage() {
  const categories = getCategoriesWithCounts();
  const stats = getTotalStats();

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-12">
      {/* Hero */}
      <div className="text-center mb-14">
        <h1 className="text-4xl sm:text-5xl font-bold text-warm-800 dark:text-cream-100 mb-4 font-serif">
          Apologetics Vault
        </h1>
        <p className="text-lg text-warm-500 dark:text-warm-400 max-w-xl mx-auto leading-relaxed">
          A curated library of Christian apologetics &mdash; theology,
          Christology, and comparative religion with Islam.
        </p>
      </div>

      {/* Stats */}
      <div className="flex justify-center gap-8 sm:gap-12 mb-14">
        <div className="text-center">
          <BookOpen className="w-5 h-5 mx-auto mb-1.5 text-slate-600 dark:text-slate-400" />
          <p className="text-2xl font-bold text-warm-800 dark:text-cream-100">
            {stats.totalArticles}
          </p>
          <p className="text-xs text-warm-400 dark:text-warm-500 mt-0.5">Articles</p>
        </div>
        <div className="text-center">
          <Layers className="w-5 h-5 mx-auto mb-1.5 text-slate-600 dark:text-slate-400" />
          <p className="text-2xl font-bold text-warm-800 dark:text-cream-100">
            {stats.totalCategories}
          </p>
          <p className="text-xs text-warm-400 dark:text-warm-500 mt-0.5">Categories</p>
        </div>
        <div className="text-center">
          <Clock className="w-5 h-5 mx-auto mb-1.5 text-slate-600 dark:text-slate-400" />
          <p className="text-2xl font-bold text-warm-800 dark:text-cream-100">
            {stats.totalReadTimeHours}h
          </p>
          <p className="text-xs text-warm-400 dark:text-warm-500 mt-0.5">Reading</p>
        </div>
      </div>

      {/* Category Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {categories.map((cat) => (
          <Link
            key={cat.slug}
            href={`/${cat.slug}`}
            className="group flex items-start gap-3 p-4 rounded-xl bg-cream-50 dark:bg-warm-800/40 hover:bg-cream-200/60 dark:hover:bg-warm-800/70 border border-cream-300/40 dark:border-warm-700/40 hover:border-slate-400/40 dark:hover:border-slate-600/30 transition-all"
          >
            <div className="p-2 rounded-lg bg-slate-100/40 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400 group-hover:bg-slate-100/70 dark:group-hover:bg-slate-900/25 transition-colors shrink-0">
              <CategoryIcon icon={cat.icon} className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="font-semibold text-warm-800 dark:text-cream-100 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors text-[0.95rem]">
                {cat.title}
              </h2>
              <p className="text-sm text-warm-400 dark:text-warm-500 mt-0.5 line-clamp-2 leading-snug">
                {cat.description}
              </p>
              <p className="text-xs text-slate-600 dark:text-slate-400 font-medium mt-2">
                {cat.articleCount} article{cat.articleCount !== 1 ? "s" : ""}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
