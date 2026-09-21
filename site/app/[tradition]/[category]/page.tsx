import { Suspense } from "react";
import { notFound } from "next/navigation";
import Link from "next/link";
import { TRADITIONS, CATEGORIES, SUBCATEGORIES, getCategoryBySlug, getTraditionBySlug } from "@/lib/categories";
import { getArticlesByCategory } from "@/lib/content";
import ArticleCard from "@/components/ArticleCard";
import CategoryIcon from "@/components/CategoryIcon";
import SubcategoryAccordion from "@/components/SubcategoryAccordion";
import { ChevronRight } from "lucide-react";

export function generateStaticParams() {
  return TRADITIONS.flatMap((t) =>
    (CATEGORIES[t.slug] ?? []).map((c) => ({ tradition: t.slug, category: c.slug }))
  );
}

interface Props {
  params: Promise<{ tradition: string; category: string }>;
}

export default async function CategoryPage({ params }: Props) {
  const { tradition: traditionSlug, category: categorySlug } = await params;
  const tradition = getTraditionBySlug(traditionSlug);
  if (!tradition) notFound();

  const category = getCategoryBySlug(traditionSlug, categorySlug);
  if (!category) notFound();

  const articles = getArticlesByCategory(traditionSlug, categorySlug);
  const subcategoryDefs = SUBCATEGORIES[traditionSlug]?.[categorySlug];
  const hasSubcategories =
    subcategoryDefs && articles.some((a) => a.subcategory);

  const subcategoriesWithCounts = hasSubcategories
    ? subcategoryDefs
        .map((sub) => ({
          ...sub,
          count: articles.filter((a) => a.subcategory === sub.name).length,
        }))
        .filter((s) => s.count > 0)
    : [];

  const allArticleData = articles.map((a) => ({
    title: a.title,
    slug: a.slug,
    tradition: a.tradition,
    category: a.category,
    readTime: a.readTime,
    subcategory: a.subcategory,
    series: a.series,
    part: a.part,
  }));

  const ungrouped = hasSubcategories
    ? allArticleData.filter(
        (a) => !a.subcategory || !subcategoryDefs.some((s) => s.name === a.subcategory)
      )
    : [];

  return (
    <div className="max-w-7xl mx-auto px-6 lg:px-12 py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm text-warm-500 dark:text-warm-400 mb-6">
        <Link
          href="/"
          className="hover:text-warm-600 dark:hover:text-cream-400 transition-colors"
        >
          Home
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <Link
          href={`/${traditionSlug}`}
          className="hover:text-warm-600 dark:hover:text-cream-400 transition-colors"
        >
          {tradition.title}
        </Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-warm-800 dark:text-cream-100 font-medium">
          {category.title}
        </span>
      </nav>

      {/* Header */}
      <div className="flex items-start gap-4 mb-10">
        <div className="p-3 rounded-xl bg-slate-100/50 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400">
          <CategoryIcon icon={category.icon} className="w-7 h-7" />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-warm-800 dark:text-cream-50 font-serif">
            {category.title}
          </h1>
          <p className="text-lg text-warm-500 dark:text-warm-400 mt-1">
            {category.description}
          </p>
          <p className="text-base text-warm-400 dark:text-warm-500 mt-1">
            {articles.length} article{articles.length !== 1 ? "s" : ""}
          </p>
        </div>
      </div>

      {/* Subcategory accordion */}
      {hasSubcategories ? (
        <Suspense fallback={null}>
          <SubcategoryAccordion
            subcategories={subcategoriesWithCounts}
            articles={allArticleData}
            ungrouped={ungrouped}
          />
        </Suspense>
      ) : (
        <div>
          {articles.map((article) => (
            <ArticleCard
              key={article.slug}
              title={article.title}
              slug={article.slug}
              tradition={article.tradition}
              category={article.category}
              readTime={article.readTime}
              series={article.series}
              part={article.part}
            />
          ))}
        </div>
      )}

      {articles.length === 0 && (
        <p className="text-center text-warm-400 dark:text-warm-500 py-12">
          No articles in this category yet. Run the scraper to populate content.
        </p>
      )}
    </div>
  );
}
