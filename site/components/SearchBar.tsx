"use client";

import { Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState, useEffect, useRef } from "react";

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative w-full max-w-md">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-warm-400" />
      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search articles... (Ctrl+K)"
        className="w-full pl-10 pr-4 py-2 rounded-lg border border-cream-300 dark:border-warm-600 bg-cream-50 dark:bg-warm-800 text-warm-800 dark:text-cream-200 placeholder-warm-400 dark:placeholder-warm-500 focus:outline-none focus:ring-2 focus:ring-slate-500/50 dark:focus:ring-slate-600/40 text-sm"
      />
    </form>
  );
}
