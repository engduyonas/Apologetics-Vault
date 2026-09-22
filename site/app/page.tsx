import Link from "next/link";
import { getCategoriesWithCounts, getTraditionsWithCounts, getTotalStats } from "@/lib/content";
import { getTraditionBySlug } from "@/lib/categories";
import CategoryIcon from "@/components/CategoryIcon";
import { BookOpen, Clock, Layers, Map } from "lucide-react";

export default function HomePage() {
  const home = getTraditionBySlug("christian-theology")!;
  const categories = getCategoriesWithCounts("christian-theology");
  const stats = getTotalStats("christian-theology");
  const otherTraditions = getTraditionsWithCounts().filter((t) => t.slug !== "christian-theology");

  return (
    <div className="max-w-6xl mx-auto px-6 lg:px-10 py-12">
      {/* Hero */}
      <div className="text-center mb-14">
        <h1 className="text-4xl sm:text-5xl font-bold text-warm-800 dark:text-cream-100 mb-4 font-serif">
          Fluent Faith
        </h1>
        <p className="text-lg text-warm-500 dark:text-warm-400 max-w-xl mx-auto leading-relaxed">
          A personal study library for knowing the Christian faith more
          deeply, and being able to explain and defend it fluently.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3 mt-6">
          <Link
            href="/christian-theology/why-christianity"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-700 dark:bg-slate-600 text-white text-sm font-medium hover:bg-slate-800 dark:hover:bg-slate-500 transition-colors"
          >
            Why Christianity?
          </Link>
          <Link
            href="/christian-theology/who-is-christ"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cream-100 dark:bg-warm-800 text-warm-800 dark:text-cream-100 text-sm font-medium border border-cream-300 dark:border-warm-700 hover:bg-cream-200 dark:hover:bg-warm-700 transition-colors"
          >
            Who Is Christ?
          </Link>
          <Link
            href="/guide"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cream-100 dark:bg-warm-800 text-warm-800 dark:text-cream-100 text-sm font-medium border border-cream-300 dark:border-warm-700 hover:bg-cream-200 dark:hover:bg-warm-700 transition-colors"
          >
            <Map className="w-4 h-4" />
            Guided tour
          </Link>
        </div>
      </div>

      {/* Stats (Christian Theology) */}
      <div className="flex justify-center gap-8 sm:gap-12 mb-10">
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

      {/* Christian Theology category grid — the home base */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-16">
        {categories.map((cat) => (
          <Link
            key={cat.slug}
            href={`/christian-theology/${cat.slug}`}
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

      {/* Other traditions — material for engaging with other perspectives */}
      <div>
        <h2 className="text-sm font-semibold text-warm-500 dark:text-warm-400 uppercase tracking-wide mb-1">
          Other Traditions
        </h2>
        <p className="text-sm text-warm-400 dark:text-warm-500 mb-4">
          Source material for understanding and engaging with other faiths.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {otherTraditions.map((t) => (
            <Link
              key={t.slug}
              href={`/${t.slug}`}
              className="group flex items-center gap-3 p-3.5 rounded-xl bg-cream-50 dark:bg-warm-800/40 hover:bg-cream-200/60 dark:hover:bg-warm-800/70 border border-cream-300/40 dark:border-warm-700/40 hover:border-slate-400/40 dark:hover:border-slate-600/30 transition-all"
            >
              <div className="p-1.5 rounded-lg bg-slate-100/40 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400 group-hover:bg-slate-100/70 dark:group-hover:bg-slate-900/25 transition-colors shrink-0">
                <CategoryIcon icon={t.icon} className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-warm-800 dark:text-cream-100 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors text-sm">
                  {t.title}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-medium mt-0.5">
                  {t.articleCount} article{t.articleCount !== 1 ? "s" : ""}
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
