import { notFound } from "next/navigation";
import Link from "next/link";
import { getGuide, GUIDES } from "@/lib/guides";
import { getTraditionBySlug, getCategoryBySlug } from "@/lib/categories";
import { getArticles } from "@/lib/content";
import GuideStepList from "@/components/GuideStepList";
import { ChevronRight, Map as MapIcon } from "lucide-react";

export function generateStaticParams() {
  return Object.keys(GUIDES).map((tradition) => ({ tradition }));
}

interface Props {
  params: Promise<{ tradition: string }>;
}

export default async function GuidePage({ params }: Props) {
  const { tradition: traditionSlug } = await params;
  const guide = getGuide(traditionSlug);
  const tradition = getTraditionBySlug(traditionSlug);
  if (!guide || !tradition) notFound();

  const articles = getArticles(traditionSlug);
  const articleMap = new Map(articles.map((a) => [`${a.category}/${a.slug}`, a]));

  const steps = guide.steps.map((step, index) => {
    const article = articleMap.get(`${step.category}/${step.slug}`);
    const category = getCategoryBySlug(traditionSlug, step.category);
    return {
      index,
      note: step.note,
      title: article?.title ?? step.slug,
      readTime: article?.readTime ?? 0,
      categoryTitle: category?.title ?? step.category,
      category: step.category,
      slug: step.slug,
    };
  });

  return (
    <div className="max-w-3xl mx-auto px-6 lg:px-10 py-12">
      <nav className="flex items-center gap-1.5 text-sm text-warm-500 dark:text-warm-400 mb-8">
        <Link href="/guide" className="hover:text-warm-600 dark:hover:text-cream-400 transition-colors flex items-center gap-1">
          <MapIcon className="w-3.5 h-3.5" />
          Start Here
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-warm-800 dark:text-cream-100 font-medium">{tradition.title}</span>
      </nav>

      <div className="mb-10">
        <h1 className="text-3xl font-bold text-warm-800 dark:text-cream-50 font-serif mb-2">
          {guide.title}
        </h1>
        <p className="text-lg text-warm-500 dark:text-warm-400">{guide.description}</p>
      </div>

      <GuideStepList tradition={traditionSlug} steps={steps} />
    </div>
  );
}
