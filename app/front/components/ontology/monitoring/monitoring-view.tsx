"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { ontologyApi } from "@/lib/ontology/client";
import type { ForecastResponse, GraphResponse, KpiCardsResponse } from "@/lib/ontology/types";
import { formatPeriod, shiftPeriod } from "@/lib/ontology/encoding";
import { missingCoords } from "@/lib/ontology/node-layout";
import { OntologyShell, ScreenBody, ScreenTitle } from "../shell";
import { OntButton, Panel, StateNote } from "../primitives";
import { KpiCardRow } from "./kpi-cards";
import { CausalGraph, GraphLegend, filterGraph, type GraphFilters } from "./causal-graph";
import { EdgeInspector } from "./edge-inspector";
import { ForecastCards } from "./forecast-cards";

/**
 * 모니터링 — 「지금 봐야 할 것 → 왜 그런지 → 다음 위험」이 한 화면에서 이어진다.
 *
 * - 그래프 데이터는 **최초 1회**만 받는다. 툴바 토글은 전부 클라이언트 필터다(AC-9).
 * - 헤더 카운트·범례 개수·탭 배지·기준일은 전부 응답 파생이다(AC-8).
 * - `?edge=<edge_id>` 로 들어오면 그 엣지가 선택 상태로 진입한다(AC-14).
 */
export function MonitoringView() {
  const searchParams = useSearchParams();
  const edgeParam = searchParams.get("edge");

  const [period, setPeriod] = useState<string | null>(null);
  const [cards, setCards] = useState<KpiCardsResponse | null>(null);
  const [graph, setGraph] = useState<GraphResponse | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [filters, setFilters] = useState<GraphFilters>({
    verdictFilter: "all",
    showRejected: false,
    showUnobserved: true,
  });
  const [selectedEdgeId, setSelectedEdgeId] = useState<string | null>(edgeParam);
  const [hoverEdgeId, setHoverEdgeId] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  // KPI 카드는 기간 파라미터에 물린다.
  useEffect(() => {
    let cancelled = false;
    ontologyApi
      .kpiCards(period ?? undefined)
      .then((res) => {
        if (!cancelled) setCards(res);
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [period]);

  // 그래프·예보는 기간과 무관하게 1회.
  useEffect(() => {
    let cancelled = false;
    Promise.all([ontologyApi.graph(), ontologyApi.forecast()])
      .then(([graphRes, forecastRes]) => {
        if (cancelled) return;
        setGraph(graphRes);
        setForecast(forecastRes);
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const nodesById = useMemo(
    () => new Map((graph?.nodes ?? []).map((node) => [node.node_id, node])),
    [graph],
  );

  const visible = useMemo(
    () => filterGraph(graph?.nodes ?? [], graph?.edges ?? [], filters),
    [graph, filters],
  );

  // `?edge=` 가 없으면 채택 엣지 중 첫 번째를 연다(디자인 04 §5).
  useEffect(() => {
    if (!graph || selectedEdgeId) return;
    const first = graph.edges.find((edge) => edge.verdict === "채택") ?? graph.edges[0];
    if (first) setSelectedEdgeId(first.edge_id);
  }, [graph, selectedEdgeId]);

  // 기각 엣지로 진입하면 토글을 켜 준다 — 선택했는데 안 보이는 상태를 만들지 않는다.
  useEffect(() => {
    if (!graph || !edgeParam) return;
    const target = graph.edges.find((edge) => edge.edge_id === edgeParam);
    if (!target) return;
    setFilters((prev) => ({
      ...prev,
      showRejected: prev.showRejected || target.verdict === "기각",
      verdictFilter: target.verdict === "채택" ? prev.verdictFilter : "all",
    }));
  }, [graph, edgeParam]);

  const selectedEdge = graph?.edges.find((edge) => edge.edge_id === selectedEdgeId) ?? null;
  const missing = graph ? missingCoords(graph.nodes.map((node) => node.node_id)) : [];
  const rejectedCount = graph?.counts["기각"] ?? 0;

  return (
    <OntologyShell cards={cards?.cards ?? null} asOf={cards?.as_of ?? null}>
      <ScreenBody>
        <ScreenTitle
          title="모니터링"
          meta="최근 7일 이상 빈도로 판정 · 일 1회 배치"
          right={
            cards && (
              <PeriodStepper
                period={cards.period}
                hasNext={cards.has_next_period}
                onChange={setPeriod}
              />
            )
          }
        />

        {error && <StateNote tone="alert">데이터를 불러오지 못했습니다 — {error}</StateNote>}

        {missing.length > 0 && (
          <StateNote tone="alert">
            좌표 자산에 없는 노드가 {missing.length}건 있습니다 — {missing.join(", ")}. 그래프가
            이 노드를 그리지 못합니다(조용히 빼지 않습니다).
          </StateNote>
        )}

        {cards ? (
          <KpiCardRow
            cards={cards.cards}
            selectedNodeId={selectedNodeId}
            onSelectNode={(nodeId) => {
              setSelectedNodeId(nodeId);
              const incident = (graph?.edges ?? []).find(
                (edge) => edge.from === nodeId || edge.to === nodeId,
              );
              if (incident) setSelectedEdgeId(incident.edge_id);
            }}
          />
        ) : (
          <StateNote>KPI 카드를 불러오는 중입니다.</StateNote>
        )}

        <div style={{ display: "flex", gap: 16, minHeight: 640, flex: 1 }}>
          <Panel padded={false} style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
            <header
              style={{
                height: 60,
                flexShrink: 0,
                display: "flex",
                alignItems: "center",
                gap: 14,
                padding: "0 20px",
                borderBottom: "1px solid var(--ont-border)",
              }}
            >
              <h2 style={{ margin: 0, fontSize: 16, fontWeight: 700 }}>원인 분석 그래프</h2>
              {graph && (
                <span className="ont-mono" style={{ fontSize: 12, color: "var(--ont-muted)" }}>
                  노드 {visible.nodes.length}/{graph.nodes.length} · 엣지 {visible.edges.length}/
                  {graph.edges.length}
                </span>
              )}
              <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
                <OntButton
                  tone={filters.verdictFilter === "all" ? "ink" : "secondary"}
                  onClick={() => setFilters((prev) => ({ ...prev, verdictFilter: "all" }))}
                >
                  판정 전체
                </OntButton>
                <OntButton
                  tone={filters.verdictFilter === "adopted" ? "ink" : "secondary"}
                  onClick={() => setFilters((prev) => ({ ...prev, verdictFilter: "adopted" }))}
                >
                  채택만
                </OntButton>
                <ToggleButton
                  checked={filters.showRejected}
                  label={`기각 ${rejectedCount}`}
                  onToggle={() => setFilters((prev) => ({ ...prev, showRejected: !prev.showRejected }))}
                />
                <ToggleButton
                  checked={filters.showUnobserved}
                  label="미관측"
                  onToggle={() =>
                    setFilters((prev) => ({ ...prev, showUnobserved: !prev.showUnobserved }))
                  }
                />
              </div>
            </header>

            <div style={{ position: "relative", flex: 1, background: "var(--ont-graph-canvas)", minHeight: 0 }}>
              {graph ? (
                <>
                  <CausalGraph
                    nodes={visible.nodes}
                    edges={visible.edges}
                    selectedEdgeId={selectedEdgeId}
                    hoverEdgeId={hoverEdgeId}
                    selectedNodeId={selectedNodeId}
                    onSelectEdge={setSelectedEdgeId}
                    onHoverEdge={setHoverEdgeId}
                  />
                  <GraphLegend counts={graph.counts} />
                </>
              ) : (
                <StateNote>그래프를 불러오는 중입니다.</StateNote>
              )}
            </div>
          </Panel>

          <div style={{ width: 480, flexShrink: 0, display: "flex", flexDirection: "column", gap: 16 }}>
            <Panel style={{ flexShrink: 0 }}>
              <h2 style={{ margin: "0 0 12px", fontSize: 16, fontWeight: 700 }}>다음 위험</h2>
              {forecast ? (
                <ForecastCards forecasts={forecast.forecasts} />
              ) : (
                <StateNote>예보를 불러오는 중입니다.</StateNote>
              )}
            </Panel>

            <Panel style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
              <h2 style={{ margin: "0 0 12px", fontSize: 16, fontWeight: 700 }}>엣지 인스펙터</h2>
              <EdgeInspector
                edge={selectedEdge}
                nodesById={nodesById}
                rejectedCount={rejectedCount}
                showRejected={filters.showRejected}
              />
            </Panel>
          </div>
        </div>
      </ScreenBody>
    </OntologyShell>
  );
}

/** 기간 스테퍼 — 다음 기간이 없으면 화살표가 비활성이다(U-4). */
function PeriodStepper({
  period,
  hasNext,
  onChange,
}: {
  period: string;
  hasNext: boolean;
  onChange: (period: string) => void;
}) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <StepButton label="◀" onClick={() => onChange(shiftPeriod(period, -1))} />
      <span style={{ height: 30, display: "inline-flex", alignItems: "center", fontSize: 14, fontWeight: 600 }}>
        {formatPeriod(period)}
      </span>
      <StepButton
        label="▶"
        disabled={!hasNext}
        onClick={() => hasNext && onChange(shiftPeriod(period, 1))}
      />
    </div>
  );
}

function StepButton({
  label,
  onClick,
  disabled,
}: {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      style={{
        width: 30,
        height: 30,
        borderRadius: 8,
        border: "1px solid var(--ont-border-card)",
        background: "var(--ont-surface)",
        color: disabled ? "var(--ont-placeholder)" : "var(--ont-body)",
        fontSize: 11,
        cursor: disabled ? "not-allowed" : "pointer",
      }}
    >
      {label}
    </button>
  );
}

function ToggleButton({
  checked,
  label,
  onToggle,
}: {
  checked: boolean;
  label: string;
  onToggle: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onToggle}
      style={{
        height: 34,
        display: "inline-flex",
        alignItems: "center",
        gap: 7,
        padding: "0 12px",
        borderRadius: 8,
        border: "1px solid var(--ont-border-card)",
        background: "var(--ont-surface)",
        color: "var(--ont-body)",
        fontSize: 13,
      }}
    >
      <span
        style={{
          width: 16,
          height: 16,
          borderRadius: 4,
          border: checked ? "1.5px solid var(--ont-primary)" : "1.5px solid var(--ont-border-card)",
          background: checked ? "var(--ont-primary)" : "transparent",
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {checked && (
          <svg width="10" height="10" viewBox="0 0 12 12" aria-hidden>
            <path d="M2 6.5 L5 9.5 L10 3" stroke="#fff" strokeWidth="2" fill="none" />
          </svg>
        )}
      </span>
      {label}
    </button>
  );
}
