import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { remark } from "remark";
import remarkGfm from "remark-gfm";
import remarkHtml from "remark-html";
import { CATEGORIES, SUBCATEGORIES, getCategoryByFolder } from "./categories";

const CONTENT_DIR = path.join(process.cwd(), "..", "content");

export interface ArticleMeta {
  title: string;
  slug: string;
  category: string;
  folder: string;
  source: string;
  series?: string;
  part?: string;
  rebuttalTo?: string;
  subcategory?: string;
  wordCount: number;
  readTime: number;
}

export interface Article extends ArticleMeta {
  content: string;
  htmlContent: string;
}

export interface CategoryWithCount {
  slug: string;
  folder: string;
  order: number;
  title: string;
  description: string;
  icon: string;
  articleCount: number;
}

function getAllMarkdownFiles(): { filePath: string; folder: string }[] {
  const results: { filePath: string; folder: string }[] = [];

  if (!fs.existsSync(CONTENT_DIR)) return results;

  const folders = fs.readdirSync(CONTENT_DIR).filter((f) => {
    const fullPath = path.join(CONTENT_DIR, f);
    return fs.statSync(fullPath).isDirectory();
  });

  for (const folder of folders) {
    const folderPath = path.join(CONTENT_DIR, folder);
    const files = fs.readdirSync(folderPath).filter((f) => f.endsWith(".md"));
    for (const file of files) {
      results.push({
        filePath: path.join(folderPath, file),
        folder,
      });
    }
  }

  return results;
}

function parseArticleMeta(
  filePath: string,
  folder: string
): ArticleMeta | null {
  try {
    const fileContent = fs.readFileSync(filePath, "utf-8");
    const { data } = matter(fileContent);

    const category = getCategoryByFolder(folder);
    const slug = data.slug || path.basename(filePath, ".md");

    return {
      title: data.title || slug,
      slug,
      category: category?.slug || data.category || "general-issues",
      folder,
      source: data.source || "",
      series: data.series,
      part: data.part?.toString(),
      rebuttalTo: data.rebuttal_to,
      subcategory: data.subcategory,
      wordCount: data.wordCount || 0,
      readTime: data.readTime || 1,
    };
  } catch {
    return null;
  }
}

export function getArticles(): ArticleMeta[] {
  const files = getAllMarkdownFiles();
  const articles: ArticleMeta[] = [];

  for (const { filePath, folder } of files) {
    const meta = parseArticleMeta(filePath, folder);
    if (meta) articles.push(meta);
  }

  return articles.sort((a, b) => a.title.localeCompare(b.title));
}

export function getArticlesByCategory(categorySlug: string): ArticleMeta[] {
  return getArticles().filter((a) => a.category === categorySlug);
}

export async function getArticle(
  categorySlug: string,
  slug: string
): Promise<Article | null> {
  const category = CATEGORIES.find((c) => c.slug === categorySlug);
  if (!category) return null;

  const folderPath = path.join(CONTENT_DIR, category.folder);
  if (!fs.existsSync(folderPath)) return null;

  const files = fs.readdirSync(folderPath).filter((f) => f.endsWith(".md"));
  const targetFile = files.find(
    (f) => path.basename(f, ".md") === slug
  );

  if (!targetFile) return null;

  const filePath = path.join(folderPath, targetFile);
  const fileContent = fs.readFileSync(filePath, "utf-8");
  const { data, content } = matter(fileContent);

  const processed = await remark()
    .use(remarkGfm)
    .use(remarkHtml, { sanitize: false })
    .process(content);

  const htmlContent = processed.toString();
  const catMeta = getCategoryByFolder(category.folder);

  return {
    title: data.title || slug,
    slug,
    category: catMeta?.slug || data.category || "general-issues",
    folder: category.folder,
    source: data.source || "",
    series: data.series,
    part: data.part?.toString(),
    rebuttalTo: data.rebuttal_to,
    subcategory: data.subcategory,
    wordCount: data.wordCount || 0,
    readTime: data.readTime || 1,
    content,
    htmlContent,
  };
}

export function getCategoriesWithCounts(): CategoryWithCount[] {
  const articles = getArticles();

  return CATEGORIES.map((cat) => ({
    ...cat,
    articleCount: articles.filter((a) => a.category === cat.slug).length,
  })).filter((c) => c.articleCount > 0);
}

export interface SubcategoryCount {
  name: string;
  icon: string;
  count: number;
}

export interface CategoryWithSubs extends CategoryWithCount {
  subcategories: SubcategoryCount[];
}

export function getCategoriesWithSubcategories(): CategoryWithSubs[] {
  const articles = getArticles();
  const cats = getCategoriesWithCounts();

  return cats.map((cat) => {
    const catArticles = articles.filter((a) => a.category === cat.slug);
    const defs = SUBCATEGORIES[cat.slug] || [];
    const subcategories = defs
      .map((sub) => ({
        ...sub,
        count: catArticles.filter((a) => a.subcategory === sub.name).length,
      }))
      .filter((s) => s.count > 0);

    return { ...cat, subcategories };
  });
}

export function getSeriesArticles(
  seriesName: string,
  categorySlug: string
): ArticleMeta[] {
  return getArticlesByCategory(categorySlug)
    .filter((a) => a.series === seriesName)
    .sort((a, b) => {
      const pa = a.part || "";
      const pb = b.part || "";
      return pa.localeCompare(pb, undefined, { numeric: true });
    });
}

export function searchArticles(query: string): ArticleMeta[] {
  if (!query || query.trim().length < 2) return [];
  const q = query.toLowerCase();
  return getArticles().filter(
    (a) =>
      a.title.toLowerCase().includes(q) ||
      (a.series && a.series.toLowerCase().includes(q))
  );
}

export function getTotalStats() {
  const articles = getArticles();
  const totalWords = articles.reduce((sum, a) => sum + a.wordCount, 0);
  const totalReadTime = articles.reduce((sum, a) => sum + a.readTime, 0);
  return {
    totalArticles: articles.length,
    totalWords,
    totalReadTimeHours: Math.round(totalReadTime / 60),
    totalCategories: getCategoriesWithCounts().length,
  };
}
