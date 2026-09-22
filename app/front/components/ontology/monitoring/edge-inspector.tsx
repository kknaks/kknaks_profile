"use client";

import Link from "next/link";
import type { GraphEdge, GraphNode } from "@/lib/ontology/types";
import {
  dataHref,
  hasDirection,
  directionGlyph,
  parseTableRef,
  verdictStroke,
  verdictWidth,
} from "@/lib/ontology/encoding";
import { StateNote } from "../primitives";

/**
 * 엣지 인스펙터(SPEC-004 U-6 · 디자인 02).
 *
 * 배지 행은 값이 있을 때만 만든다 — 방향 배지는 `sign` 이 `+`/`−` 일 때만, `lag` 배지는
 * 정본 문자열 원형이 있을 때만, 신뢰도는 `채택` 에만 있다.
 *
 * 「원본 데이터 보기」의 목적지는 **양 끝 노드의 `source` 에서 파생**한다 —
 * 매핑을 화면에 손으로 두지 않는다.
 */
export function EdgeInspector({
  edge,
  nodesById,
  rejectedCount,
  showRejected,
}: {
  edge: GraphEdge | null;
  nodesById: Map<string, GraphNode>;
  rejectedCount: number;
  showRejected: boolean;
}) {
  if (!edge) {
    return <StateNote>엣지를 선택하면 판정·근거·설명이 여기에 표시됩니다.</StateNote>;
  }

  const fromNode = nodesById.get(edge.from);
  const toNode = nodesById.get(edge.to);
  const stroke = verdictStroke(edge.verdict);
  const width = verdictWidth(edge.verdict, edge.confidence);

  // 목적지는 결과 노드의 원천을 먼저 보고, 없으면 원인 노드로 내려간다.
  const ref = parseTableRef(toNode?.source) ?? parseTableRef(fromNode?.source);
  const question = `${fromNode?.name ?? edge.from} → ${toNode?.name ?? edge.to} 엣지는 어떤 근거로 ${edge.verdict}됐어?`;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, minHeight: 0 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 13, fontWeight: 700 }}>
        <span>{fromNode?.name ?? edge.from}</span>
        <svg width="34" height="10" aria-hidden>
          <line
            x1="0"
            y1="5"
            x2="30"
            y2="5"
            stroke={stroke.color}
            strokeWidth={width}
            strokeDasharray={stroke.dash}
            opacity={stroke.opacity}
          />
          <path d={`M30 1 L34 5 L30 9`} fill={stroke.color} opacity={stroke.opacity} />
        </svg>
        <span>{toNode?.name ?? edge.to}</span>
      </div>

      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        <Badge background={badgeFill(edge.verdict)} color={badgeText(edge.verdict)}>
          {edge.verdict}
        </Badge>
        {hasDirection(edge.sign) && (
          <Badge background="var(--ont-hover)" color="var(--ont-ink)" mono>
            {directionGlyph(edge.sign)}
          </Badge>
        )}
        {edge.lag && (
          <Badge background="var(--ont-hover)" color="var(--ont-body)" mono>
            lag {edge.lag}
          </Badge>
        )}
        {edge.confidence && (
          <Badge background="var(--ont-hover)" color="var(--ont-body)">
            신뢰도 {edge.confidence}
          </Badge>
        )}
        <Badge background="var(--ont-primary-fill)" color="var(--ont-primary-deep)" mono>
          {edge.kind}
        </Badge>
      </div>

      <div
        className="ont-mono"
        style={{
          background: "var(--ont-canvas)",
          border: "1px solid var(--ont-border)",
          borderRadius: 6,
          padding: "9px 12px",
          fontSize: 12,
          lineHeight: 1.6,
          color: "var(--ont-ink)",
        }}
      >
        {edge.evidence}
      </div>

      {edge.note && (
        <p style={{ margin: 0, fontSize: 12, lineHeight: 1.6, color: "var(--ont-body)" }}>{edge.note}</p>
      )}
      {edge.reason && (
        <p style={{ margin: 0, fontSize: 12, lineHeight: 1.6, color: "var(--ont-body)" }}>
          <strong style={{ color: "var(--ont-alert-text)" }}>{edge.verdict} 사유</strong> — {edge.reason}
        </p>
      )}

      <div style={{ display: "flex", gap: 8, marginTop: "auto", paddingTop: 4 }}>
        {ref ? (
          <Link href={dataHref(ref)} style={linkButtonStyle}>
            원본 데이터 보기
          </Link>
        ) : (
          <span style={{ ...linkButtonStyle, opacity: 0.45, cursor: "not-allowed" }} title="양 끝 노드에 원천 테이블이 없습니다">
            원본 데이터 보기
          </span>
        )}
        <Link href={`/ontology/chat?q=${encodeURIComponent(question)}`} style={linkButtonStyle}>
          이 엣지로 질문하기
        </Link>
      </div>

      <p style={{ margin: 0, fontSize: 12, color: "var(--ont-muted)", lineHeight: 1.6 }}>
        {showRejected
          ? `기각 엣지 ${rejectedCount}건이 표시됩니다 — 따져봤고 아니었다는 기록입니다.`
          : `기각 엣지 ${rejectedCount}건은 토글로 볼 수 있습니다 — 따져봤고 아니었다는 기록입니다.`}
      </p>
    </div>
  );
}

const linkButtonStyle = {
  height: 30,
  display: "inline-flex",
  alignItems: "center",
  padding: "0 12px",
  borderRadius: 8,
  border: "1px solid var(--ont-border-card)",
  background: "var(--ont-surface)",
  color: "var(--ont-body)",
  fontSize: 13,
} as const;

function badgeFill(verdict: string): string {
  if (verdict === "채택") return "var(--ont-ink)";
  if (verdict === "자동 확정") return "var(--ont-primary-fill)";
  if (verdict === "보류") return "var(--ont-watch-fill)";
  if (verdict === "기각") return "var(--ont-alert-fill)";
  return "var(--ont-hover)";
}

function badgeText(verdict: string): string {
  if (verdict === "채택") return "#fff";
  if (verdict === "자동 확정") return "var(--ont-primary-deep)";
  if (verdict === "보류") return "var(--ont-watch-text)";
  if (verdict === "기각") return "var(--ont-alert-text)";
  return "var(--ont-body)";
}

function Badge({
  children,
  background,
  color,
  mono,
}: {
  children: React.ReactNode;
  background: string;
  color: string;
  mono?: boolean;
}) {
  return (
    <span
      className={mono ? "ont-mono" : undefined}
      style={{
        height: 24,
        display: "inline-flex",
        alignItems: "center",
        padding: "0 9px",
        borderRadius: 6,
        background,
        color,
        fontSize: 12,
        fontWeight: 600,
      }}
    >
      {children}
    </span>
  );
}
