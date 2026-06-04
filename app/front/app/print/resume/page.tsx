/**
 * /print/resume — P1.2 — KO+EN 합본 (API 데이터, 두 Pager 연속 렌더).
 * 1) /api/print/resume fetch
 * 2) KO Pager (atoms: about, career[]) + EN Pager (atoms: about, career[])
 * 3) playwright 가 모든 sheet 캡처 → 한 PDF 안에 KO + EN 모두
 */

import "../print.css";
import { PrintResume } from "@/components/print/resume";
import type { PrintResumeResponse } from "@/lib/print-types";

export const dynamic = "force-dynamic";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

async function fetchResume(): Promise<PrintResumeResponse> {
  const res = await fetch(`${API_BASE}/api/print/resume`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`API ${res.status}: /api/print/resume`);
  }
  return (await res.json()) as PrintResumeResponse;
}

export default async function PrintResumePage() {
  const data = await fetchResume();
  return (
    <div className="print-root">
      <div className="desk">
        <PrintResume data={data} />
      </div>
    </div>
  );
}
