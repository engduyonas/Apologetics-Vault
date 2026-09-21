"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { ArrowLeft, ArrowRight, Map } from "lucide-react";
import { getGuide } from "@/lib/guides";

export default function GuideNav({ tradition }: { tradition: string }) {
  const searchParams = useSearchParams();
  const guideParam = searchParams.get("guide");
  const stepParam = searchParams.get("step");

  if (!guideParam || stepParam === null) return null;

  const guide = getGuide(guideParam);
  const stepIndex = parseInt(stepParam, 10);
  if (!guide || Number.isNaN(stepIndex) || !guide.steps[stepIndex]) return null;

  const prevStep = guide.steps[stepIndex - 1];
  const nextStep = guide.steps[stepIndex + 1];

  const stepUrl = (index: number) => {
    const step = guide.steps[index];
    return `/${tradition}/${step.category}/${step.slug}?guide=${guideParam}&step=${index}`;
  };

  return (
    <div className="max-w-[58rem] mx-auto mb-6 px-4 py-3 rounded-xl bg-slate-100/50 dark:bg-slate-900/15 border border-slate-300/40 dark:border-slate-700/40 flex items-center gap-3 flex-wrap font-sans text-sm">
      <Link
        href={`/guide/${guideParam}`}
        className="flex items-center gap-1.5 text-slate-700 dark:text-slate-400 font-medium hover:text-slate-800 dark:hover:text-slate-300 transition-colors shrink-0"
      >
        <Map className="w-4 h-4" />
        {guide.title}
      </Link>
      <span className="text-slate-500 dark:text-slate-500 shrink-0">
        Step {stepIndex + 1} of {guide.steps.length}
      </span>
      <div className="flex-1" />
      {prevStep && (
        <Link
          href={stepUrl(stepIndex - 1)}
          className="flex items-center gap-1 text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Previous
        </Link>
      )}
      {nextStep && (
        <Link
          href={stepUrl(stepIndex + 1)}
          className="flex items-center gap-1 text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors"
        >
          Next
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      )}
    </div>
  );
}
