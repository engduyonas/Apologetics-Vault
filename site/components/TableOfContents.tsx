"use client";

import { useEffect, useState } from "react";

interface TOCItem {
  id: string;
  text: string;
  level: number;
}

export default function TableOfContents({
  htmlContent,
}: {
  htmlContent: string;
}) {
  const [items, setItems] = useState<TOCItem[]>([]);
  const [activeId, setActiveId] = useState("");

  useEffect(() => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlContent, "text/html");
    const headings = doc.querySelectorAll("h2, h3");
    const tocItems: TOCItem[] = [];

    headings.forEach((h, i) => {
      const text = h.textContent?.trim() || "";
      if (text.length > 0) {
        const id = `heading-${i}`;
        tocItems.push({ id, text, level: parseInt(h.tagName[1]) });
      }
    });

    setItems(tocItems);
  }, [htmlContent]);

  useEffect(() => {
    if (items.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -60% 0px" }
    );

    items.forEach(({ id }) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [items]);

  if (items.length < 3) return null;

  return (
    <nav className="hidden xl:block sticky top-20 w-56 shrink-0 max-h-[calc(100vh-6rem)] overflow-y-auto text-sm font-sans">
      <h4 className="font-semibold text-warm-700 dark:text-cream-200 mb-3 text-xs uppercase tracking-wider">
        On This Page
      </h4>
      <ul className="space-y-1.5 border-l border-cream-300 dark:border-warm-700">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#${item.id}`}
              onClick={(e) => {
                e.preventDefault();
                document
                  .getElementById(item.id)
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
              className={`block py-0.5 pl-3 -ml-px transition-colors leading-snug ${
                item.level === 3 ? "pl-6" : ""
              } ${
                activeId === item.id
                  ? "text-slate-700 dark:text-slate-400 font-medium border-l-2 border-slate-500 dark:border-slate-400"
                  : "text-warm-400 dark:text-warm-500 hover:text-warm-700 dark:hover:text-cream-300 border-l-2 border-transparent"
              }`}
            >
              {item.text.length > 50
                ? item.text.substring(0, 50) + "..."
                : item.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
