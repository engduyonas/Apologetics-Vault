"use client";

import { Menu, X } from "lucide-react";
import { useState } from "react";
import Sidebar from "./Sidebar";

interface SidebarCategory {
  slug: string;
  title: string;
  icon: string;
  articleCount: number;
}

interface SidebarTradition {
  slug: string;
  title: string;
  icon: string;
}

export default function MobileNav({
  traditions,
  categoriesByTradition,
}: {
  traditions: SidebarTradition[];
  categoriesByTradition: Record<string, SidebarCategory[]>;
}) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="md:hidden p-2 rounded-lg hover:bg-cream-200 dark:hover:bg-warm-800 transition-colors"
        aria-label="Open menu"
      >
        <Menu className="w-5 h-5 text-warm-600 dark:text-warm-300" />
      </button>

      {open && (
        <>
          <div
            className="fixed inset-0 z-40 bg-warm-900/40 backdrop-blur-sm md:hidden"
            onClick={() => setOpen(false)}
          />
          <div className="fixed inset-y-0 left-0 z-50 w-72 bg-cream-50 dark:bg-warm-900 shadow-xl md:hidden">
            <button
              onClick={() => setOpen(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg hover:bg-cream-200 dark:hover:bg-warm-800"
              aria-label="Close menu"
            >
              <X className="w-5 h-5 text-warm-500" />
            </button>
            <Sidebar
              traditions={traditions}
              categoriesByTradition={categoriesByTradition}
              onNavigate={() => setOpen(false)}
            />
          </div>
        </>
      )}
    </>
  );
}
