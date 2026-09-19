const BOOKMARKS_KEY = "av:bookmarks:v1";
const READ_KEY = "av:read:v1";

export interface BookmarkEntry {
  slug: string;
  tradition: string;
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

export function articleKey(tradition: string, category: string, slug: string) {
  return `${tradition}/${category}/${slug}`;
}

// Pre-multi-tradition data had no `tradition` field / used 2-part keys.
// Everything scraped before this migration was Islam content, so backfill it.
const LEGACY_TRADITION = "islam";

export function getBookmarks(): BookmarkEntry[] {
  const raw = readJSON<(BookmarkEntry & { tradition?: string })[]>(BOOKMARKS_KEY, []);
  let migrated = false;
  const result = raw.map((b) => {
    if (b.tradition) return b as BookmarkEntry;
    migrated = true;
    return { ...b, tradition: LEGACY_TRADITION };
  });
  if (migrated) setBookmarks(result);
  return result;
}

export function setBookmarks(entries: BookmarkEntry[]) {
  writeJSON(BOOKMARKS_KEY, entries);
}

export function getReadMap(): Record<string, number> {
  const raw = readJSON<Record<string, number>>(READ_KEY, {});
  let migrated = false;
  const result: Record<string, number> = {};
  for (const [key, value] of Object.entries(raw)) {
    if (key.split("/").length === 2) {
      migrated = true;
      result[`${LEGACY_TRADITION}/${key}`] = value;
    } else {
      result[key] = value;
    }
  }
  if (migrated) setReadMap(result);
  return result;
}

export function setReadMap(map: Record<string, number>) {
  writeJSON(READ_KEY, map);
}
