"use client";

import Link from "next/link";
import { useState } from "react";
import type { Lang } from "@/lib/i18n";
import type { ProjectItem, ProjectsResponse } from "@/lib/types";

import { StatusTag } from "./status-tag";

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
  const langSuffix = lang === "en" ? "?lang=en" : "";

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

      {doneList.length > 0 && (
        <Group
          eyebrow={t("완성된 것", "done")}
          count={doneList.length}
          items={doneList}
          langSuffix={langSuffix}
        />
      )}
      {wipList.length > 0 && (
        <Group
          eyebrow={t("만들고 있는 것", "in progress")}
          count={wipList.length}
          items={wipList}
          marginTop={doneList.length > 0 ? 40 : 0}
          langSuffix={langSuffix}
        />
      )}
    </>
  );
}

function Group({
  eyebrow,
  count,
  items,
  marginTop = 0,
  langSuffix,
}: {
  eyebrow: string;
  count: number;
  items: ProjectItem[];
  marginTop?: number;
  langSuffix: string;
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
          <ProjectCard key={p.id} p={p} langSuffix={langSuffix} />
        ))}
      </div>
    </div>
  );
}

function ProjectCard({
  p,
  langSuffix,
}: {
  p: ProjectItem;
  langSuffix: string;
}) {
  const [imgError, setImgError] = useState(false);
  const showImg = !!p.thumbnail && !imgError;

  return (
    <Link
      href={`/projects/${p.id}${langSuffix}`}
      className="card"
      style={{
        overflow: "hidden",
        transition: "border-color 120ms",
        textDecoration: "none",
        color: "inherit",
        display: "block",
      }}
    >
      <article>
        {showImg ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={p.thumbnail!}
            alt={`${p.title} cover`}
            style={{
              width: "100%",
              aspectRatio: "16/9",
              objectFit: "cover",
              display: "block",
              background: "var(--bg-2)",
            }}
            onError={() => setImgError(true)}
          />
        ) : (
          <div
            className="placeholder-hatch"
            style={{ aspectRatio: "16/9", fontSize: 10 }}
          >
            [ {p.title} ]
          </div>
        )}
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
    </Link>
  );
}
