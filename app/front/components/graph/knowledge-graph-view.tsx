"use client";

import { forceX, forceY } from "d3-force";
import { useEffect, useMemo, useRef, useState } from "react";
import { NoteDetailPanel } from "@/components/notes/notes-graph-view";
import type { Lang } from "@/lib/i18n";
import type { GraphNodeType, GraphResponse, NoteDetail } from "@/lib/types";

// SSR 회피 — useEffect 안에서 lazy import. ref 정상 forwarding. (notes-graph-view 패턴 복제)
type FGComponent = React.ComponentType<Record<string, unknown> & { ref?: unknown }>;

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

// SPEC-005 §5 — 노드 색 = type. 5색(reference/permanent/post/product/idea).
const TYPE_COLOR: Record<GraphNodeType, string> = {
  reference: "oklch(0.72 0.13 240)", // blue
  permanent: "oklch(0.78 0.14 145)", // green (notes accent 계열)
  post: "oklch(0.82 0.13 80)", // gold
  product: "oklch(0.70 0.16 320)", // magenta
  idea: "oklch(0.76 0.15 50)", // orange
};

const TYPE_ORDER: GraphNodeType[] = [
  "reference",
  "permanent",
  "post",
  "product",
  "idea",
];

// `/api/notes/{id}` 패널을 재사용할 수 있는 노트성 타입. product/idea는 정식 이동 = WORK-009.
const NOTE_TYPES = new Set<GraphNodeType>(["reference", "permanent", "post"]);

// react-force-graph는 첫 렌더 후 link.source/target을 string id → node 객체로 변형한다.
const endId = (v: unknown): string =>
  typeof v === "object" && v !== null && "id" in v
    ? String((v as { id: string | number }).id)
    : String(v);

export function KnowledgeGraphView({
  graphData,
  lang,
}: {
  graphData: GraphResponse;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  const [activeTypes, setActiveTypes] = useState<Set<GraphNodeType>>(
    () => new Set(TYPE_ORDER),
  );
  const [hoverId, setHoverId] = useState<string | null>(null);
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

  // type별 노드 개수 (범례 표기)
  const typeCounts = useMemo(() => {
    const m = {} as Record<GraphNodeType, number>;
    TYPE_ORDER.forEach((ty) => (m[ty] = 0));
    graphData.nodes.forEach((n) => {
      if (n.type in m) m[n.type] += 1;
    });
    return m;
  }, [graphData]);

  // 필터된 노드/엣지 + 이웃 인접 맵 (string id 기준으로 미리 계산)
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
    if (!detail) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setDetail(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [detail]);

  // 포커스(hover) 시 이웃 외 노드를 흐리게 — null이면 강조 없음
  const isDimmed = (id: string): boolean => {
    if (!hoverId) return false;
    if (id === hoverId) return false;
    return !neighbors[hoverId]?.has(id);
  };

  function toggleType(ty: GraphNodeType) {
    setActiveTypes((prev) => {
      const next = new Set(prev);
      if (next.has(ty)) next.delete(ty);
      else next.add(ty);
      // 전부 끄면 다시 전체 (빈 그래프 방지)
      return next.size === 0 ? new Set(TYPE_ORDER) : next;
    });
  }

  async function onNodeClick(node: {
    id?: string | number;
    type?: GraphNodeType;
  }) {
    if (!node.id || !node.type) return;
    // product/idea 등은 정식 이동(WORK-009) — 이 work는 패널/하이라이트까지.
    if (!NOTE_TYPES.has(node.type)) {
      setHoverId(String(node.id));
      return;
    }
    setLoadingDetail(true);
    try {
      const id = encodeURIComponent(String(node.id));
      const res = await fetch(`${API_BASE}/api/notes/${id}?lang=${lang}`, {
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

  const panelOpen = detail || loadingDetail;

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
                  type: GraphNodeType;
                  archived?: boolean;
                };
                const base = TYPE_COLOR[node.type] ?? "oklch(0.7 0 0)";
                const lc = base.slice(0, -1); // "oklch(L C H" → 알파 합성용
                // archived 흐리게 + hover 시 비이웃 흐리게 (둘 다면 더 흐리게)
                let alpha = node.archived ? 0.3 : 1;
                if (isDimmed(node.id)) alpha = Math.min(alpha, 0.12);
                return alpha === 1 ? base : `${lc} / ${alpha})`;
              }}
              linkColor={(l: object) => {
                const link = l as { source: unknown; target: unknown; type?: string };
                const s = endId(link.source);
                const tgt = endId(link.target);
                const touch = hoverId && (s === hoverId || tgt === hoverId);
                if (touch) return "rgba(255,255,255,0.45)";
                if (hoverId) return "rgba(255,255,255,0.04)";
                return link.type === "lineage"
                  ? "rgba(255,255,255,0.22)"
                  : "rgba(255,255,255,0.1)";
              }}
              linkWidth={(l: object) =>
                (l as { type?: string }).type === "lineage" ? 0.9 : 0.6
              }
              // lineage = 화살표, assoc = 무방향 선
              linkDirectionalArrowLength={(l: object) =>
                (l as { type?: string }).type === "lineage" ? 3 : 0
              }
              linkDirectionalArrowRelPos={1}
              backgroundColor="transparent"
              onNodeClick={onNodeClick}
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

          {/* 범례 — 좌측 상단. 클릭 = type 필터 토글 (SPEC-005 §5) */}
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
            {TYPE_ORDER.map((ty) => {
              const on = activeTypes.has(ty);
              return (
                <button
                  key={ty}
                  type="button"
                  onClick={() => toggleType(ty)}
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
                      background: TYPE_COLOR[ty],
                      flexShrink: 0,
                    }}
                  />
                  {ty}
                  <span style={{ color: "var(--fg-3)" }}>{typeCounts[ty]}</span>
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

        {/* 노드 클릭 패널 — notes NoteDetailPanel 재사용 */}
        <NoteDetailPanel
          detail={detail}
          loading={loadingDetail}
          onClose={() => setDetail(null)}
          lang={lang}
        />
      </div>
    </div>
  );
}
