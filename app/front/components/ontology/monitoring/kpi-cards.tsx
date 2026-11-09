"use client";

import type { KpiCard } from "@/lib/ontology/types";
import {
  formatDelta,
  formatMetricValue,
  grainCaption,
  sortCardsBySeverity,
  stateTone,
} from "@/lib/ontology/encoding";
import { StatusDot } from "../primitives";

/**
 * KPI 카드 행 — **알림 → 관찰 → 미관측 → 정상** 정렬, 알림이 항상 맨 왼쪽(U-4).
 *
 * 카드로 낼 지표를 고르는 규칙(화면 몫):
 *   1. **정상이 아닌 카드는 전건** 낸다 — 봐야 할 것을 접지 않는다(최대 `MAX_SLOTS`).
 *   2. 그래도 5장이 안 되면 정상 카드로 채운다(디자인 04 의 5슬롯).
 *   3. 남은 것은 「그 외 KPI」 로 접고, **상태별 내역을 파생**시킨다 —
 *      「나머지 전부 정상」이라고 단정하지 않는다(디자인 08 규칙 7).
 *
 * 값·상태·전일 대비·스파크라인·개수는 전부 `/api/kpi/cards` 파생이다. 하드코딩 0건.
 */

const MIN_SLOTS = 5;
const MAX_SLOTS = 8;

export function selectCards(cards: KpiCard[]): { featured: KpiCard[]; rest: KpiCard[] } {
  const sorted = sortCardsBySeverity(cards);
  const abnormal = sorted.filter((card) => card.node_state !== null && card.node_state !== "정상");
  const featured = sorted.slice(0, Math.min(Math.max(abnormal.length, MIN_SLOTS), MAX_SLOTS));
  const featuredIds = new Set(featured.map((card) => card.metric));
  return { featured, rest: sorted.filter((card) => !featuredIds.has(card.metric)) };
}

export function KpiCardRow({
  cards,
  selectedNodeId,
  onSelectNode,
}: {
  cards: KpiCard[];
  selectedNodeId: string | null;
  onSelectNode: (nodeId: string) => void;
}) {
  const { featured, rest } = selectCards(cards);

  return (
    <div style={{ display: "flex", gap: 16, flexShrink: 0, alignItems: "stretch" }}>
      {featured.map((card) => (
        <MetricCard
          key={card.metric}
          card={card}
          selected={card.node_id === selectedNodeId}
          onSelect={() => onSelectNode(card.node_id)}
        />
      ))}
      <RestCard rest={rest} />
    </div>
  );
}

function MetricCard({
  card,
  selected,
  onSelect,
}: {
  card: KpiCard;
  selected: boolean;
  onSelect: () => void;
}) {
  const tone = stateTone(card.node_state);
  const isAlert = card.node_state === "알림";
  const isUnobserved = card.node_state === "미관측";
  const delta = formatDelta(card.dod, card.dod_pct, card.format);

  return (
    <button
      type="button"
      onClick={onSelect}
      title="카드를 누르면 아래 그래프에서 해당 노드가 선택됩니다"
      style={{
        position: "relative",
        overflow: "hidden",
        flex: 1,
        minWidth: 0,
        height: 132,
        borderRadius: 16,
        background: "var(--ont-surface)",
        border: isUnobserved
          ? "1px dashed var(--ont-border-card)"
          : `1px solid ${selected ? "var(--ont-ink)" : "var(--ont-border)"}`,
        boxShadow: "var(--ont-shadow-metric)",
        padding: "16px 18px",
        textAlign: "left",
        display: "flex",
        flexDirection: "column",
        transition: "border-color var(--ont-transition)",
      }}
    >
      {isAlert && (
        <span
          aria-hidden
          style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 2, background: "var(--ont-alert)" }}
        />
      )}

      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontSize: 13, color: "var(--ont-body)", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
          {card.label}
        </span>
        <span style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 5 }}>
          {card.node_state !== null && <StatusDot state={card.node_state} />}
          <span style={{ fontSize: 13, color: card.node_state ? tone.text : "var(--ont-muted)" }}>
            {card.node_state ?? "상태 없음"}
          </span>
        </span>
      </div>

      <div style={{ marginTop: 8, display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
        <span
          className="ont-mono"
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: isAlert ? "var(--ont-alert)" : isUnobserved ? "var(--ont-placeholder)" : "var(--ont-ink)",
          }}
        >
          {formatMetricValue(card.latest, card.format)}
        </span>
        {delta && (
          <span className="ont-mono" style={{ fontSize: 13, color: "var(--ont-body)" }}>
            {delta}
          </span>
        )}
      </div>

      <div style={{ marginTop: 2, fontSize: 12, color: "var(--ont-muted)" }}>
        {card.unit ? `${card.unit} · ` : ""}
        {card.node_state === "미관측" ? "관측되지 않는 항목입니다" : grainCaption(card.grain)}
      </div>

      {card.spark && card.spark.length > 0 && (
        <div style={{ marginTop: "auto", display: "flex", alignItems: "flex-end", gap: 3, height: 26 }}>
          <Sparkline values={card.spark} tone={tone.spark} accent={tone.dot} />
        </div>
      )}
    </button>
  );
}

function Sparkline({ values, tone, accent }: { values: number[]; tone: string; accent: string }) {
  const max = Math.max(...values.map((v) => Math.abs(v)), 0.000001);
  return (
    <>
      {values.map((value, index) => (
        <span
          key={`${index}-${value}`}
          style={{
            flex: 1,
            borderRadius: 2,
            height: `${Math.max((Math.abs(value) / max) * 100, 8)}%`,
            background: index >= values.length - 2 ? accent : tone,
          }}
        />
      ))}
    </>
  );
}

/**
 * 「그 외 KPI」 — 카드로 낸 지표를 제외한 나머지. 상태별 내역을 파생시키고,
 * 관찰·미관측이 섞여 있으면 그대로 드러낸다.
 */
function RestCard({ rest }: { rest: KpiCard[] }) {
  const breakdown = rest.reduce<Record<string, number>>((acc, card) => {
    const key = card.node_state ?? "상태 없음";
    if (key === "정상") return acc;
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
  }, {});
  const detail = Object.entries(breakdown)
    .map(([state, count]) => `${state} ${count}`)
    .join(" · ");

  return (
    <div
      style={{
        width: 120,
        flexShrink: 0,
        height: 132,
        borderRadius: 16,
        border: "1px dashed var(--ont-border-card)",
        background: "var(--ont-surface)",
        padding: "16px 14px",
        display: "flex",
        flexDirection: "column",
        gap: 6,
        justifyContent: "center",
      }}
    >
      <span style={{ fontSize: 13, color: "var(--ont-body)" }}>그 외 KPI</span>
      <span className="ont-mono" style={{ fontSize: 24, fontWeight: 700 }}>
        {rest.length}
      </span>
      {detail && <span style={{ fontSize: 12, color: "var(--ont-muted)" }}>{detail}</span>}
    </div>
  );
}
