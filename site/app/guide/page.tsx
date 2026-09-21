import Link from "next/link";
import { GUIDES } from "@/lib/guides";
import { getTraditionBySlug } from "@/lib/categories";
import CategoryIcon from "@/components/CategoryIcon";
import { Map } from "lucide-react";

export default function GuideLandingPage() {
  const guides = Object.values(GUIDES)
    .map((g) => ({ guide: g, tradition: getTraditionBySlug(g.tradition) }))
    .filter((g) => g.tradition);

  return (
    <div className="max-w-4xl mx-auto px-6 lg:px-10 py-12">
      <div className="text-center mb-12">
        <Map className="w-10 h-10 mx-auto mb-4 text-slate-600 dark:text-slate-400" />
        <h1 className="text-4xl font-bold text-warm-800 dark:text-cream-100 mb-4 font-serif">
          Start Here
        </h1>
        <p className="text-lg text-warm-500 dark:text-warm-400 max-w-xl mx-auto leading-relaxed">
          New to the library? Pick a tradition below for a short, guided
          sequence of articles that walks through its core topics one step
          at a time.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {guides.map(({ guide, tradition }) => (
          <Link
            key={guide.tradition}
            href={`/guide/${guide.tradition}`}
            className="group flex items-start gap-4 p-5 rounded-xl bg-cream-50 dark:bg-warm-800/40 hover:bg-cream-200/60 dark:hover:bg-warm-800/70 border border-cream-300/40 dark:border-warm-700/40 hover:border-slate-400/40 dark:hover:border-slate-600/30 transition-all"
          >
            <div className="p-2.5 rounded-lg bg-slate-100/40 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400 group-hover:bg-slate-100/70 dark:group-hover:bg-slate-900/25 transition-colors shrink-0">
              <CategoryIcon icon={tradition!.icon} className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="font-semibold text-warm-800 dark:text-cream-100 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors text-lg font-serif">
                {guide.title}
              </h2>
              <p className="text-sm text-warm-400 dark:text-warm-500 mt-1 leading-snug">
                {guide.description}
              </p>
              <p className="text-xs text-slate-600 dark:text-slate-400 font-medium mt-2">
                {guide.steps.length} steps
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
