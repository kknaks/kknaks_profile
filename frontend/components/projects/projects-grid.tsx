"use client";

import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import type { Lang } from "@/lib/i18n";
import type { ProjectItem, ProjectsResponse } from "@/lib/types";

const STATUS_COLOR: Record<string, string> = {
  live: "var(--accent)",
  wip: "var(--info)",
  archived: "var(--fg-3)",
};

function StatusTag({ s }: { s: ProjectItem["status"] }) {
  const isLive = s === "live";
  return (
    <span
      className="tag"
      style={{
        fontSize: 9,
        padding: "1px 6px",
        ...(isLive
          ? {
              color: "var(--accent)",
              background: "var(--accent-soft)",
              borderColor: "var(--accent-line)",
            }
          : {}),
      }}
    >
      <span className="tag-dot" style={{ background: STATUS_COLOR[s], width: 4, height: 4 }} />
      {s}
    </span>
  );
}

export function ProjectsGrid({
  projects,
  lang,
}: {
  projects: ProjectsResponse;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const items = projects["projects[]"];
  const cats = projects.projects.categories;
  const [active, setActive] = useState<string>("all");
  const [selected, setSelected] = useState<ProjectItem | null>(null);

  useEffect(() => {
    if (!selected) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setSelected(null);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [selected]);

  const sorted = [...items].sort((a, b) =>
    (b.date ?? "").localeCompare(a.date ?? ""),
  );
  const filtered = active === "all" ? sorted : sorted.filter((p) => p.category === active);
  const wipList = filtered.filter((p) => p.status === "wip");
  const doneList = filtered.filter((p) => p.status !== "wip");

  return (
    <>
      <div
        style={{
          display: "flex",
          gap: 8,
          marginBottom: 24,
          alignItems: "center",
          flexWrap: "wrap",
        }}
      >
        <span className="caps">filter</span>
        <button
          type="button"
          onClick={() => setActive("all")}
          className={active === "all" ? "btn" : "btn ghost"}
          style={{ padding: "4px 10px", fontSize: 11 }}
        >
          {t("전체", "All")}{" "}
          <span style={{ color: "var(--fg-3)", marginLeft: 4 }}>
            {items.length}
          </span>
        </button>
        {cats.map((c) => (
          <button
            key={c.id}
            type="button"
            onClick={() => setActive(c.id)}
            className={active === c.id ? "btn" : "btn ghost"}
            style={{ padding: "4px 10px", fontSize: 11 }}
          >
            {c.label}{" "}
            <span style={{ color: "var(--fg-3)", marginLeft: 4 }}>
              {c.count}
            </span>
          </button>
        ))}
        <span
          className="mono"
          style={{ marginLeft: "auto", fontSize: 11, color: "var(--fg-3)" }}
        >
          sorted by date ↓
        </span>
      </div>

      {wipList.length > 0 && (
        <Group
          eyebrow={t("만들고 있는 것", "in progress")}
          count={wipList.length}
          items={wipList}
          onSelect={setSelected}
        />
      )}
      {doneList.length > 0 && (
        <Group
          eyebrow={t("완성된 것", "done")}
          count={doneList.length}
          items={doneList}
          marginTop={wipList.length > 0 ? 40 : 0}
          onSelect={setSelected}
        />
      )}

      <ProjectPanel selected={selected} onClose={() => setSelected(null)} lang={lang} />
    </>
  );
}

function Group({
  eyebrow,
  count,
  items,
  marginTop = 0,
  onSelect,
}: {
  eyebrow: string;
  count: number;
  items: ProjectItem[];
  marginTop?: number;
  onSelect: (p: ProjectItem) => void;
}) {
  return (
    <div style={{ marginTop }}>
      <div
        className="mono"
        style={{
          fontSize: 11,
          color: "var(--accent)",
          marginBottom: 12,
          display: "flex",
          alignItems: "baseline",
          gap: 8,
        }}
      >
        // {eyebrow}
        <span style={{ color: "var(--fg-3)" }}>{count}</span>
      </div>
      <div
        className="projects-grid m-stack"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 12,
        }}
      >
        <style>{`
          @media (max-width: 1024px) {
            .projects-grid { grid-template-columns: repeat(2, 1fr) !important; }
          }
        `}</style>
        {items.map((p) => (
          <ProjectCard key={p.id} p={p} onSelect={onSelect} />
        ))}
      </div>
    </div>
  );
}

function ProjectCard({
  p,
  onSelect,
}: {
  p: ProjectItem;
  onSelect: (p: ProjectItem) => void;
}) {
  return (
    <article
      className="card"
      onClick={() => onSelect(p)}
      style={{
        overflow: "hidden",
        cursor: "pointer",
        transition: "border-color 120ms",
      }}
    >
      <div
        className="placeholder-hatch"
        style={{ aspectRatio: "16/9", fontSize: 10 }}
      >
        [ {p.title} ]
      </div>
      <div style={{ padding: 12, borderTop: "1px solid var(--line-1)" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            marginBottom: 6,
          }}
        >
          <span className="mono" style={{ fontSize: 10, color: "var(--fg-3)" }}>
            {p.id}
          </span>
          <StatusTag s={p.status} />
          {p.date && (
            <span
              className="mono"
              style={{
                fontSize: 10,
                color: "var(--fg-3)",
                marginLeft: "auto",
              }}
            >
              {p.date}
            </span>
          )}
        </div>
        <h3
          style={{
            margin: "0 0 4px",
            fontSize: 13,
            letterSpacing: "-0.01em",
            fontWeight: 500,
          }}
        >
          {p.title}
        </h3>
        <p
          style={{
            margin: "0 0 8px",
            fontSize: 11,
            color: "var(--fg-2)",
            lineHeight: 1.5,
          }}
        >
          {p.summary}
        </p>
        {p.stack && p.stack.length > 0 && (
          <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
            {p.stack.slice(0, 4).map((s) => (
              <span
                key={s}
                className="tag"
                style={{ fontSize: 9, padding: "1px 5px" }}
              >
                {s}
              </span>
            ))}
          </div>
        )}
      </div>
    </article>
  );
}

function ProjectPanel({
  selected,
  onClose,
  lang,
}: {
  selected: ProjectItem | null;
  onClose: () => void;
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);
  const open = selected !== null;

  return (
    <>
      {open && (
        <div
          onClick={onClose}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.6)",
            zIndex: 50,
            transition: "opacity 200ms",
          }}
        />
      )}
      <aside
        style={{
          position: "fixed",
          top: 0,
          right: 0,
          height: "100vh",
          width: "min(460px, 100vw)",
          background: "var(--bg-1)",
          borderLeft: "1px solid var(--line-1)",
          boxShadow: "var(--shadow-pop)",
          zIndex: 51,
          transform: open ? "translateX(0)" : "translateX(100%)",
          transition: "transform 240ms var(--ease)",
          overflowY: "auto",
          padding: "24px 28px 48px",
        }}
      >
        {selected && (
          <>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginBottom: 16,
              }}
            >
              <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                {selected.id}
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
                  lineHeight: 1,
                }}
              >
                ✕
              </button>
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                marginBottom: 8,
                flexWrap: "wrap",
              }}
            >
              <StatusTag s={selected.status} />
              {selected.date && (
                <span
                  className="mono"
                  style={{ fontSize: 11, color: "var(--fg-3)" }}
                >
                  {selected.date}
                </span>
              )}
            </div>

            <h2
              style={{
                margin: "0 0 8px",
                fontSize: 24,
                fontWeight: 600,
                letterSpacing: "-0.01em",
              }}
            >
              {selected.title}
            </h2>
            <p
              style={{
                margin: "0 0 16px",
                fontSize: 14,
                color: "var(--fg-1)",
                lineHeight: 1.65,
              }}
            >
              {selected.summary}
            </p>

            {selected.stack && selected.stack.length > 0 && (
              <div
                style={{
                  display: "flex",
                  gap: 6,
                  flexWrap: "wrap",
                  marginBottom: 16,
                }}
              >
                {selected.stack.map((s) => (
                  <span key={s} className="tag">
                    {s}
                  </span>
                ))}
              </div>
            )}

            {selected.links && (selected.links.repo || selected.links.live) && (
              <div
                style={{
                  display: "flex",
                  gap: 12,
                  marginBottom: 24,
                  fontSize: 12,
                }}
              >
                {selected.links.repo && (
                  <a
                    href={selected.links.repo.startsWith("http") ? selected.links.repo : `https://${selected.links.repo}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mono"
                    style={{ color: "var(--fg-2)" }}
                  >
                    repo ↗
                  </a>
                )}
                {selected.links.live && (
                  <a
                    href={selected.links.live.startsWith("http") ? selected.links.live : `https://${selected.links.live}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mono"
                    style={{ color: "var(--accent)" }}
                  >
                    live ↗
                  </a>
                )}
              </div>
            )}

            {selected.body && selected.body.trim().length > 0 ? (
              <div style={{ borderTop: "1px solid var(--line-1)", paddingTop: 20 }}>
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => (
                      <h2 style={{ fontSize: 18, fontWeight: 600, margin: "0 0 12px" }}>{children}</h2>
                    ),
                    h2: ({ children }) => (
                      <h3 style={{ fontSize: 14, fontWeight: 500, color: "var(--fg-0)", marginTop: 18, marginBottom: 8 }}>{children}</h3>
                    ),
                    h3: ({ children }) => (
                      <h4 style={{ fontSize: 13, fontWeight: 500, color: "var(--fg-1)", marginTop: 14, marginBottom: 6 }}>{children}</h4>
                    ),
                    p: ({ children }) => (
                      <p style={{ fontSize: 13, lineHeight: 1.7, color: "var(--fg-1)", margin: "0 0 10px" }}>{children}</p>
                    ),
                    ul: ({ children }) => (
                      <ul style={{ fontSize: 13, lineHeight: 1.7, color: "var(--fg-1)", paddingLeft: 18, margin: "0 0 10px" }}>{children}</ul>
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
                    a: ({ href, children }) => (
                      <a href={href} target="_blank" rel="noopener noreferrer" style={{ color: "var(--accent)" }}>
                        {children}
                      </a>
                    ),
                  }}
                >
                  {selected.body}
                </ReactMarkdown>
              </div>
            ) : (
              <div
                className="mono"
                style={{
                  borderTop: "1px solid var(--line-1)",
                  paddingTop: 20,
                  fontSize: 12,
                  color: "var(--fg-3)",
                }}
              >
                // {t("본문 — 추후 추가", "body — coming soon")}
              </div>
            )}
          </>
        )}
      </aside>
    </>
  );
}
