"use client";

import Link from "next/link";
import { Clock, Check } from "lucide-react";
import { useReadStatus } from "@/lib/useReadStatus";

interface Step {
  index: number;
  note: string;
  title: string;
  readTime: number;
  categoryTitle: string;
  category: string;
  slug: string;
}

export default function GuideStepList({
  tradition,
  steps,
}: {
  tradition: string;
  steps: Step[];
}) {
  const { isRead, mounted } = useReadStatus();
  const completed = mounted
    ? steps.filter((s) => isRead(tradition, s.category, s.slug)).length
    : 0;

  return (
    <div>
      {mounted && (
        <div className="flex items-center gap-3 mb-8">
          <div className="flex-1 h-1.5 rounded-full bg-cream-200 dark:bg-warm-800 overflow-hidden">
            <div
              className="h-full bg-slate-600 dark:bg-slate-400 transition-all"
              style={{ width: `${(completed / steps.length) * 100}%` }}
            />
          </div>
          <span className="text-xs text-warm-500 dark:text-warm-400 tabular-nums shrink-0">
            {completed} / {steps.length} read
          </span>
        </div>
      )}

      <ol className="space-y-3">
        {steps.map((step) => {
          const done = mounted && isRead(tradition, step.category, step.slug);
          return (
            <li key={`${step.category}/${step.slug}`}>
              <Link
                href={`/${tradition}/${step.category}/${step.slug}?guide=${tradition}&step=${step.index}`}
                className="group flex items-start gap-4 p-4 rounded-xl bg-cream-50 dark:bg-warm-800/40 hover:bg-cream-200/60 dark:hover:bg-warm-800/70 border border-cream-300/40 dark:border-warm-700/40 hover:border-slate-400/40 dark:hover:border-slate-600/30 transition-all"
              >
                <div
                  className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold shrink-0 mt-0.5 ${
                    done
                      ? "bg-slate-700 dark:bg-slate-600 text-white"
                      : "bg-cream-200 dark:bg-warm-800 text-warm-500 dark:text-warm-400"
                  }`}
                >
                  {done ? <Check className="w-4 h-4" /> : step.index + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold text-warm-800 dark:text-cream-100 group-hover:text-slate-800 dark:group-hover:text-slate-400 transition-colors">
                    {step.title}
                  </h3>
                  <p className="text-sm text-warm-400 dark:text-warm-500 mt-0.5 leading-snug">
                    {step.note}
                  </p>
                  <div className="flex items-center gap-2 mt-1.5 text-xs text-warm-400 dark:text-warm-500">
                    <span>{step.categoryTitle}</span>
                    <span>&middot;</span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {step.readTime}m
                    </span>
                  </div>
                </div>
              </Link>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
