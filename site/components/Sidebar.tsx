"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import CategoryIcon from "./CategoryIcon";

interface SidebarCategory {
  slug: string;
  title: string;
  icon: string;
  articleCount: number;
}

interface SidebarTradition {
  slug: string;
  title: string;
  icon: string;
}

export default function Sidebar({
  traditions,
  categoriesByTradition,
  onNavigate,
  collapseButton,
}: {
  traditions: SidebarTradition[];
  categoriesByTradition: Record<string, SidebarCategory[]>;
  onNavigate?: () => void;
  collapseButton?: React.ReactNode;
}) {
  const pathname = usePathname();
  const firstSegment = pathname.split("/")[1];
  const activeTradition = traditions.find((t) => t.slug === firstSegment);
  const categories = activeTradition
    ? categoriesByTradition[activeTradition.slug] ?? []
    : [];

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between px-4 py-5 border-b border-cream-300 dark:border-warm-700">
        <Link
          href="/"
          onClick={onNavigate}
          className="flex items-center gap-3"
        >
          <div className="w-8 h-8 rounded-lg bg-slate-700 dark:bg-slate-600 flex items-center justify-center text-white font-bold text-xs tracking-tight">
            FF
          </div>
          <div>
            <h1 className="font-bold text-warm-800 dark:text-cream-100 text-sm leading-tight">
              Fluent
            </h1>
            <p className="text-[10px] text-warm-500 dark:text-warm-400 leading-tight">
              Faith
            </p>
          </div>
        </Link>
        {collapseButton}
      </div>

      {/* Tradition switcher */}
      <div className="flex flex-wrap gap-1.5 px-4 py-3 border-b border-cream-300 dark:border-warm-700">
        {traditions.map((t) => {
          const isActive = t.slug === activeTradition?.slug;
          return (
            <Link
              key={t.slug}
              href={`/${t.slug}`}
              onClick={() => onNavigate?.()}
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                isActive
                  ? "bg-slate-700 dark:bg-slate-600 text-white"
                  : "bg-cream-200 dark:bg-warm-800 text-warm-600 dark:text-warm-400 hover:bg-cream-300 dark:hover:bg-warm-700"
              }`}
            >
              <CategoryIcon icon={t.icon} className="w-3 h-3" />
              {t.title}
            </Link>
          );
        })}
      </div>

      {activeTradition && (
        <nav className="flex-1 overflow-y-auto py-3 px-2">
          <ul className="space-y-0.5">
            {categories.map((cat) => {
              const isActive = pathname.startsWith(`/${activeTradition.slug}/${cat.slug}`);

              return (
                <li key={cat.slug}>
                  <Link
                    href={`/${activeTradition.slug}/${cat.slug}`}
                    onClick={() => onNavigate?.()}
                    className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors ${
                      isActive
                        ? "bg-slate-100/60 dark:bg-slate-900/15 text-slate-800 dark:text-slate-400 font-medium"
                        : "text-warm-700 dark:text-warm-300 hover:bg-cream-200 dark:hover:bg-warm-800"
                    }`}
                  >
                    <CategoryIcon
                      icon={cat.icon}
                      className={`w-4 h-4 shrink-0 ${
                        isActive
                          ? "text-slate-700 dark:text-slate-400"
                          : "text-warm-400 dark:text-warm-500"
                      }`}
                    />
                    <span className="flex-1 leading-snug">{cat.title}</span>
                    <span
                      className={`text-xs px-1.5 py-0.5 rounded-full shrink-0 ${
                        isActive
                          ? "bg-slate-200/60 dark:bg-slate-800/30 text-slate-800 dark:text-slate-300"
                          : "bg-cream-300/60 dark:bg-warm-700 text-warm-500 dark:text-warm-400"
                      }`}
                    >
                      {cat.articleCount}
                    </span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      )}
    </div>
  );
}
