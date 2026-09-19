"use client";

import { useState } from "react";
import Link from "next/link";
import { PanelLeftClose, PanelLeftOpen, Bookmark } from "lucide-react";
import Sidebar from "./Sidebar";
import MobileNav from "./MobileNav";
import SearchBar from "./SearchBar";
import ThemeToggle from "./ThemeToggle";

interface SidebarCategory {
  slug: string;
  title: string;
  icon: string;
  articleCount: number;
}

export default function DesktopShell({
  categories,
  children,
}: {
  categories: SidebarCategory[];
  children: React.ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="flex h-full">
      {/* Desktop sidebar */}
      <aside
        className={`hidden md:flex shrink-0 border-r border-cream-300 dark:border-warm-700 bg-cream-50 dark:bg-warm-900 flex-col fixed inset-y-0 left-0 z-30 transition-[width] duration-200 ${
          collapsed ? "w-0 overflow-hidden border-r-0" : "w-72"
        }`}
      >
        <Sidebar
          categories={categories}
          collapseButton={
            <button
              onClick={() => setCollapsed(true)}
              className="p-1.5 rounded-lg hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors"
              aria-label="Hide sidebar"
            >
              <PanelLeftClose className="w-4 h-4 text-warm-400 dark:text-warm-500" />
            </button>
          }
        />
      </aside>

      {/* Main area */}
      <div
        className={`flex-1 flex flex-col min-h-screen transition-[margin] duration-200 ${
          collapsed ? "md:ml-0" : "md:ml-72"
        }`}
      >
        {/* Top bar */}
        <header className="sticky top-0 z-20 border-b border-cream-300 dark:border-warm-700 bg-cream-100/80 dark:bg-warm-900/80 backdrop-blur-md">
          <div className="flex items-center px-6 py-3 w-full gap-4">
            <MobileNav categories={categories} />
            {collapsed && (
              <button
                onClick={() => setCollapsed(false)}
                className="hidden md:flex p-2 rounded-lg hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors shrink-0"
                aria-label="Show sidebar"
              >
                <PanelLeftOpen className="w-5 h-5 text-warm-500 dark:text-warm-400" />
              </button>
            )}
            <div className="flex-1 flex justify-center">
              <SearchBar />
            </div>
            <Link
              href="/reading-list"
              className="p-2 rounded-lg hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors"
              aria-label="Reading list"
              title="Reading list"
            >
              <Bookmark className="w-5 h-5 text-warm-500 dark:text-warm-400" />
            </Link>
            <ThemeToggle />
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}
