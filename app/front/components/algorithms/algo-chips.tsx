/**
 * 알고리즘 카드/행에 박는 칩들 — diff badge, platform chip, curation chip.
 * proto-algorithms.jsx 의 diffBadge / platformChip / curationChip 이식.
 */

import type { AlgoDifficulty, AlgorithmSource } from "@/lib/types";

const DIFF_MAP = {
  easy: { color: "#7fdb8a", label: "easy" },
  medium: { color: "var(--accent)", label: "medium" },
  hard: { color: "#ff8b6e", label: "hard" },
} as const;

export function DiffBadge({ level }: { level: AlgoDifficulty }) {
  const m = DIFF_MAP[level] ?? DIFF_MAP.medium;
  return (
    <span
      className="mono"
      style={{
        fontSize: 10,
        color: m.color,
        padding: "2px 6px",
        border: `1px solid ${m.color}`,
        borderRadius: 3,
        letterSpacing: "0.08em",
        textTransform: "uppercase",
      }}
    >
      {m.label}
    </span>
  );
}

export function PlatformChip({ source }: { source?: AlgorithmSource }) {
  if (!source) return null;
  return (
    <span
      className="mono"
      style={{
        fontSize: 10,
        color: "var(--fg-2)",
        padding: "2px 6px",
        border: "1px solid var(--line-2)",
        borderRadius: 3,
      }}
    >
      {source.platform} #{source.number}
    </span>
  );
}

export function CurationChip({ source }: { source?: AlgorithmSource }) {
  if (!source?.curatedIn?.length) return null;
  const c = source.curatedIn[0];
  return (
    <span
      className="mono"
      style={{
        fontSize: 10,
        color: "var(--accent)",
        padding: "2px 6px",
        border: "1px solid var(--accent-line)",
        borderRadius: 3,
      }}
    >
      {c}
    </span>
  );
}

export function AlgoSectionHeader({
  idx,
  label,
  title,
}: {
  idx: string;
  label: string;
  title: string;
}) {
  return (
    <div style={{ marginBottom: 18, display: "flex", alignItems: "baseline", gap: 12 }}>
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
        {idx}
      </span>
      <h2 style={{ margin: 0, fontSize: 22, letterSpacing: "-0.015em", fontWeight: 600 }}>
        {title}
      </h2>
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
        · {label}
      </span>
    </div>
  );
}
