"use client";

import { forceX, forceY } from "d3-force";
import { useEffect, useMemo, useRef, useState } from "react";
import { LocalGraph } from "@/components/graph/local-graph";
import { NoteDetailPanel } from "@/components/notes/notes-graph-view";
import {
  arrowLengthFor,
  endId,
  LINK_COLOR_ASSOC,
  LINK_COLOR_LINEAGE,
  nodeColorFor,
  NOTE_TYPES,
  presentTypes,
  TYPE_COLOR,
} from "@/lib/graph";
import type { Lang } from "@/lib/i18n";
import type { GraphResponse, NoteDetail } from "@/lib/types";

// SSR 회피 — useEffect 안에서 lazy import. ref 정상 forwarding. (notes-graph-view 패턴 복제)
type FGComponent = React.ComponentType<Record<string, unknown> & { ref?: unknown }>;

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

export function KnowledgeGraphView({
  graphData,
  lang,
}: {
  graphData: GraphResponse;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  // 데이터에 실제 등장하는 타입만 (stale 문서 5종이 아니라 라이브 8종 기반)
  const legend = useMemo(() => presentTypes(graphData.nodes), [graphData]);

  const [activeTypes, setActiveTypes] = useState<Set<string>>(
    () => new Set(legend.map((l) => l.type)),
  );
  const [hoverId, setHoverId] = useState<string | null>(null);
  const [selected, setSelected] = useState<{ id: string; type: string } | null>(
    null,
  );
  const [detail, setDetail] = useState<NoteDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const fgRef = useRef<unknown>(null);
  const [size, setSize] = useState({ w: 800, h: 600 });
  const [ForceGraph2D, setForceGraph2D] = useState<FGComponent | null>(null);

  // 클라이언트 사이드에서만 import (SSR 회피)
  useEffect(() => {
    let mounted = true;
    import("react-force-graph-2d").then((mod) => {
      if (mounted) setForceGraph2D(() => mod.default as unknown as FGComponent);
    });
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!containerRef.current) return;
    const el = containerRef.current;
    const obs = new ResizeObserver((entries) => {
      const r = entries[0].contentRect;
      setSize({ w: r.width, h: Math.max(500, r.height) });
    });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  // 필터된 노드/엣지 + 이웃 인접 맵 (pristine GraphResponse 에서 string id 기준 계산 후 복사)
  const { graph, neighbors } = useMemo(() => {
    const nodes = graphData.nodes.filter((n) => activeTypes.has(n.type));
    const visible = new Set(nodes.map((n) => n.id));
    const links = graphData.edges
      .filter((e) => visible.has(endId(e.source)) && visible.has(endId(e.target)))
      .map((e) => ({
        source: endId(e.source),
        target: endId(e.target),
        type: e.type,
        dir: e.dir ?? null,
      }));
    const nbr: Record<string, Set<string>> = {};
    links.forEach((l) => {
      (nbr[l.source] ??= new Set()).add(l.target);
      (nbr[l.target] ??= new Set()).add(l.source);
    });
    return {
      graph: { nodes: nodes.map((n) => ({ ...n })), links },
      neighbors: nbr,
    };
  }, [graphData, activeTypes]);

  // d3Force tuning + reheat + zoomToFit (notes-graph-view 패턴 복제)
  useEffect(() => {
    const fg = fgRef.current as
      | {
          d3Force?: (
            name: string,
            force?: unknown,
          ) =>
            | { strength?: (v: number) => unknown; distance?: (v: number) => unknown }
            | undefined;
          d3ReheatSimulation?: () => unknown;
          zoomToFit?: (ms?: number, padding?: number) => unknown;
        }
      | null;
    if (!fg?.d3Force) return;
    const charge = fg.d3Force("charge");
    charge?.strength?.(-60);
    const link = fg.d3Force("link");
    link?.distance?.(30);
    link?.strength?.(1);
    fg.d3Force("center-x", forceX(0).strength(0.12));
    fg.d3Force("center-y", forceY(0).strength(0.12));
    fg.d3ReheatSimulation?.();
    const t1 = setTimeout(() => fg.zoomToFit?.(400, 40), 1500);
    const t2 = setTimeout(() => fg.zoomToFit?.(400, 40), 3000);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [graph, ForceGraph2D]);

  useEffect(() => {
    if (!selected) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") closePanel();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selected]);

  // 포커스(hover) 시 이웃 외 노드를 흐리게 — null이면 강조 없음
  const isDimmed = (id: string): boolean => {
    if (!hoverId) return false;
    if (id === hoverId) return false;
    return !neighbors[hoverId]?.has(id);
  };

  function toggleType(ty: string) {
    setActiveTypes((prev) => {
      const next = new Set(prev);
      if (next.has(ty)) next.delete(ty);
      else next.add(ty);
      // 전부 끄면 다시 전체 (빈 그래프 방지)
      return next.size === 0 ? new Set(legend.map((l) => l.type)) : next;
    });
  }

  function closePanel() {
    setSelected(null);
    setDetail(null);
  }

  // 노드 선택(전역 클릭·로컬 그래프 이웃 클릭 공용). reference(notes)면 상세 fetch, 그 외는 로컬 그래프만.
  async function selectNode(id: string, type: string) {
    setSelected({ id, type });
    if (!NOTE_TYPES.has(type)) {
      setDetail(null);
      setLoadingDetail(false);
      return;
    }
    setLoadingDetail(true);
    setDetail(null);
    try {
      const encoded = encodeURIComponent(id);
      const res = await fetch(`${API_BASE}/api/notes/${encoded}?lang=${lang}`, {
        cache: "no-store",
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      setDetail(data["notes.detail"]);
    } catch (err) {
      console.error("[graph] detail fetch failed:", err);
      setDetail(null);
    } finally {
      setLoadingDetail(false);
    }
  }

  const panelOpen = selected !== null;

  return (
    <div
      className="pad-x graph-main"
      style={{
        padding: "24px 80px 24px",
        height: "calc(100vh - 200px)",
        minHeight: 600,
      }}
    >
      <style>{`
        @media (max-width: 720px) {
          .graph-main { padding-left: 20px !important; padding-right: 20px !important; }
          .graph-area { grid-template-columns: 1fr !important; }
          .graph-area > .graph-canvas { ${panelOpen ? "display: none;" : ""} }
        }
      `}</style>

      <div
        className="graph-area"
        style={{
          display: "grid",
          gridTemplateColumns: panelOpen
            ? "minmax(0, 2fr) minmax(0, 1fr)"
            : "1fr",
          gap: 0,
          border: "1px solid var(--line-1)",
          borderRadius: 6,
          overflow: "hidden",
          background: "var(--bg-1)",
          height: "100%",
          minHeight: 500,
        }}
      >
        <div
          ref={containerRef}
          className="graph-canvas"
          style={{ position: "relative", overflow: "hidden", minHeight: 500 }}
        >
          {ForceGraph2D && graph.nodes.length > 0 ? (
            <ForceGraph2D
              ref={fgRef as never}
              graphData={graph}
              width={size.w}
              height={size.h}
              nodeId="id"
              nodeLabel={(n: object) => (n as { title?: string }).title ?? ""}
              nodeRelSize={4}
              nodeVal={() => 1}
              nodeColor={(n: object) => {
                const node = n as {
                  id: string;
                  type: string;
                  archived?: boolean;
                };
                return nodeColorFor(node.type, {
                  archived: node.archived,
                  dimmed: isDimmed(node.id),
                });
              }}
              linkColor={(l: object) => {
                const link = l as { source: unknown; target: unknown; type?: string };
                const s = endId(link.source);
                const tgt = endId(link.target);
                const touch = hoverId && (s === hoverId || tgt === hoverId);
                if (touch) return "rgba(255,255,255,0.45)";
                if (hoverId) return "rgba(255,255,255,0.04)";
                return link.type === "lineage"
                  ? LINK_COLOR_LINEAGE
                  : LINK_COLOR_ASSOC;
              }}
              linkWidth={(l: object) =>
                (l as { type?: string }).type === "lineage" ? 0.9 : 0.6
              }
              // lineage = 화살표, assoc = 무방향 선
              linkDirectionalArrowLength={(l: object) =>
                arrowLengthFor((l as { type?: string }).type)
              }
              linkDirectionalArrowRelPos={1}
              backgroundColor="transparent"
              onNodeClick={(n: object) => {
                const node = n as { id?: string | number; type?: string };
                if (node.id && node.type) selectNode(String(node.id), node.type);
              }}
              onNodeHover={(n: object | null) =>
                setHoverId(n ? String((n as { id: string }).id) : null)
              }
              d3VelocityDecay={0.5}
              d3AlphaDecay={0.02}
              cooldownTicks={250}
            />
          ) : (
            <div
              className="mono"
              style={{
                height: "100%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "var(--fg-3)",
                fontSize: 11,
              }}
            >
              {graphData.nodes.length === 0
                ? t("// 그래프 비어있음", "// empty graph")
                : "// loading graph..."}
            </div>
          )}

          {/* 범례 — 좌측 상단. 데이터에 등장하는 type만. 클릭 = 필터 토글 (SPEC-005 §5) */}
          <div
            className="mono"
            style={{
              position: "absolute",
              top: 12,
              left: 16,
              display: "flex",
              flexWrap: "wrap",
              gap: 10,
              fontSize: 11,
              maxWidth: "calc(100% - 32px)",
            }}
          >
            {legend.map(({ type, count }) => {
              const on = activeTypes.has(type);
              return (
                <button
                  key={type}
                  type="button"
                  onClick={() => toggleType(type)}
                  title={t("type 필터 토글", "toggle type filter")}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    padding: "2px 6px",
                    background: "transparent",
                    border: "none",
                    cursor: "pointer",
                    color: on ? "var(--fg-1)" : "var(--fg-3)",
                    opacity: on ? 1 : 0.5,
                    fontFamily: "var(--font-mono)",
                    fontSize: 11,
                  }}
                >
                  <span
                    style={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      background: TYPE_COLOR[type] ?? "oklch(0.70 0.02 250)",
                      flexShrink: 0,
                    }}
                  />
                  {type}
                  <span style={{ color: "var(--fg-3)" }}>{count}</span>
                </button>
              );
            })}
          </div>

          <div
            className="mono"
            style={{
              position: "absolute",
              bottom: 12,
              right: 16,
              fontSize: 10,
              color: "var(--fg-3)",
            }}
          >
            {graph.nodes.length} nodes · {graph.links.length} edges
          </div>
        </div>

        {/* 노드 클릭 패널 — 로컬 그래프(WORK-009) + NoteDetailPanel(notes 재사용) */}
        {panelOpen && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              overflowY: "auto",
              minHeight: 0,
            }}
          >
            {selected && (
              <LocalGraph
                graphData={graphData}
                centerId={selected.id}
                onSelectNode={selectNode}
                onClose={closePanel}
                lang={lang}
              />
            )}
            <NoteDetailPanel
              detail={detail}
              loading={loadingDetail}
              onClose={closePanel}
              lang={lang}
            />
          </div>
        )}
      </div>
    </div>
  );
}
