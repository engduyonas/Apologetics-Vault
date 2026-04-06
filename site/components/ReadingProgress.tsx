"use client";

import { useEffect, useState } from "react";

export default function ReadingProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    function handleScroll() {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (docHeight > 0) {
        setProgress((window.scrollY / docHeight) * 100);
      }
    }

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="fixed top-0 left-0 right-0 z-50 h-0.5 bg-cream-200 dark:bg-warm-800">
      <div
        className="h-full bg-slate-500 dark:bg-slate-400 transition-[width] duration-150"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
