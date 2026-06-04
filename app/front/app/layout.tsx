import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Suspense } from "react";
import { TopNav } from "@/components/shell/topnav";
import { PageFooter } from "@/components/shell/footer";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-next-sans",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-next-mono",
});

export const metadata: Metadata = {
  title: "kknaks.dev",
  description: "이건학(kknaks) — Backend Engineer @ AI startup",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko" className={`${inter.variable} ${mono.variable}`}>
      <body>
        <Suspense fallback={null}>
          <TopNav />
        </Suspense>
        {children}
        <Suspense fallback={null}>
          <PageFooter />
        </Suspense>
      </body>
    </html>
  );
}
