import Link from "next/link";

import { api } from "@/lib/api";
import { AlgoSectionHeader, CurationChip, DiffBadge, PlatformChip } from "@/components/algorithms/algo-chips";
import { LogicPanel } from "@/components/algorithms/logic-panel";
import { PreSolvePanel } from "@/components/algorithms/pre-solve-panel";
import { ProblemPanel } from "@/components/algorithms/problem-panel";
import { TracePanel } from "@/components/algorithms/trace-panel";

export const dynamic = "force-dynamic";

export default async function AlgorithmDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  let data;
  try {
    data = await api.algorithmDetail(slug);
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Algorithm not found</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
        <Link href="/algorithms">← 전체 회차</Link>
      </main>
    );
  }

  const item = data["algorithms.detail"];

  return (
    <main>
      {/* Header */}
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "40px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <Link
          href="/algorithms"
          className="mono"
          style={{
            color: "var(--fg-3)",
            fontSize: 12,
            textDecoration: "none",
            marginBottom: 20,
            display: "inline-block",
          }}
        >
          ← 전체 회차
        </Link>
        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
            display: "flex",
            gap: 12,
            flexWrap: "wrap",
          }}
        >
          <span>{item.slug}</span>
          {item.today && <span style={{ color: "var(--accent)" }}>● today</span>}
          <span>{item.publishedOn ?? ""}</span>
          <span style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
            <DiffBadge level={item.difficulty} />
            <PlatformChip source={item.source} />
            <CurationChip source={item.source} />
          </span>
        </div>
        <h1
          className="m-h1"
          style={{
            fontSize: 40,
            lineHeight: 1.15,
            letterSpacing: "-0.02em",
            margin: 0,
            fontWeight: 600,
            maxWidth: 900,
          }}
        >
          {item.title}
        </h1>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 20 }}>
          {item.tags.map((tag) => (
            <span key={tag} className="tag">
              #{tag}
            </span>
          ))}
        </div>
        {item.source?.url && (
          <div style={{ marginTop: 16 }}>
            <a
              href={item.source.url}
              target="_blank"
              rel="noreferrer"
              className="mono"
              style={{
                fontSize: 11,
                color: "var(--fg-3)",
                textDecoration: "none",
                display: "inline-flex",
                alignItems: "center",
                gap: 8,
                padding: "6px 10px",
                border: "1px solid var(--line-2)",
                borderRadius: 3,
              }}
            >
              ↗ {item.source.platform} #{item.source.number} · {item.slug}
            </a>
          </div>
        )}
      </header>

      {/* §01 — Problem */}
      <section className="pad-x" style={{ padding: "48px 80px 24px" }}>
        <AlgoSectionHeader idx="01" label="problem" title="문제" />
        <ProblemPanel algoSlug={item.slug} problem={item.problem} source={item.source} />
      </section>

      {/* §02 — Pre-solve */}
      <section className="pad-x" style={{ padding: "32px 80px 24px" }}>
        <AlgoSectionHeader idx="02" label="pre-solve" title="사전 사고" />
        <PreSolvePanel clarifying={item.clarifying} approach={item.approach} />
      </section>

      {/* §03 — 논리 구조 */}
      <section className="pad-x" style={{ padding: "24px 80px 24px" }}>
        <AlgoSectionHeader idx="03" label="logic" title="논리 구조" />
        <LogicPanel logic={item.logic} />
      </section>

      {/* §04 — Solve · Trace */}
      <section className="pad-x" style={{ padding: "24px 80px 32px" }}>
        <AlgoSectionHeader idx="04" label="solve" title="문제풀이 · 트레이스" />
        <TracePanel trace={item.trace} solution={item.solution} />
      </section>

      {/* Prev / Next */}
      <nav
        className="pad-x m-stack"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 16,
          padding: "32px 80px 64px",
          borderTop: "1px solid var(--line-1)",
        }}
      >
        {item.newer ? (
          <Link
            href={`/algorithms/${item.newer.slug}`}
            className="card"
            style={{
              padding: "20px 24px",
              textAlign: "left",
              background: "var(--bg-1)",
              border: "1px solid var(--line-1)",
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}>
              ← 다음 회차
            </div>
            <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{item.newer.title}</div>
          </Link>
        ) : (
          <div />
        )}
        {item.older ? (
          <Link
            href={`/algorithms/${item.older.slug}`}
            className="card"
            style={{
              padding: "20px 24px",
              textAlign: "right",
              background: "var(--bg-1)",
              border: "1px solid var(--line-1)",
              textDecoration: "none",
              color: "inherit",
            }}
          >
            <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}>
              이전 회차 →
            </div>
            <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{item.older.title}</div>
          </Link>
        ) : (
          <div />
        )}
      </nav>
    </main>
  );
}
