"use client";

import { forceX, forceY } from "d3-force";
import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import type { Lang } from "@/lib/i18n";
import type { NoteDetail, NotesGraphResponse } from "@/lib/types";

// SSR 회피 — useEffect 안에서 lazy import. ref 정상 forwarding.
type FGComponent = React.ComponentType<Record<string, unknown> & { ref?: unknown }>;

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:48000";

export function NotesGraphView({
  graphData,
  lang,
}: {
  graphData: NotesGraphResponse["notes"];
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const [activeGroup, setActiveGroup] = useState<string>("all");
  const [activeStack, setActiveStack] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
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

  // d3Force tuning + reheat + zoomToFit
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
    charge?.strength?.(-40);
    const link = fg.d3Force("link");
    link?.distance?.(22);
    link?.strength?.(1);
    fg.d3Force("center-x", forceX(0).strength(0.15));
    fg.d3Force("center-y", forceY(0).strength(0.15));
    // force 추가/변경했으니 시뮬레이션 reheat (alpha=1 로 재시작)
    fg.d3ReheatSimulation?.();
    // 시뮬레이션 후 zoomToFit
    const t1 = setTimeout(() => fg.zoomToFit?.(400, 30), 1500);
    const t2 = setTimeout(() => fg.zoomToFit?.(400, 30), 3000);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [activeStack, searchQuery, graphData, ForceGraph2D]);

  useEffect(() => {
    if (!detail) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setDetail(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [detail]);

  const colorByGroup = useMemo(() => {
    const map: Record<string, string> = {};
    graphData.graph.clusters.forEach((c) => {
      if (c.color) map[c.id] = c.color;
    });
    return map;
  }, [graphData]);

  const groupCounts = useMemo(() => {
    const m: Record<string, number> = {};
    graphData.graph.nodes.forEach((n) => {
      const g = n.group ?? "_";
      m[g] = (m[g] ?? 0) + 1;
    });
    return m;
  }, [graphData]);

  const filtered = useMemo(() => {
    // 1. 필터링된 노트 노드
    let noteNodes = graphData.graph.nodes;
    if (activeGroup !== "all") {
      noteNodes = noteNodes.filter((n) => n.group === activeGroup);
    }
    if (activeStack) {
      noteNodes = noteNodes.filter((n) => n.stack?.includes(activeStack));
    }
    if (searchQuery.trim()) {
      const q = searchQuery.trim().toLowerCase();
      noteNodes = noteNodes.filter((n) =>
        (n.title ?? "").toLowerCase().includes(q),
      );
    }
    const noteIds = new Set(noteNodes.map((n) => n.id));

    // 2. 노트 간 link (frontmatter `links` 기반 edges)
    const linkEnd = (v: unknown): string =>
      typeof v === "object" && v !== null && "id" in v
        ? String((v as { id: string | number }).id)
        : String(v);
    const noteLinks = graphData.graph.edges
      .filter(
        (e) => noteIds.has(linkEnd(e.source)) && noteIds.has(linkEnd(e.target)),
      )
      .map((e) => ({ source: linkEnd(e.source), target: linkEnd(e.target) }));

    // 3. 보이는 노트들이 사용한 stack 모음
    const usedStacks = new Set<string>();
    noteNodes.forEach((n) => {
      n.stack?.forEach((s) => usedStacks.add(s));
    });

    // 4. stack hub 노드 합성 — 보이는 stack만
    const stackById: Record<string, { name: string; count: number }> = {};
    graphData.stacks.forEach((s) => {
      stackById[s.name] = s;
    });
    const stackNodes = Array.from(usedStacks).map((name) => ({
      id: `__stack__${name}`,
      title: name,
      type: "stack" as const,
      stackName: name,
      count: stackById[name]?.count ?? 0,
    }));

    // 5. 노트 → stack edges
    const stackLinks: { source: string; target: string }[] = [];
    noteNodes.forEach((n) => {
      n.stack?.forEach((s) => {
        if (usedStacks.has(s)) {
          stackLinks.push({ source: n.id, target: `__stack__${s}` });
        }
      });
    });

    return {
      nodes: [
        ...noteNodes.map((n) => ({ ...n, type: "note" as const })),
        ...stackNodes,
      ],
      links: [...noteLinks, ...stackLinks],
    };
  }, [graphData, activeGroup, activeStack, searchQuery]);

  async function onNodeClick(node: { id?: string | number; type?: string; stackName?: string }) {
    if (!node.id) return;
    // stack hub 노드 클릭 → stack 필터 적용
    if (node.type === "stack" && node.stackName) {
      setActiveStack(activeStack === node.stackName ? null : node.stackName);
      return;
    }
    // 노트 노드 클릭 → detail 패널
    setLoadingDetail(true);
    try {
      const id = encodeURIComponent(String(node.id));
      const url = `${API_BASE}/api/notes/${id}?lang=${lang}`;
      console.log("[notes] fetch detail:", node.id, "→", url);
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      setDetail(data["notes.detail"]);
    } catch (err) {
      console.error("[notes] detail fetch failed:", err);
      setDetail(null);
    } finally {
      setLoadingDetail(false);
    }
  }

  return (
    <div
      className="pad-x notes-main"
      style={{
        padding: "24px 80px 24px",
        display: "grid",
        gridTemplateColumns: "220px 1fr",
        gap: 16,
        height: "calc(100vh - 180px)",
        minHeight: 600,
      }}
    >
      <style>{`
        @media (max-width: 720px) {
          .notes-main { grid-template-columns: 1fr !important; }
          .notes-sidebar { display: none !important; }
          .notes-graph-area { grid-template-columns: 1fr !important; }
          .notes-graph-area > .notes-graph { ${detail || loadingDetail ? "display: none;" : ""} }
        }
      `}</style>
      {/* sidebar — 데스크탑 항상 보임, 모바일 hide */}
      <aside
        className="notes-sidebar"
        style={{
          border: "1px solid var(--line-1)",
          borderRadius: 6,
          background: "var(--bg-1)",
          padding: "16px 12px",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder={t("search — title", "search — title")}
          style={{
            padding: "6px 10px",
            background: "var(--bg-2)",
            border: "1px solid var(--line-2)",
            borderRadius: 4,
            color: "var(--fg-0)",
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            outline: "none",
          }}
        />

        <div className="caps" style={{ marginTop: 4 }}>
          {t("기술 스택", "tech stack")}
        </div>

        <button
          type="button"
          onClick={() => setActiveStack(null)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            width: "100%",
            padding: "5px 8px",
            background: activeStack === null ? "var(--bg-2)" : "transparent",
            border: "none",
            borderLeft:
              activeStack === null
                ? "2px solid var(--accent)"
                : "2px solid transparent",
            color: activeStack === null ? "var(--fg-0)" : "var(--fg-2)",
            fontFamily: "var(--font-mono)",
            fontSize: 11,
            cursor: "pointer",
            textAlign: "left",
          }}
        >
          <span style={{ flex: 1 }}>{t("전체보기", "All")}</span>
          <span style={{ color: "var(--fg-3)" }}>
            {graphData.totalCount}
          </span>
        </button>

        {graphData.stacks.map((s) => {
          const isActive = activeStack === s.name;
          return (
            <button
              key={s.name}
              type="button"
              onClick={() => setActiveStack(isActive ? null : s.name)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                width: "100%",
                padding: "5px 8px",
                background: isActive ? "var(--bg-2)" : "transparent",
                border: "none",
                borderLeft: isActive
                  ? "2px solid oklch(0.82 0.13 80)"
                  : "2px solid transparent",
                color: isActive ? "var(--fg-0)" : "var(--fg-2)",
                fontFamily: "var(--font-mono)",
                fontSize: 11,
                cursor: "pointer",
                textAlign: "left",
              }}
            >
              <span
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: "50%",
                  background: "oklch(0.82 0.13 80)",
                  opacity: isActive ? 1 : 0.6,
                  flexShrink: 0,
                }}
              />
              <span
                style={{
                  flex: 1,
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                {s.name}
              </span>
              <span style={{ color: "var(--fg-3)" }}>{s.count}</span>
            </button>
          );
        })}
      </aside>

      {/* 그래프 + panel 단일 박스 안 split — 가운데 borderLeft 로만 분리 */}
      <div
        className="notes-graph-area"
        style={{
          display: "grid",
          gridTemplateColumns:
            detail || loadingDetail ? "1fr 3fr" : "1fr",
          gap: 0,
          border: "1px solid var(--line-1)",
          borderRadius: 6,
          overflow: "hidden",
          background: "var(--bg-1)",
          minHeight: 500,
        }}
      >
      <div
        ref={containerRef}
        className="notes-graph"
        style={{
          position: "relative",
          overflow: "hidden",
          minHeight: 500,
        }}
      >
        {ForceGraph2D ? (
          <ForceGraph2D
            ref={fgRef as never}
            graphData={filtered}
            width={size.w}
            height={size.h}
            nodeId="id"
            nodeLabel={(n: object) => (n as { title?: string }).title ?? ""}
            nodeColor={(n: object) => {
              const node = n as { type?: string };
              return node.type === "stack"
                ? "oklch(0.82 0.13 80)"
                : "oklch(0.78 0.14 145)";
            }}
            nodeVal={() => 1}
            nodeRelSize={3}
            linkColor={() => "rgba(255,255,255,0.12)"}
            linkWidth={0.6}
            backgroundColor="transparent"
            onNodeClick={onNodeClick}
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
            // loading graph...
          </div>
        )}
        {/* 범례 — 좌측 상단 */}
        <div
          className="mono"
          style={{
            position: "absolute",
            top: 12,
            left: 16,
            display: "flex",
            gap: 14,
            fontSize: 11,
            color: "var(--fg-2)",
            pointerEvents: "none",
          }}
        >
          <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: "oklch(0.82 0.13 80)",
              }}
            />
            Tech Stack
          </span>
          <span style={{ color: "var(--fg-3)" }}>·</span>
          <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: "oklch(0.78 0.14 145)",
              }}
            />
            Note
          </span>
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
          {filtered.nodes.length} nodes · {filtered.links.length} edges
        </div>
      </div>

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

function NavButton({
  label,
  count,
  color,
  active,
  onClick,
}: {
  label: string;
  count: number;
  color?: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 8,
        width: "100%",
        padding: "6px 8px",
        background: active ? "var(--bg-2)" : "transparent",
        border: "none",
        borderLeft: active
          ? "2px solid var(--accent)"
          : "2px solid transparent",
        color: active ? "var(--fg-0)" : "var(--fg-2)",
        fontFamily: "var(--font-mono)",
        fontSize: 12,
        cursor: "pointer",
        textAlign: "left",
        transition: "background 80ms",
      }}
    >
      {color && (
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: color,
            flexShrink: 0,
          }}
        />
      )}
      <span style={{ flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
        {label}
      </span>
      <span style={{ color: "var(--fg-3)", fontSize: 11 }}>{count}</span>
    </button>
  );
}

function NoteDetailPanel({
  detail,
  loading,
  onClose,
  lang,
}: {
  detail: NoteDetail | null;
  loading: boolean;
  onClose: () => void;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  if (!detail && !loading) return null;

  return (
    <aside
      style={{
        borderLeft: "1px solid var(--line-1)",
        background: "var(--bg-2)",
        overflowY: "auto",
        padding: "24px 28px 48px",
      }}
    >
        {loading && !detail && (
          <div
            className="mono"
            style={{ color: "var(--fg-3)", fontSize: 12 }}
          >
            // loading...
          </div>
        )}
        {detail && (
          <>
            <div style={{ display: "flex", alignItems: "center", marginBottom: 16 }}>
              <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                {detail.id}
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
                  width: 28,
                  height: 28,
                  color: "var(--fg-2)",
                  cursor: "pointer",
                  fontSize: 14,
                }}
              >
                ✕
              </button>
            </div>

            {detail.date && (
              <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 8 }}>
                {detail.date}
              </div>
            )}
            <h2 style={{ margin: "0 0 12px", fontSize: 22, fontWeight: 600, letterSpacing: "-0.01em" }}>
              {detail.title}
            </h2>

            {detail.stack && detail.stack.length > 0 && (
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
                {detail.stack.map((s) => (
                  <span
                    key={s}
                    className="tag"
                    style={{
                      fontSize: 11,
                      color: "var(--accent)",
                      background: "var(--accent-soft)",
                      borderColor: "var(--accent-line)",
                    }}
                  >
                    {s}
                  </span>
                ))}
              </div>
            )}

            {detail.tags && detail.tags.length > 0 && (
              <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 16 }}>
                {detail.tags.map((tag) => (
                  <span key={tag} className="tag" style={{ fontSize: 11 }}>
                    {tag.startsWith("#") ? tag : `#${tag}`}
                  </span>
                ))}
              </div>
            )}

            {detail.body && detail.body.trim() ? (
              <div style={{ borderTop: "1px solid var(--line-1)", paddingTop: 18 }}>
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => (
                      <h2 style={{ fontSize: 18, fontWeight: 600, margin: "16px 0 10px" }}>{children}</h2>
                    ),
                    h2: ({ children }) => (
                      <h3 style={{ fontSize: 15, fontWeight: 500, color: "var(--fg-0)", marginTop: 18, marginBottom: 8 }}>
                        {children}
                      </h3>
                    ),
                    h3: ({ children }) => (
                      <h4 style={{ fontSize: 13, fontWeight: 500, color: "var(--fg-1)", marginTop: 14, marginBottom: 6 }}>
                        {children}
                      </h4>
                    ),
                    p: ({ children }) => (
                      <p style={{ fontSize: 13, lineHeight: 1.7, color: "var(--fg-1)", margin: "0 0 10px" }}>
                        {children}
                      </p>
                    ),
                    ul: ({ children }) => (
                      <ul style={{ fontSize: 13, lineHeight: 1.7, color: "var(--fg-1)", paddingLeft: 18, margin: "0 0 10px" }}>
                        {children}
                      </ul>
                    ),
                    ol: ({ children }) => (
                      <ol style={{ fontSize: 13, lineHeight: 1.7, color: "var(--fg-1)", paddingLeft: 18, margin: "0 0 10px" }}>
                        {children}
                      </ol>
                    ),
                    li: ({ children }) => <li style={{ marginBottom: 3 }}>{children}</li>,
                    code: ({ children }) => (
                      <code
                        style={{
                          fontFamily: "var(--font-mono)",
                          fontSize: 11,
                          background: "var(--bg-2)",
                          padding: "1px 6px",
                          borderRadius: 3,
                        }}
                      >
                        {children}
                      </code>
                    ),
                    pre: ({ children }) => (
                      <pre
                        style={{
                          background: "var(--bg-2)",
                          padding: 12,
                          borderRadius: 4,
                          overflowX: "auto",
                          fontSize: 11,
                          margin: "8px 0 12px",
                        }}
                      >
                        {children}
                      </pre>
                    ),
                    a: ({ href, children }) => (
                      <a href={href} target="_blank" rel="noopener noreferrer" style={{ color: "var(--accent)" }}>
                        {children}
                      </a>
                    ),
                    blockquote: ({ children }) => (
                      <blockquote
                        style={{
                          borderLeft: "2px solid var(--line-3)",
                          paddingLeft: 12,
                          color: "var(--fg-2)",
                          margin: "0 0 10px",
                        }}
                      >
                        {children}
                      </blockquote>
                    ),
                    img: ({ src, alt }) => (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={typeof src === "string" ? src : ""}
                        alt={alt ?? ""}
                        style={{
                          maxWidth: "100%",
                          height: "auto",
                          borderRadius: 4,
                          margin: "8px 0",
                        }}
                      />
                    ),
                  }}
                >
                  {detail.body}
                </ReactMarkdown>
              </div>
            ) : (
              <div
                className="mono"
                style={{ borderTop: "1px solid var(--line-1)", paddingTop: 18, color: "var(--fg-3)", fontSize: 12 }}
              >
                // {t("본문 비어있음", "empty body")}
              </div>
            )}

            {detail.backlinks && detail.backlinks.length > 0 && (
              <div style={{ marginTop: 24, borderTop: "1px solid var(--line-1)", paddingTop: 18 }}>
                <div className="mono" style={{ fontSize: 11, color: "var(--accent)", marginBottom: 8 }}>
                  // {t("백링크", "backlinks")} {detail.backlinks.length}
                </div>
                <ul style={{ margin: 0, padding: 0, listStyle: "none", fontSize: 13 }}>
                  {detail.backlinks.map((bl) => (
                    <li key={bl.id} style={{ padding: "4px 0", color: "var(--fg-1)" }}>
                      → {bl.title}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </aside>
  );
}
