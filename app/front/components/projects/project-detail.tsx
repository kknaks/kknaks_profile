import Link from "next/link";
import ReactMarkdown, { defaultUrlTransform } from "react-markdown";

import { assetUrl } from "@/lib/api";
import type { Neighbor, ProjectItem } from "@/lib/types";

import { StatusTag } from "./status-tag";

export function ProjectDetail({
  item,
  newer,
  older,
}: {
  item: ProjectItem;
  newer: Neighbor | null;
  older: Neighbor | null;
}) {

  return (
    <>
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "40px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <Link
          href="/projects"
          className="mono"
          style={{
            color: "var(--fg-3)",
            fontSize: 12,
            textDecoration: "none",
            display: "inline-block",
            marginBottom: 20,
          }}
        >
          ← {"전체 프로젝트"}
        </Link>

        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
            display: "flex",
            alignItems: "center",
            gap: 12,
            flexWrap: "wrap",
          }}
        >
          <span>{item.slug}</span>
          <StatusTag s={item.status} />
          {item.startedOn && <span>{item.startedOn}</span>}
        </div>

        <h1
          className="m-h1"
          style={{
            fontSize: 40,
            lineHeight: 1.15,
            letterSpacing: "-0.02em",
            margin: 0,
            fontWeight: 600,
            maxWidth: 900,
          }}
        >
          {item.title}
        </h1>
        <p
          style={{
            margin: "16px 0 0",
            color: "var(--fg-1)",
            fontSize: 15,
            lineHeight: 1.65,
            maxWidth: 760,
          }}
        >
          {item.summary}
        </p>

        {item.stack && item.stack.length > 0 && (
          <div
            style={{
              display: "flex",
              gap: 6,
              flexWrap: "wrap",
              marginTop: 20,
            }}
          >
            {item.stack.map((s) => (
              <span key={s} className="tag">
                {s}
              </span>
            ))}
          </div>
        )}

        {item.links && (item.links.repo || item.links.site) && (
          <div
            style={{
              display: "flex",
              gap: 12,
              marginTop: 16,
              fontSize: 12,
            }}
          >
            {item.links.repo && (
              <a
                href={ensureHttp(item.links.repo)}
                target="_blank"
                rel="noopener noreferrer"
                className="mono"
                style={{ color: "var(--fg-2)" }}
              >
                repo ↗
              </a>
            )}
            {item.links.site && (
              <a
                href={ensureHttp(item.links.site)}
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
      </header>

      <section className="pad-x" style={{ padding: "48px 80px 32px" }}>
        {item.body && item.body.trim().length > 0 ? (
          <article className="contents-body" style={{ maxWidth: 900 }}>
            {/* 이미지 상대참조(assets/…)는 원장(showcase.md) 디렉토리 기준이다 —
                para 를 서빙하는 백엔드 /api/assets 로 풀어 준다. */}
            <ReactMarkdown
              urlTransform={(url, key) =>
                key === "src" && !/^(https?:|data:|\/)/.test(url)
                  ? assetUrl(
                      `para/projects/summer-star/${item.slug}/${url.replace(/^\.\//, "")}`,
                    )
                  : defaultUrlTransform(url)
              }
            >
              {item.body}
            </ReactMarkdown>
          </article>
        ) : (
          <div
            className="mono"
            style={{ fontSize: 12, color: "var(--fg-3)" }}
          >
            // {"본문 — 추후 추가"}
          </div>
        )}
      </section>

      <ProjectPrevNext
        newer={newer}
        older={older}
      />
    </>
  );
}

function ensureHttp(url: string) {
  return url.startsWith("http") ? url : `https://${url}`;
}

function ProjectPrevNext({
  newer,
  older,
}: {
  newer: Neighbor | null;
  older: Neighbor | null;
}) {
  return (
    <nav
      className="pad-x m-stack"
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: 16,
        padding: "32px 80px 64px",
        borderTop: "1px solid var(--line-1)",
      }}
    >
      {newer ? (
        <Link
          href={`/projects/${newer.slug}`}
          className="card"
          style={{
            padding: "20px 24px",
            textAlign: "left",
            background: "var(--bg-1)",
            border: "1px solid var(--line-1)",
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <div
            className="mono"
            style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}
          >
            ← {"최신"}
          </div>
          <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{newer.title}</div>
        </Link>
      ) : (
        <div />
      )}
      {older ? (
        <Link
          href={`/projects/${older.slug}`}
          className="card"
          style={{
            padding: "20px 24px",
            textAlign: "right",
            background: "var(--bg-1)",
            border: "1px solid var(--line-1)",
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <div
            className="mono"
            style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}
          >
            {"이전"} →
          </div>
          <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{older.title}</div>
        </Link>
      ) : (
        <div />
      )}
    </nav>
  );
}
