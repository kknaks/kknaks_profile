"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { Lang } from "@/lib/i18n";
import {
  arrowLengthFor,
  endId,
  LINK_COLOR_ASSOC,
  LINK_COLOR_LINEAGE,
  nodeColorFor,
} from "@/lib/graph";
import type { GraphResponse } from "@/lib/types";

// notes/knowledge-graph-view 와 동일한 SSR 회피 lazy-import 패턴 (미니 모드).
type FGComponent = React.ComponentType<Record<string, unknown> & { ref?: unknown }>;

// 선택 노드 중심 ego-network: 1-hop 이웃 + backlinks (SPEC-005 U-2, WORK-009).
// 이미 로드된 GraphResponse 에서 클라이언트 추출 — BE/API 무변경.
function egoNetwork(g: GraphResponse, centerId: string) {
  const links: { source: string; target: string; type: string; dir: string | null }[] =
    [];
  const ids = new Set<string>([centerId]);

  for (const e of g.edges) {
    const s = endId(e.source);
    const t = endId(e.target);
    if (s === centerId || t === centerId) {
      ids.add(s);
      ids.add(t);
      links.push({ source: s, target: t, type: e.type, dir: e.dir ?? null });
    }
  }

  // backlinks(역참조) 소스 포함. 기존 엣지가 양방향 어느 쪽으로도 없을 때만 assoc 합성(중복 방지).
  const connected = (a: string, b: string) =>
    links.some(
      (l) =>
        (l.source === a && l.target === b) || (l.source === b && l.target === a),
    );
  for (const src of g.backlinks[centerId] ?? []) {
    if (src === centerId) continue;
    ids.add(src);
    if (!connected(src, centerId)) {
      links.push({ source: src, target: centerId, type: "assoc", dir: null });
    }
  }

  // pristine GraphResponse 에서 노드 복사({...n}) — 미니 그래프 시뮬레이션이 전역 노드 좌표와 충돌하지 않게.
  const nodeMap = new Map(g.nodes.map((n) => [n.id, n]));
  const nodes = [...ids]
    .map((id) => nodeMap.get(id))
    .filter((n): n is NonNullable<typeof n> => Boolean(n))
    .map((n) => ({ ...n }));

  // 링크 dedup (정렬 pair + type)
  const seen = new Set<string>();
  const uniqLinks = links.filter((l) => {
    if (!ids.has(l.source) || !ids.has(l.target)) return false;
    const k = [l.source, l.target].sort().join("|") + "|" + l.type;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });

  return { nodes, links: uniqLinks };
}

export function LocalGraph({
  graphData,
  centerId,
  onSelectNode,
  onClose,
  lang,
}: {
  graphData: GraphResponse;
  centerId: string;
  onSelectNode: (id: string, type: string) => void;
  onClose: () => void;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  const containerRef = useRef<HTMLDivElement>(null);
  const fgRef = useRef<unknown>(null);
  const [width, setWidth] = useState(320);
  const [ForceGraph2D, setForceGraph2D] = useState<FGComponent | null>(null);
  const HEIGHT = 240;

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
      setWidth(entries[0].contentRect.width);
    });
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const ego = useMemo(
    () => egoNetwork(graphData, centerId),
    [graphData, centerId],
  );

  // zoomToFit (전역 뷰 패턴 — 작은 캔버스)
  useEffect(() => {
    const fg = fgRef.current as
      | { zoomToFit?: (ms?: number, padding?: number) => unknown }
      | null;
    if (!fg?.zoomToFit) return;
    const t1 = setTimeout(() => fg.zoomToFit?.(400, 24), 600);
    const t2 = setTimeout(() => fg.zoomToFit?.(400, 24), 1600);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [ego, ForceGraph2D]);

  const neighborCount = ego.nodes.length - 1;

  return (
    <section
      style={{
        borderLeft: "1px solid var(--line-1)",
        borderBottom: "1px solid var(--line-1)",
        background: "var(--bg-2)",
        padding: "16px 20px",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          marginBottom: 10,
        }}
      >
        <span className="mono" style={{ fontSize: 11, color: "var(--accent)" }}>
          // {t("연결된 노트", "connected notes")} {neighborCount}
        </span>
        <button
          type="button"
          onClick={onClose}
          aria-label="close"
          style={{
            marginLeft: "auto",
            background: "transparent",
            border: "1px solid var(--line-2)",
            borderRadius: 4,
            width: 24,
            height: 24,
            color: "var(--fg-2)",
            cursor: "pointer",
            fontSize: 12,
            lineHeight: 1,
          }}
        >
          ✕
        </button>
      </div>

      <div
        ref={containerRef}
        style={{
          position: "relative",
          height: HEIGHT,
          border: "1px solid var(--line-1)",
          borderRadius: 4,
          overflow: "hidden",
          background: "var(--bg-1)",
        }}
      >
        {ForceGraph2D && neighborCount > 0 ? (
          <ForceGraph2D
            ref={fgRef as never}
            graphData={ego}
            width={width}
            height={HEIGHT}
            nodeId="id"
            nodeLabel={(n: object) => (n as { title?: string }).title ?? ""}
            nodeRelSize={4}
            // 중심 노드 강조 — 더 큰 val
            nodeVal={(n: object) =>
              (n as { id: string }).id === centerId ? 6 : 1.5
            }
            nodeColor={(n: object) => {
              const node = n as {
                id: string;
                type: string;
                archived?: boolean;
              };
              // 중심 노드는 항상 또렷, 이웃은 archived면 흐리게 (전역과 동일 규칙)
              return nodeColorFor(node.type, {
                archived: node.id === centerId ? false : node.archived,
              });
            }}
            linkColor={(l: object) =>
              (l as { type?: string }).type === "lineage"
                ? LINK_COLOR_LINEAGE
                : LINK_COLOR_ASSOC
            }
            linkWidth={(l: object) =>
              (l as { type?: string }).type === "lineage" ? 0.9 : 0.6
            }
            linkDirectionalArrowLength={(l: object) =>
              arrowLengthFor((l as { type?: string }).type)
            }
            linkDirectionalArrowRelPos={1}
            backgroundColor="transparent"
            onNodeClick={(n: object) => {
              const node = n as { id: string; type: string };
              if (node.id !== centerId) onSelectNode(node.id, node.type);
            }}
            d3VelocityDecay={0.5}
            d3AlphaDecay={0.025}
            cooldownTicks={120}
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
              textAlign: "center",
              padding: "0 12px",
            }}
          >
            {!ForceGraph2D
              ? "// loading..."
              : t("// 이웃 없음 — 단독 노드", "// no neighbors — isolated node")}
          </div>
        )}
      </div>
    </section>
  );
}
