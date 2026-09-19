// Generates public/search-index.json for client-side search (MiniSearch).
// Run manually before `next dev`/`next build`:
//   node scripts/generate-search-index.mjs
// Also wired as the "prebuild" npm lifecycle hook in package.json for when
// a full npm toolchain is available.
//
// NOTE: this is plain JS (not importing lib/categories.ts) because this
// sandbox's Node build has no TypeScript-stripping support. The folder/slug
// mapping below must stay in sync with lib/categories.ts's CATEGORIES array.

import fs from "fs";
import path from "path";
import matter from "gray-matter";

const CATEGORIES = [
  { slug: "answers-to-common-questions", folder: "01-answers-to-common-questions", title: "Answers to Common Questions" },
  { slug: "christological-issues", folder: "02-christological-issues", title: "Christological Issues" },
  { slug: "theological-issues", folder: "03-theological-issues", title: "Theological Issues" },
  { slug: "biblical-issues", folder: "04-biblical-issues", title: "Biblical Issues" },
  { slug: "quranic-issues", folder: "05-quranic-issues", title: "Quranic Issues" },
  { slug: "analysis-of-muhammad", folder: "06-analysis-of-muhammad", title: "Analysis of Muhammad" },
  { slug: "hadith-analysis", folder: "07-hadith-analysis", title: "Hadith Analysis" },
  { slug: "polemical-issues", folder: "08-polemical-issues", title: "Polemical Issues" },
  { slug: "general-issues", folder: "09-general-issues", title: "General Issues" },
  { slug: "responses-to-authors", folder: "10-responses-to-authors", title: "Responses to Muslim Authors" },
  { slug: "turning-the-tables", folder: "11-turning-the-tables", title: "Turning the Tables" },
  { slug: "short-summaries", folder: "12-short-summaries", title: "Short Summaries" },
  { slug: "blog-posts", folder: "13-blog-posts", title: "Blog Posts" },
];

const CONTENT_DIR = path.join(process.cwd(), "..", "content");
const OUT_FILE = path.join(process.cwd(), "public", "search-index.json");

function getCategoryByFolder(folder) {
  return CATEGORIES.find((c) => c.folder === folder);
}

function getCategoryBySlug(slug) {
  return CATEGORIES.find((c) => c.slug === slug);
}

function stripMarkdown(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[.*?\]\(.*?\)/g, " ")
    .replace(/\[(.*?)\]\(.*?\)/g, "$1")
    .replace(/[#>*_`~]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function excerptOf(markdown, maxLength = 220) {
  const plain = stripMarkdown(markdown);
  if (plain.length <= maxLength) return plain;
  const truncated = plain.slice(0, maxLength);
  const lastSpace = truncated.lastIndexOf(" ");
  return `${truncated.slice(0, lastSpace > 0 ? lastSpace : maxLength)}…`;
}

function main() {
  if (!fs.existsSync(CONTENT_DIR)) {
    console.warn(`Content dir not found at ${CONTENT_DIR}, writing empty index.`);
    fs.writeFileSync(OUT_FILE, "[]");
    return;
  }

  const folders = fs
    .readdirSync(CONTENT_DIR)
    .filter((f) => fs.statSync(path.join(CONTENT_DIR, f)).isDirectory());

  const docs = [];

  for (const folder of folders) {
    const folderPath = path.join(CONTENT_DIR, folder);
    const files = fs.readdirSync(folderPath).filter((f) => f.endsWith(".md"));

    for (const file of files) {
      const filePath = path.join(folderPath, file);
      try {
        const fileContent = fs.readFileSync(filePath, "utf-8");
        const { data, content } = matter(fileContent);

        const category = getCategoryByFolder(folder);
        const categorySlug = category?.slug || data.category || "general-issues";
        const slug = data.slug || path.basename(file, ".md");

        docs.push({
          id: `${categorySlug}/${slug}`,
          title: data.title || slug,
          slug,
          category: categorySlug,
          categoryLabel: getCategoryBySlug(categorySlug)?.title || categorySlug,
          subcategory: data.subcategory,
          series: data.series,
          part: data.part?.toString(),
          readTime: data.readTime || 1,
          excerpt: excerptOf(content),
        });
      } catch (err) {
        console.warn(`Skipping unparseable article: ${filePath}`, err.message);
      }
    }
  }

  fs.mkdirSync(path.dirname(OUT_FILE), { recursive: true });
  fs.writeFileSync(OUT_FILE, JSON.stringify(docs));
  console.log(`Wrote ${docs.length} documents to ${path.relative(process.cwd(), OUT_FILE)}`);
}

main();
