import { notFound } from "next/navigation";
import Link from "next/link";
import { getArticle, getArticlesByCategory, getSeriesArticles } from "@/lib/content";
import { getCategoryBySlug, CATEGORIES } from "@/lib/categories";
import ReadingProgress from "@/components/ReadingProgress";
import TableOfContents from "@/components/TableOfContents";
import CategoryIcon from "@/components/CategoryIcon";
import { ChevronRight, Clock, ExternalLink, ArrowLeft, ArrowRight } from "lucide-react";

export function generateStaticParams() {
  const params: { category: string; slug: string }[] = [];
  for (const cat of CATEGORIES) {
    const articles = getArticlesByCategory(cat.slug);
    for (const a of articles) {
      params.push({ category: cat.slug, slug: a.slug });
    }
  }
  return params;
}

interface Props {
  params: Promise<{ category: string; slug: string }>;
}

export default async function ArticlePage({ params }: Props) {
  const { category: categorySlug, slug } = await params;
  const category = getCategoryBySlug(categorySlug);
  if (!category) notFound();

  const article = await getArticle(categorySlug, slug);
  if (!article) notFound();

  let prevArticle = null;
  let nextArticle = null;

  if (article.series) {
    const seriesParts = getSeriesArticles(article.series, categorySlug);
    const currentIdx = seriesParts.findIndex((a) => a.slug === slug);
    if (currentIdx > 0) prevArticle = seriesParts[currentIdx - 1];
    if (currentIdx < seriesParts.length - 1)
      nextArticle = seriesParts[currentIdx + 1];
  }

  let headingIndex = 0;
  const htmlWithIds = article.htmlContent.replace(
    /<(h[23])>(.*?)<\/h[23]>/g,
    (_match, tag, content) => {
      const id = `heading-${headingIndex++}`;
      return `<${tag} id="${id}">${content}</${tag}>`;
    }
  );

  return (
    <>
      <ReadingProgress />

      <div className="px-6 lg:px-14 xl:px-20 py-10 flex gap-10">
        <article className="flex-1 min-w-0 mx-auto">
          {/* Breadcrumb */}
          <nav className="flex items-center gap-1.5 text-sm text-warm-500 dark:text-warm-400 mb-10 flex-wrap font-sans max-w-[58rem] mx-auto">
            <Link
              href="/"
              className="hover:text-warm-600 dark:hover:text-cream-400 transition-colors"
            >
              Home
            </Link>
            <ChevronRight className="w-3.5 h-3.5 shrink-0" />
            <Link
              href={`/${categorySlug}`}
              className="hover:text-warm-600 dark:hover:text-cream-400 transition-colors"
            >
              {category.title}
            </Link>
            <ChevronRight className="w-3.5 h-3.5 shrink-0" />
            <span className="text-warm-700 dark:text-cream-200 font-medium truncate">
              {article.title}
            </span>
          </nav>

          {/* Paper container */}
          <div className="bg-cream-50 dark:bg-warm-900 rounded-xl shadow-sm dark:shadow-warm-800/20 px-8 sm:px-12 lg:px-20 xl:px-28 py-12 lg:py-16 border border-cream-300/50 dark:border-warm-700/50">
            {/* Title block — centered like the prose column */}
            <header className="max-w-[58rem] mx-auto">
              <h1 className="font-serif text-3xl sm:text-4xl font-bold text-warm-800 dark:text-cream-100 leading-tight tracking-tight mb-5">
                {article.title}
              </h1>

              {/* Meta */}
              <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-sm text-warm-500 dark:text-warm-400 pb-6 font-sans">
                <Link
                  href={`/${categorySlug}`}
                  className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-cream-200 dark:bg-warm-800 text-warm-600 dark:text-warm-400 hover:bg-cream-300 dark:hover:bg-warm-700 transition-colors"
                >
                  <CategoryIcon icon={category.icon} className="w-3 h-3" />
                  {category.title}
                </Link>
                {article.subcategory && (
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100/60 dark:bg-slate-900/15 text-slate-700 dark:text-slate-400">
                    {article.subcategory}
                  </span>
                )}
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {article.readTime} min read
                </span>
                {article.series && (
                  <span className="px-2.5 py-0.5 bg-slate-100 dark:bg-slate-900/20 text-slate-700 dark:text-slate-400 rounded-full text-xs font-medium">
                    {article.series}
                    {article.part ? ` — Part ${article.part}` : ""}
                  </span>
                )}
                {article.source && (
                  <a
                    href={article.source}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1 hover:text-warm-600 dark:hover:text-cream-400 transition-colors ml-auto"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    Source
                  </a>
                )}
              </div>

              {/* Ornamental divider */}
              <div className="article-divider" aria-hidden="true">
                <span className="text-xs">◆</span>
              </div>
            </header>

            {/* Prose body */}
            <div className="mt-10">
              <div
                className="prose-kindle [&_h2]:scroll-mt-20 [&_h3]:scroll-mt-20"
                dangerouslySetInnerHTML={{ __html: htmlWithIds }}
              />
            </div>
          </div>

          {/* Series Navigation */}
          {(prevArticle || nextArticle) && (
            <div className="mt-12 pt-6 border-t border-cream-300 dark:border-warm-700 grid grid-cols-2 gap-4 font-sans max-w-[58rem] mx-auto">
              {prevArticle ? (
                <Link
                  href={`/${categorySlug}/${prevArticle.slug}`}
                  className="group p-4 rounded-lg bg-cream-50 dark:bg-warm-800/50 hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors"
                >
                  <span className="text-xs text-warm-500 dark:text-warm-400 flex items-center gap-1">
                    <ArrowLeft className="w-3 h-3" /> Previous
                  </span>
                  <span className="block mt-1 text-sm font-medium text-warm-700 dark:text-cream-200 group-hover:text-warm-800 dark:group-hover:text-cream-100 transition-colors line-clamp-2">
                    {prevArticle.title}
                  </span>
                </Link>
              ) : (
                <div />
              )}
              {nextArticle ? (
                <Link
                  href={`/${categorySlug}/${nextArticle.slug}`}
                  className="group p-4 rounded-lg bg-cream-50 dark:bg-warm-800/50 hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors text-right"
                >
                  <span className="text-xs text-warm-500 dark:text-warm-400 flex items-center justify-end gap-1">
                    Next <ArrowRight className="w-3 h-3" />
                  </span>
                  <span className="block mt-1 text-sm font-medium text-warm-700 dark:text-cream-200 group-hover:text-warm-800 dark:group-hover:text-cream-100 transition-colors line-clamp-2">
                    {nextArticle.title}
                  </span>
                </Link>
              ) : (
                <div />
              )}
            </div>
          )}

          {/* Back link */}
          <div className="mt-10 font-sans max-w-[58rem] mx-auto">
            <Link
              href={`/${categorySlug}`}
              className="text-sm text-warm-500 dark:text-warm-400 hover:text-warm-600 dark:hover:text-cream-400 transition-colors flex items-center gap-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Back to {category.title}
            </Link>
          </div>
        </article>

        <TableOfContents htmlContent={htmlWithIds} />
      </div>
    </>
  );
}
