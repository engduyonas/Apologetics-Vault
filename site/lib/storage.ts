const BOOKMARKS_KEY = "av:bookmarks:v1";
const READ_KEY = "av:read:v1";

export interface BookmarkEntry {
  slug: string;
  category: string;
  title: string;
  categoryLabel: string;
  readTime: number;
  subcategory?: string;
  series?: string;
  part?: string;
  bookmarkedAt: number;
}

function readJSON<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeJSON(key: string, value: unknown) {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    // localStorage unavailable (private browsing, quota, etc.) — ignore
  }
}

export function articleKey(category: string, slug: string) {
  return `${category}/${slug}`;
}

export function getBookmarks(): BookmarkEntry[] {
  return readJSON<BookmarkEntry[]>(BOOKMARKS_KEY, []);
}

export function setBookmarks(entries: BookmarkEntry[]) {
  writeJSON(BOOKMARKS_KEY, entries);
}

export function getReadMap(): Record<string, number> {
  return readJSON<Record<string, number>>(READ_KEY, {});
}

export function setReadMap(map: Record<string, number>) {
  writeJSON(READ_KEY, map);
}
