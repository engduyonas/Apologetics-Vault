import type { Metadata } from "next";
import { Inter, Merriweather } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";
import DesktopShell from "@/components/DesktopShell";
import { getAllCategoriesWithCounts } from "@/lib/content";
import { TRADITIONS } from "@/lib/categories";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const merriweather = Merriweather({
  subsets: ["latin"],
  weight: ["300", "400", "700"],
  variable: "--font-serif",
});

export const metadata: Metadata = {
  title: "Apologetics Vault",
  description:
    "A personal study library for knowing the Christian faith more deeply, and being able to explain and defend it fluently.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const categoriesByTradition = Object.fromEntries(
    Object.entries(getAllCategoriesWithCounts()).map(([tradition, cats]) => [
      tradition,
      cats.map((c) => ({
        slug: c.slug,
        title: c.title,
        icon: c.icon,
        articleCount: c.articleCount,
      })),
    ])
  );
  const traditions = TRADITIONS.map((t) => ({
    slug: t.slug,
    title: t.title,
    icon: t.icon,
  }));

  return (
    <html lang="en" className={`${inter.variable} ${merriweather.variable} h-full`} suppressHydrationWarning>
      <body className="h-full font-sans">
        <Providers>
          <DesktopShell traditions={traditions} categoriesByTradition={categoriesByTradition}>
            {children}
          </DesktopShell>
        </Providers>
      </body>
    </html>
  );
}
