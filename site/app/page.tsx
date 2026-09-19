import Link from "next/link";
import { getTraditionsWithCounts, getTotalStats } from "@/lib/content";
import CategoryIcon from "@/components/CategoryIcon";
import { BookOpen, Clock, Layers, Map } from "lucide-react";

export default function HomePage() {
  const traditions = getTraditionsWithCounts();
  const stats = getTotalStats();

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-12">
      {/* Hero */}
      <div className="text-center mb-14">
        <h1 className="text-4xl sm:text-5xl font-bold text-warm-800 dark:text-cream-100 mb-4 font-serif">
          Apologetics Vault
        </h1>
        <p className="text-lg text-warm-500 dark:text-warm-400 max-w-xl mx-auto leading-relaxed">
          A curated, multi-perspective library of comparative religion and
          theology &mdash; scholarship from within and about the world&apos;s
          major traditions.
        </p>
        <Link
          href="/guide"
          className="inline-flex items-center gap-2 mt-6 px-4 py-2 rounded-lg bg-slate-700 dark:bg-slate-600 text-white text-sm font-medium hover:bg-slate-800 dark:hover:bg-slate-500 transition-colors"
        >
          <Map className="w-4 h-4" />
          New here? Start with a guided tour
        </Link>
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
            {traditions.length}
          </p>
          <p className="text-xs text-warm-400 dark:text-warm-500 mt-0.5">Traditions</p>
        </div>
        <div className="text-center">
          <Clock className="w-5 h-5 mx-auto mb-1.5 text-slate-600 dark:text-slate-400" />
          <p className="text-2xl font-bold text-warm-800 dark:text-cream-100">
            {stats.totalReadTimeHours}h
          </p>
          <p className="text-xs text-warm-400 dark:text-warm-500 mt-0.5">Reading</p>
        </div>
      </div>

      {/* Tradition Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {traditions.map((t) => (
          <Link
            key={t.slug}
            href={`/${t.slug}`}
            className="group flex items-start gap-4 p-5 rounded-xl bg-cream-50 dark:bg-warm-800/40 hover:bg-cream-200/60 dark:hover:bg-warm-800/70 border border-cream-300/40 dark:border-warm-700/40 hover:border-slate-400/40 dark:hover:border-slate-600/30 transition-all"
          >
            <div className="p-2.5 rounded-lg bg-slate-100/40 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400 group-hover:bg-slate-100/70 dark:group-hover:bg-slate-900/25 transition-colors shrink-0">
              <CategoryIcon icon={t.icon} className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="font-semibold text-warm-800 dark:text-cream-100 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors text-lg font-serif">
                {t.title}
              </h2>
              <p className="text-sm text-warm-400 dark:text-warm-500 mt-1 leading-snug">
                {t.description}
              </p>
              <p className="text-xs text-slate-600 dark:text-slate-400 font-medium mt-2">
                {t.articleCount} article{t.articleCount !== 1 ? "s" : ""} &middot; {t.categoryCount} categor{t.categoryCount !== 1 ? "ies" : "y"}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
