import { getArticles, type ArticleMeta } from "@/lib/content";
import { CATEGORIES } from "@/lib/categories";
import SearchResults from "./SearchResults";

export default function SearchPage() {
  const articles = getArticles();

  const categoryMap: Record<string, string> = {};
  for (const c of CATEGORIES) {
    categoryMap[c.slug] = c.title;
  }

  const searchData = articles.map((a: ArticleMeta) => ({
    title: a.title,
    slug: a.slug,
    category: a.category,
    categoryLabel: categoryMap[a.category] || a.category,
    readTime: a.readTime,
    series: a.series,
    part: a.part,
    subcategory: a.subcategory,
  }));

  return <SearchResults articles={searchData} />;
}
