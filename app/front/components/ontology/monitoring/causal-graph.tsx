"use client";

import { Fragment, useMemo } from "react";
import type { GraphEdge, GraphNode, Verdict } from "@/lib/ontology/types";
import {
  NODE_TYPE_LABEL,
  NODE_TYPE_ORDER,
  VERDICT_ORDER,
  directionGlyph,
  hasDirection,
  stateTone,
  verdictStroke,
  verdictWidth,
} from "@/lib/ontology/encoding";
import { GRAPH_VIEWBOX, NODE_COORDS } from "@/lib/ontology/node-layout";

/**
 * 원인 분석 그래프 — 고정 좌표 정적 SVG(`viewBox 0 0 1130 560`).
 *
 * > 색 = 상태 · 모양 = 노드 타입 · 선 스타일 = 엣지 판정 · 굵기 = **채택 엣지의** 신뢰도
 *
 * 좌표 자산은 확정 `node_id` 로 키잉한다. 응답 노드 중 좌표가 없는 것은 **조용히 빼지
 * 않고** 호출부가 배너로 드러낸다(SPEC-004 AC-10 — `missingCoords`).
 */

export interface GraphFilters {
  verdictFilter: "all" | "adopted";
  showRejected: boolean;
  showUnobserved: boolean;
}

export function filterGraph(
  nodes: GraphNode[],
  edges: GraphEdge[],
  filters: GraphFilters,
): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const unobserved = new Set(nodes.filter((n) => !n.observed).map((n) => n.node_id));

  const visibleNodes = filters.showUnobserved ? nodes : nodes.filter((n) => n.observed);

  const visibleEdges = edges.filter((edge) => {
    if (filters.verdictFilter === "adopted" && edge.verdict !== "채택") return false;
    if (!filters.showRejected && edge.verdict === "기각") return false;
    if (!filters.showUnobserved && (unobserved.has(edge.from) || unobserved.has(edge.to))) return false;
    return true;
  });

  return { nodes: visibleNodes, edges: visibleEdges };
}

interface Point {
  x: number;
  y: number;
}

/** 선 끝 트리밍 — 노드 중심에서 x 72 · y 21 물러난 경계에서 시작·끝난다(디자인 03). */
function boundaryPoint(from: Point, to: Point): Point {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  if (dx === 0 && dy === 0) return from;
  const tx = dx === 0 ? Number.POSITIVE_INFINITY : 72 / Math.abs(dx);
  const ty = dy === 0 ? Number.POSITIVE_INFINITY : 21 / Math.abs(dy);
  const t = Math.min(tx, ty, 1);
  return { x: from.x + dx * t, y: from.y + dy * t };
}

const ARROW_COLORS = ["#1E1E1E", "#7181F8", "#5F6470", "#E3B93C"];

function arrowId(color: string): string {
  return `ont-arrow-${color.replace("#", "")}`;
}

export function CausalGraph({
  nodes,
  edges,
  selectedEdgeId,
  hoverEdgeId,
  selectedNodeId,
  onSelectEdge,
  onHoverEdge,
}: {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedEdgeId: string | null;
  hoverEdgeId: string | null;
  selectedNodeId: string | null;
  onSelectEdge: (edgeId: string) => void;
  onHoverEdge: (edgeId: string | null) => void;
}) {
  const coordOf = (id: string): Point | null => NODE_COORDS[id] ?? null;

  const selectedEdge = edges.find((edge) => edge.edge_id === selectedEdgeId) ?? null;
  const emphasizedNodes = useMemo(() => {
    const set = new Set<string>();
    if (selectedEdge) {
      set.add(selectedEdge.from);
      set.add(selectedEdge.to);
    }
    if (selectedNodeId) set.add(selectedNodeId);
    return set;
  }, [selectedEdge, selectedNodeId]);

  return (
    <svg
      viewBox={`0 0 ${GRAPH_VIEWBOX.width} ${GRAPH_VIEWBOX.height}`}
      preserveAspectRatio="xMidYMid meet"
      style={{ width: "100%", height: "100%", display: "block" }}
      role="img"
      aria-label="원인 분석 그래프"
    >
      <defs>
        {ARROW_COLORS.map((color) => (
          <marker
            key={color}
            id={arrowId(color)}
            viewBox="0 0 10 10"
            refX="9"
            refY="5"
            markerWidth="7"
            markerHeight="7"
            orient="auto-start-reverse"
          >
            <path d="M0 0 L10 5 L0 10 z" fill={color} />
          </marker>
        ))}
      </defs>

      {edges.map((edge) => {
        const from = coordOf(edge.from);
        const to = coordOf(edge.to);
        if (!from || !to) return null;

        const start = boundaryPoint(from, to);
        const end = boundaryPoint(to, from);
        const stroke = verdictStroke(edge.verdict);
        const active = edge.edge_id === selectedEdgeId;
        const hovered = edge.edge_id === hoverEdgeId;
        const width = verdictWidth(edge.verdict, edge.confidence) + (hovered || active ? 1.4 : 0);
        const mid = { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 };

        return (
          <Fragment key={edge.edge_id}>
            {/* 클릭·hover 판정용 투명 히트 영역 — 얇은 선을 정확히 집기 어렵다. */}
            <line
              x1={start.x}
              y1={start.y}
              x2={end.x}
              y2={end.y}
              stroke="transparent"
              strokeWidth={14}
              style={{ cursor: "pointer" }}
              onClick={() => onSelectEdge(edge.edge_id)}
              onMouseEnter={() => onHoverEdge(edge.edge_id)}
              onMouseLeave={() => onHoverEdge(null)}
            />
            <line
              x1={start.x}
              y1={start.y}
              x2={end.x}
              y2={end.y}
              stroke={stroke.color}
              strokeWidth={width}
              strokeDasharray={stroke.dash}
              opacity={active ? 1 : stroke.opacity}
              markerEnd={stroke.arrow ? `url(#${arrowId(stroke.color)})` : undefined}
              pointerEvents="none"
            />
            {stroke.cross && (
              <g pointerEvents="none" opacity={0.7}>
                <path
                  d={`M${mid.x - 5} ${mid.y - 5} L${mid.x + 5} ${mid.y + 5} M${mid.x + 5} ${mid.y - 5} L${mid.x - 5} ${mid.y + 5}`}
                  stroke={stroke.color}
                  strokeWidth={1.6}
                />
              </g>
            )}
            {(active || hovered) && hasDirection(edge.sign) && (
              <g pointerEvents="none">
                <rect x={mid.x - 11} y={mid.y - 11} width={22} height={22} rx={6} fill="#1E1E1E" />
                <text
                  x={mid.x}
                  y={mid.y + 4}
                  textAnchor="middle"
                  fill="#fff"
                  fontSize={12}
                  fontWeight={700}
                >
                  {directionGlyph(edge.sign)}
                </text>
              </g>
            )}
          </Fragment>
        );
      })}

      {nodes.map((node) => {
        const coord = coordOf(node.node_id);
        if (!coord) return null;
        return (
          <GraphNodeShape
            key={node.node_id}
            node={node}
            coord={coord}
            emphasized={emphasizedNodes.has(node.node_id)}
          />
        );
      })}
    </svg>
  );
}

function GraphNodeShape({
  node,
  coord,
  emphasized,
}: {
  node: GraphNode;
  coord: Point;
  emphasized: boolean;
}) {
  const tone = stateTone(node.node_state);
  const colored = node.node_state === "알림" || node.node_state === "관찰";

  // 개입 노드의 Primary 표기는 **타입 표식**이고, 상태가 붙으면 상태 토큰이 이긴다(08 규칙 4).
  const typeIsIntervention = node.node_type === "intervention";
  const fill = colored ? tone.fill : typeIsIntervention ? "#F1F2FE" : tone.fill;
  const stroke = colored ? tone.dot : typeIsIntervention ? "#7181F8" : tone.dot;
  const textColor = colored ? tone.text : typeIsIntervention ? "#4B52A8" : "var(--ont-ink)";

  const strokeWidth = emphasized ? 2 : node.node_id === "sales_total" ? 1.6 : 1.2;
  const strokeColor = emphasized ? "#1E1E1E" : stroke;
  const labelSize = node.node_id === "sales_total" ? 13 : node.name.length > 8 ? 11 : 12;
  const labelWeight = node.node_id === "sales_total" ? 700 : 500;

  const shared = {
    fill,
    stroke: strokeColor,
    strokeWidth,
  };

  switch (node.node_type) {
    case "organic": {
      const words = splitLabel(node.name);
      return (
        <g>
          <circle cx={coord.x} cy={coord.y} r={30} {...shared} />
          {words.map((line, index) => (
            <text
              key={line}
              x={coord.x}
              y={coord.y + 4 + (index - (words.length - 1) / 2) * 12}
              textAnchor="middle"
              fontSize={10}
              fontWeight={500}
              fill={textColor}
            >
              {line}
            </text>
          ))}
        </g>
      );
    }
    case "exogenous":
      return (
        <g>
          <polygon
            points={`${coord.x},${coord.y - 26} ${coord.x + 62},${coord.y} ${coord.x},${coord.y + 26} ${coord.x - 62},${coord.y}`}
            {...shared}
          />
          <text x={coord.x} y={coord.y + 4} textAnchor="middle" fontSize={labelSize} fill={textColor}>
            {node.name}
          </text>
        </g>
      );
    case "attribute":
      return (
        <g>
          <polygon
            points={`${coord.x - 46},${coord.y - 20} ${coord.x + 46},${coord.y - 20} ${coord.x + 66},${coord.y} ${coord.x + 46},${coord.y + 20} ${coord.x - 46},${coord.y + 20} ${coord.x - 66},${coord.y}`}
            {...shared}
            fill={colored ? fill : "#F5F6F8"}
          />
          <text x={coord.x} y={coord.y + 4} textAnchor="middle" fontSize={10} fill={textColor}>
            {node.name}
          </text>
        </g>
      );
    case "unobserved":
      return (
        <g>
          <circle
            cx={coord.x}
            cy={coord.y}
            r={26}
            fill="var(--ont-unobserved-fill)"
            stroke="var(--ont-unobserved)"
            strokeWidth={strokeWidth}
            strokeDasharray="3 2.5"
          />
          <text
            x={coord.x}
            y={coord.y + 5}
            textAnchor="middle"
            fontSize={15}
            fontWeight={700}
            fill="var(--ont-unobserved-text)"
          >
            ?
          </text>
          <text
            x={coord.x}
            y={coord.y + 42}
            textAnchor="middle"
            fontSize={10}
            fill="var(--ont-unobserved-text)"
          >
            {node.name}
          </text>
        </g>
      );
    case "intervention":
    case "kpi":
    default:
      return (
        <g>
          <rect
            x={coord.x - 69}
            y={coord.y - 18}
            width={138}
            height={36}
            rx={node.node_type === "kpi" ? 18 : 3}
            {...shared}
          />
          <text
            x={coord.x}
            y={coord.y + 4}
            textAnchor="middle"
            fontSize={labelSize}
            fontWeight={labelWeight}
            fill={textColor}
          >
            {node.name}
          </text>
        </g>
      );
  }
}

function splitLabel(label: string): string[] {
  const parts = label.split(" ");
  if (parts.length < 2) return [label];
  const half = Math.ceil(parts.length / 2);
  return [parts.slice(0, half).join(" "), parts.slice(half).join(" ")];
}

/**
 * 범례 — 좌하단 고정 오버레이. **개수는 응답 `counts` 파생이다**(디자인 03 · 08 규칙 7).
 */
export function GraphLegend({ counts }: { counts: Record<string, number> }) {
  return (
    <div
      style={{
        position: "absolute",
        left: 16,
        bottom: 16,
        background: "rgba(255,255,255,0.94)",
        borderRadius: 10,
        border: "1px solid var(--ont-border)",
        padding: "12px 14px",
        display: "flex",
        flexDirection: "column",
        gap: 8,
        pointerEvents: "none",
      }}
    >
      <div style={{ display: "flex", gap: 14, flexWrap: "wrap" }}>
        {VERDICT_ORDER.map((verdict) => (
          <LegendVerdict key={verdict} verdict={verdict} count={counts[verdict] ?? 0} />
        ))}
      </div>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        {NODE_TYPE_ORDER.map((type) => (
          <span key={type} style={{ fontSize: 11, color: "var(--ont-body)" }}>
            {NODE_TYPE_LABEL[type]}
          </span>
        ))}
        <span style={{ fontSize: 11, color: "var(--ont-muted)" }}>
          색 = 상태 · 모양 = 타입 · 선 = 판정 · 굵기 = 채택 신뢰도
        </span>
      </div>
    </div>
  );
}

function LegendVerdict({ verdict, count }: { verdict: Verdict; count: number }) {
  const stroke = verdictStroke(verdict);
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 6, fontSize: 11 }}>
      <svg width="22" height="8" aria-hidden>
        <line
          x1="0"
          y1="4"
          x2="22"
          y2="4"
          stroke={stroke.color}
          strokeWidth={verdictWidth(verdict, verdict === "채택" ? "중간" : null)}
          strokeDasharray={stroke.dash}
          opacity={stroke.opacity}
        />
      </svg>
      <span style={{ color: "var(--ont-body)" }}>{verdict}</span>
      <span className="ont-mono" style={{ color: "var(--ont-muted)" }}>
        {count}
      </span>
    </span>
  );
}
