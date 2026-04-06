import type { Metadata } from "next";
import { Inter, Merriweather } from "next/font/google";
import "./globals.css";
import Providers from "@/components/Providers";
import DesktopShell from "@/components/DesktopShell";
import { getCategoriesWithCounts } from "@/lib/content";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const merriweather = Merriweather({
  subsets: ["latin"],
  weight: ["300", "400", "700"],
  variable: "--font-serif",
});

export const metadata: Metadata = {
  title: "Apologetics Vault",
  description:
    "A curated library of Christian apologetics — theology, Christology, and comparative religion.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const categories = getCategoriesWithCounts().map((c) => ({
    slug: c.slug,
    title: c.title,
    icon: c.icon,
    articleCount: c.articleCount,
  }));

  return (
    <html lang="en" className={`${inter.variable} ${merriweather.variable} h-full`} suppressHydrationWarning>
      <body className="h-full font-sans">
        <Providers>
          <DesktopShell categories={categories}>
            {children}
          </DesktopShell>
        </Providers>
      </body>
    </html>
  );
}
