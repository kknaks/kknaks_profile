/**
 * /print/portfolio — A4 landscape, KO+EN 합본.
 * cover + visible 프로젝트들의 케이스 스터디 (problem/approach/impact/learnings/troubles).
 */

import "../print.css";
import { PrintPortfolio } from "@/components/print/portfolio";
import type { PrintPortfolioResponse } from "@/lib/print-types";

export const dynamic = "force-dynamic";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

async function fetchPortfolio(): Promise<PrintPortfolioResponse> {
  const res = await fetch(`${API_BASE}/api/print/portfolio`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API ${res.status}: /api/print/portfolio`);
  }
  return (await res.json()) as PrintPortfolioResponse;
}

export default async function PrintPortfolioPage() {
  const data = await fetchPortfolio();
  return (
    <div className="print-root">
      <div className="desk">
        <PrintPortfolio data={data} />
      </div>
    </div>
  );
}
