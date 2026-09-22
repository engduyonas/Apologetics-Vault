import fs from "fs";
import path from "path";
import matter from "gray-matter";
import { remark } from "remark";
import remarkGfm from "remark-gfm";
import remarkHtml from "remark-html";
import {
  TRADITIONS,
  CATEGORIES,
  SUBCATEGORIES,
  getCategoryByFolder,
  getCategoryBySlug,
  getTraditionBySlug,
  type Tradition,
  type Category,
} from "./categories";

const CONTENT_DIR = path.join(process.cwd(), "..", "content");

export interface ArticleMeta {
  title: string;
  slug: string;
  tradition: string;
  category: string;
  folder: string;
  source: string;
  author: string;
  sourceName: string;
  license?: string;
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

export interface CategoryWithCount extends Category {
  articleCount: number;
}

export interface TraditionWithCount extends Tradition {
  articleCount: number;
  categoryCount: number;
}

function getAllMarkdownFiles(): { filePath: string; tradition: string; folder: string }[] {
  const results: { filePath: string; tradition: string; folder: string }[] = [];

  if (!fs.existsSync(CONTENT_DIR)) return results;

  const traditionDirs = fs.readdirSync(CONTENT_DIR).filter((t) => {
    const fullPath = path.join(CONTENT_DIR, t);
    return fs.statSync(fullPath).isDirectory();
  });

  for (const tradition of traditionDirs) {
    const traditionPath = path.join(CONTENT_DIR, tradition);
    const folders = fs.readdirSync(traditionPath).filter((f) => {
      const fullPath = path.join(traditionPath, f);
      return fs.statSync(fullPath).isDirectory();
    });

    for (const folder of folders) {
      const folderPath = path.join(traditionPath, folder);
      const files = fs.readdirSync(folderPath).filter((f) => f.endsWith(".md"));
      for (const file of files) {
        results.push({
          filePath: path.join(folderPath, file),
          tradition,
          folder,
        });
      }
    }
  }

  return results;
}

function parseArticleMeta(
  filePath: string,
  tradition: string,
  folder: string
): ArticleMeta | null {
  try {
    const fileContent = fs.readFileSync(filePath, "utf-8");
    const { data } = matter(fileContent);

    const category = getCategoryByFolder(tradition, folder);
    const slug = data.slug || path.basename(filePath, ".md");

    return {
      title: data.title || slug,
      slug,
      tradition: data.tradition || tradition,
      category: category?.slug || data.category || "why-christianity",
      folder,
      source: data.source || "",
      author: data.author || "",
      sourceName: data.sourceName || "",
      license: data.license,
      series: data.series,
      part: data.part?.toString(),
      rebuttalTo: data.rebuttal_to,
      subcategory: data.subcategory,
      wordCount: data.wordCount || 0,
      readTime: data.readTime || 1,
    };
  } catch (err) {
    console.warn(`Skipping unparseable article frontmatter: ${filePath}`, err);
    return null;
  }
}

export function getArticles(tradition?: string): ArticleMeta[] {
  const files = getAllMarkdownFiles();
  const articles: ArticleMeta[] = [];

  for (const { filePath, tradition: t, folder } of files) {
    if (tradition && t !== tradition) continue;
    const meta = parseArticleMeta(filePath, t, folder);
    if (meta) articles.push(meta);
  }

  return articles.sort((a, b) => a.title.localeCompare(b.title));
}

export function getArticlesByCategory(
  tradition: string,
  categorySlug: string
): ArticleMeta[] {
  return getArticles(tradition).filter((a) => a.category === categorySlug);
}

export async function getArticle(
  tradition: string,
  categorySlug: string,
  slug: string
): Promise<Article | null> {
  const category = getCategoryBySlug(tradition, categorySlug);
  if (!category) return null;

  const folderPath = path.join(CONTENT_DIR, tradition, category.folder);
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
  const catMeta = getCategoryByFolder(tradition, category.folder);

  return {
    title: data.title || slug,
    slug,
    tradition: data.tradition || tradition,
    category: catMeta?.slug || data.category || "why-christianity",
    folder: category.folder,
    source: data.source || "",
    author: data.author || "",
    sourceName: data.sourceName || "",
    license: data.license,
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

export function getCategoriesWithCounts(tradition: string): CategoryWithCount[] {
  const articles = getArticles(tradition);

  return (CATEGORIES[tradition] ?? [])
    .map((cat) => ({
      ...cat,
      articleCount: articles.filter((a) => a.category === cat.slug).length,
    }))
    .filter((c) => c.articleCount > 0);
}

export function getAllCategoriesWithCounts(): Record<string, CategoryWithCount[]> {
  const result: Record<string, CategoryWithCount[]> = {};
  for (const t of TRADITIONS) {
    result[t.slug] = getCategoriesWithCounts(t.slug);
  }
  return result;
}

export function getTraditionsWithCounts(): TraditionWithCount[] {
  return TRADITIONS.map((t) => {
    const categories = getCategoriesWithCounts(t.slug);
    return {
      ...t,
      articleCount: categories.reduce((sum, c) => sum + c.articleCount, 0),
      categoryCount: categories.length,
    };
  }).filter((t) => t.articleCount > 0);
}

export interface SubcategoryCount {
  name: string;
  icon: string;
  count: number;
}

export interface CategoryWithSubs extends CategoryWithCount {
  subcategories: SubcategoryCount[];
}

export function getCategoriesWithSubcategories(tradition: string): CategoryWithSubs[] {
  const articles = getArticles(tradition);
  const cats = getCategoriesWithCounts(tradition);
  const traditionSubs = SUBCATEGORIES[tradition] ?? {};

  return cats.map((cat) => {
    const catArticles = articles.filter((a) => a.category === cat.slug);
    const defs = traditionSubs[cat.slug] || [];
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
  tradition: string,
  categorySlug: string,
  seriesName: string
): ArticleMeta[] {
  return getArticlesByCategory(tradition, categorySlug)
    .filter((a) => a.series === seriesName)
    .sort((a, b) => {
      const pa = a.part || "";
      const pb = b.part || "";
      return pa.localeCompare(pb, undefined, { numeric: true });
    });
}

export function getRelatedArticles(
  article: ArticleMeta,
  limit = 5
): ArticleMeta[] {
  const categoryArticles = getArticlesByCategory(
    article.tradition,
    article.category
  ).filter((a) => a.slug !== article.slug);

  const sameSubcategory = article.subcategory
    ? categoryArticles.filter((a) => a.subcategory === article.subcategory)
    : [];
  const sameSeries = article.series
    ? categoryArticles.filter(
        (a) => a.series === article.series && !sameSubcategory.includes(a)
      )
    : [];
  const rest = categoryArticles.filter(
    (a) => !sameSubcategory.includes(a) && !sameSeries.includes(a)
  );

  return [...sameSubcategory, ...sameSeries, ...rest].slice(0, limit);
}

export interface SearchDoc {
  id: string;
  title: string;
  slug: string;
  tradition: string;
  traditionLabel: string;
  category: string;
  categoryLabel: string;
  subcategory?: string;
  series?: string;
  part?: string;
  readTime: number;
  excerpt: string;
}

function stripMarkdown(markdown: string): string {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[.*?\]\(.*?\)/g, " ")
    .replace(/\[(.*?)\]\(.*?\)/g, "$1")
    .replace(/[#>*_`~]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function excerptOf(markdown: string, maxLength = 220): string {
  const plain = stripMarkdown(markdown);
  if (plain.length <= maxLength) return plain;
  const truncated = plain.slice(0, maxLength);
  const lastSpace = truncated.lastIndexOf(" ");
  return `${truncated.slice(0, lastSpace > 0 ? lastSpace : maxLength)}…`;
}

export function getSearchIndex(): SearchDoc[] {
  const files = getAllMarkdownFiles();
  const docs: SearchDoc[] = [];

  for (const { filePath, tradition, folder } of files) {
    try {
      const fileContent = fs.readFileSync(filePath, "utf-8");
      const { data, content } = matter(fileContent);

      const traditionSlug = data.tradition || tradition;
      const category = getCategoryByFolder(traditionSlug, folder);
      const categorySlug = category?.slug || data.category || "why-christianity";
      const slug = data.slug || path.basename(filePath, ".md");

      docs.push({
        id: `${traditionSlug}/${categorySlug}/${slug}`,
        title: data.title || slug,
        slug,
        tradition: traditionSlug,
        traditionLabel: getTraditionBySlug(traditionSlug)?.title || traditionSlug,
        category: categorySlug,
        categoryLabel: getCategoryBySlug(traditionSlug, categorySlug)?.title || categorySlug,
        subcategory: data.subcategory,
        series: data.series,
        part: data.part?.toString(),
        readTime: data.readTime || 1,
        excerpt: excerptOf(content),
      });
    } catch (err) {
      console.warn(`Skipping unparseable article in search index: ${filePath}`, err);
    }
  }

  return docs;
}

export function getTotalStats(tradition?: string) {
  const articles = getArticles(tradition);
  const totalWords = articles.reduce((sum, a) => sum + a.wordCount, 0);
  const totalReadTime = articles.reduce((sum, a) => sum + a.readTime, 0);
  return {
    totalArticles: articles.length,
    totalWords,
    totalReadTimeHours: Math.round(totalReadTime / 60),
    totalCategories: tradition
      ? getCategoriesWithCounts(tradition).length
      : getTraditionsWithCounts().reduce((sum, t) => sum + t.categoryCount, 0),
  };
}
