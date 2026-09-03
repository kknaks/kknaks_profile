"use client";

import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { AnswerResult, RowValue, UsedEdge } from "@/lib/ontology/types";
import { formatCount, verdictStroke } from "@/lib/ontology/encoding";
import { serializeFilters } from "@/lib/ontology/client";
import { LayerBadge, SectionLabel } from "../primitives";

/**
 * 답변 6블록 — 순서 고정, 출처는 SPEC-005 §4 답변 객체다(SPEC-004 U-10).
 * **없는 필드의 블록은 만들지 않는다** — 빈 상자를 그리지 않는다(AC-13).
 *
 * 1 상태 배지 · 2 본문 · 3 근거(citations) · 4 used_edges 칩 ·
 * 5 드릴다운 표(최대 5행 + 「5 / N」) · 6 후속 질문 칩
 */
export function AnswerBlocks({
  result,
  nodeLabels,
  onFollowup,
}: {
  result: AnswerResult;
  nodeLabels: Record<string, string>;
  onFollowup: (question: string) => void;
}) {
  const badges: { label: string; fill: string; color: string }[] = [];
  if (result.premise_correction?.corrected) {
    badges.push({ label: "전제 교정", fill: "var(--ont-watch-fill)", color: "var(--ont-watch-text)" });
  }
  if (result.unknowns && result.unknowns.length > 0) {
    badges.push({ label: "답할 수 없음 · 미관측", fill: "var(--ont-hover)", color: "var(--ont-label)" });
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14, minWidth: 0 }}>
      {badges.length > 0 && (
        <div style={{ display: "flex", gap: 6 }}>
          {badges.map((badge) => (
            <span
              key={badge.label}
              style={{
                height: 24,
                display: "inline-flex",
                alignItems: "center",
                padding: "0 9px",
                borderRadius: 6,
                background: badge.fill,
                color: badge.color,
                fontSize: 12,
                fontWeight: 600,
              }}
            >
              {badge.label}
            </span>
          ))}
        </div>
      )}

      <div style={{ fontSize: 14, lineHeight: 1.75, color: "var(--ont-ink)" }}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.answer}</ReactMarkdown>
      </div>

      {result.citations.length > 0 && (
        <div
          style={{
            background: "var(--ont-canvas)",
            borderRadius: 8,
            border: "1px solid var(--ont-border)",
            padding: "10px 12px",
            display: "flex",
            flexDirection: "column",
            gap: 6,
          }}
        >
          <SectionLabel>근거</SectionLabel>
          <div
            className="ont-mono"
            style={{ fontSize: 12, lineHeight: 1.7, color: "var(--ont-ink)", whiteSpace: "pre-line" }}
          >
            {result.citations
              .map(
                (citation) =>
                  `${citation.source.table}.${citation.source.column} · ${citation.grain} · ` +
                  `${citation.period.start} ~ ${citation.period.end} · ${formatCount(citation.row_count)}행 — ${citation.claim}`,
              )
              .join("\n")}
          </div>
        </div>
      )}

      <UsedEdgeChips edges={result.used_edges} nodeLabels={nodeLabels} />

      {result.drilldown && result.drilldown.columns.length > 0 && (
        <DrilldownTable drilldown={result.drilldown} />
      )}

      {result.followups && result.followups.length > 0 && (
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {result.followups.map((followup) => (
            <button
              key={followup}
              type="button"
              onClick={() => onFollowup(followup)}
              style={{
                height: 30,
                padding: "0 12px",
                borderRadius: 8,
                border: "1px solid var(--ont-border-card)",
                background: "var(--ont-surface)",
                color: "var(--ont-body)",
                fontSize: 13,
              }}
            >
              {followup}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/**
 * `used_edges` 칩 — 하이라이트의 유일한 표시다. 칩을 누르면 모니터링 그래프로 점프해
 * 그 엣지가 선택된 채로 열린다. **채팅에는 그래프 패널이 없다**(U-11 · AC-14).
 * 칩 문구는 **노드 라벨**이고 id 를 노출하지 않는다.
 */
function UsedEdgeChips({
  edges,
  nodeLabels,
}: {
  edges: UsedEdge[];
  nodeLabels: Record<string, string>;
}) {
  if (edges.length === 0) {
    return (
      <p style={{ margin: 0, fontSize: 13, color: "var(--ont-muted)" }}>
        이 답변은 엣지를 밟지 않았습니다.
      </p>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      <SectionLabel>밟은 엣지 · used_edges {edges.length}</SectionLabel>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {edges.map((edge) => {
          const stroke = verdictStroke(edge.verdict);
          return (
            <Link
              key={edge.edge_id}
              href={`/ontology/monitoring?edge=${encodeURIComponent(edge.edge_id)}`}
              title={edge.role}
              style={{
                height: 26,
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                padding: "0 10px",
                borderRadius: 6,
                background: "var(--ont-surface)",
                border: `1px ${stroke.dash ? "dashed" : "solid"} ${stroke.color}`,
                color: stroke.color === "#1E1E1E" ? "var(--ont-ink)" : stroke.color,
                fontSize: 12,
                fontWeight: 600,
              }}
            >
              {nodeLabels[edge.from] ?? edge.from}
              <span aria-hidden>→</span>
              {nodeLabels[edge.to] ?? edge.to}
            </Link>
          );
        })}
      </div>
      <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>
        칩을 누르면 모니터링 그래프에서 그 엣지가 선택된 채로 열립니다.
      </span>
    </div>
  );
}

const DRILLDOWN_ROW_CAP = 5;

/** 인라인 드릴다운 표 — 최대 5행 + 「5 / N」. 소리 없는 절단 금지(AC-16). */
function DrilldownTable({ drilldown }: { drilldown: NonNullable<AnswerResult["drilldown"]> }) {
  const rows = drilldown.rows.slice(0, DRILLDOWN_ROW_CAP);
  const filters = serializeFilters(drilldown.filters);
  const params = new URLSearchParams({ tier: drilldown.layer, table: drilldown.table });
  if (filters) params.set("filters", filters);

  return (
    <div
      style={{
        maxWidth: 960,
        borderRadius: 8,
        border: "1px solid var(--ont-border)",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          height: 32,
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "0 12px",
          background: "var(--ont-bronze-fill)",
          borderBottom: `1px solid var(--ont-bronze-border)`,
        }}
      >
        <LayerBadge layer={drilldown.layer} size="sm" />
        <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-bronze-text)" }}>
          {drilldown.view}
        </span>
        {drilldown.total > DRILLDOWN_ROW_CAP && (
          <span className="ont-mono" style={{ marginLeft: "auto", fontSize: 12, color: "var(--ont-muted)" }}>
            {rows.length} / {formatCount(drilldown.total)}
          </span>
        )}
      </div>

      <div style={{ overflowX: "auto" }}>
        <table style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              {drilldown.columns.map((column) => (
                <th
                  key={column}
                  className="ont-mono"
                  style={{
                    height: 32,
                    padding: "0 10px",
                    textAlign: "left",
                    whiteSpace: "nowrap",
                    background: "var(--ont-canvas)",
                    borderBottom: "1px solid var(--ont-border)",
                    fontSize: 12,
                    fontWeight: 600,
                    color: "var(--ont-body)",
                  }}
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={index}>
                {drilldown.columns.map((column) => (
                  <td
                    key={column}
                    className="ont-mono"
                    style={{
                      height: 36,
                      padding: "0 10px",
                      borderBottom: "1px solid var(--ont-row-divider)",
                      fontSize: 12,
                      whiteSpace: "nowrap",
                      textAlign: typeof row[column] === "number" ? "right" : "left",
                      color: drilldown.masked_fields.includes(column)
                        ? "var(--ont-label)"
                        : "var(--ont-ink)",
                    }}
                  >
                    {renderCell(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ padding: "8px 12px", borderTop: "1px solid var(--ont-border)" }}>
        <Link
          href={`/ontology/data?${params.toString()}`}
          style={{ fontSize: 12, color: "var(--ont-primary-deep)", textDecoration: "underline" }}
        >
          전체 보기
        </Link>
      </div>
    </div>
  );
}

function renderCell(value: RowValue): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "number") return formatCount(value);
  return String(value);
}
