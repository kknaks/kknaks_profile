"use client";

import Link from "next/link";
import { useState } from "react";
import type { ProjectItem, ProjectsResponse } from "@/lib/types";

import { StatusTag } from "./status-tag";

export function ProjectsGrid({ projects }: { projects: ProjectsResponse }) {
  const items = projects["projects[]"];
  const cats = projects.projects?.categories ?? [];
  const [active, setActive] = useState<string>("all");

  // `started_on DESC` — 정렬은 컬럼이 아니라 날짜에서 나온다.
  const sorted = [...items].sort((a, b) =>
    (b.startedOn ?? "").localeCompare(a.startedOn ?? ""),
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
          {"전체"}{" "}
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
          eyebrow={"완성된 것"}
          count={doneList.length}
          items={doneList}
        />
      )}
      {wipList.length > 0 && (
        <Group
          eyebrow={"만들고 있는 것"}
          count={wipList.length}
          items={wipList}
          marginTop={doneList.length > 0 ? 40 : 0}
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
}: {
  eyebrow: string;
  count: number;
  items: ProjectItem[];
  marginTop?: number;
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
          <ProjectCard key={p.slug} p={p} />
        ))}
      </div>
    </div>
  );
}

function ProjectCard({ p }: { p: ProjectItem }) {
  const [imgError, setImgError] = useState(false);
  const showImg = !!p.thumbnail && !imgError;

  return (
    <Link
      href={`/projects/${p.slug}`}
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
              {p.slug}
            </span>
            <StatusTag s={p.status} />
            {p.startedOn && (
              <span
                className="mono"
                style={{
                  fontSize: 10,
                  color: "var(--fg-3)",
                  marginLeft: "auto",
                }}
              >
                {p.startedOn}
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
