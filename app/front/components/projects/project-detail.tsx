import Link from "next/link";
import ReactMarkdown, { defaultUrlTransform } from "react-markdown";
import remarkGfm from "remark-gfm";

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

        <div className="project-head-row">
        <div className="project-head-main">
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

        {/* 나머지 링크 — 작은 텍스트. 배지(스토어·PyPI)는 오른쪽 컬럼으로 뺀다. */}
        {item.links && (item.links.site || item.links.docs || item.links.repo) && (
          <div
            style={{
              display: "flex",
              gap: 16,
              marginTop: 16,
              fontSize: 12,
              flexWrap: "wrap",
            }}
          >
            {(
              [
                ["site", "live", "var(--accent)"],
                ["docs", "docs", "var(--fg-2)"],
                ["repo", "repo", "var(--fg-2)"],
              ] as const
            ).map(([key, label, color]) =>
              item.links?.[key] ? (
                <a
                  key={key}
                  href={ensureHttp(item.links[key]!)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mono"
                  style={{ color }}
                >
                  {label} ↗
                </a>
              ) : null,
            )}
          </div>
        )}
        </div>

        {/* 오른쪽 끝 — 배지(App Store·Google Play·PyPI) 가로로 크게 */}
        {item.links && (item.links.ios || item.links.android || item.links.pypi) && (
          <div className="project-head-store">
            {item.links.ios && (
              <StoreBadge
                href={ensureHttp(item.links.ios)}
                icon={<AppleLogo />}
                top="Download on the"
                label="App Store"
                bg="var(--bg-3)"
                fg="var(--fg-0)"
              />
            )}
            {item.links.android && (
              <StoreBadge
                href={ensureHttp(item.links.android)}
                icon={<PlayLogo />}
                top="GET IT ON"
                label="Google Play"
                bg="var(--accent)"
                fg="var(--accent-ink)"
              />
            )}
            {item.links.pypi && (
              <StoreBadge
                href={ensureHttp(item.links.pypi)}
                icon={<PyPiLogo />}
                top="pip install"
                label="PyPI"
                bg="var(--bg-3)"
                fg="var(--fg-0)"
              />
            )}
          </div>
        )}
        </div>
      </header>

      <section className="pad-x" style={{ padding: "48px 80px 32px" }}>
        {item.body && item.body.trim().length > 0 ? (
          <article className="contents-body" style={{ maxWidth: 900 }}>
            {/* 이미지 상대참조(assets/…)는 원장(showcase.md) 디렉토리 기준이다 —
                para 를 서빙하는 백엔드 /api/assets 로 풀어 준다. */}
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
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

function StoreBadge({
  href,
  icon,
  top,
  label,
  bg,
  fg,
}: {
  href: string;
  icon: React.ReactNode;
  top: string;
  label: string;
  bg: string;
  fg: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        padding: "10px 18px",
        borderRadius: 10,
        background: bg,
        color: fg,
        border: "1px solid var(--line-2)",
        textDecoration: "none",
      }}
    >
      <span style={{ display: "flex", width: 24, height: 24 }}>{icon}</span>
      <span style={{ display: "flex", flexDirection: "column", lineHeight: 1.1 }}>
        <span style={{ fontSize: 9, opacity: 0.85, letterSpacing: "0.02em" }}>{top}</span>
        <span style={{ fontSize: 16, fontWeight: 600 }}>{label}</span>
      </span>
    </a>
  );
}

function AppleLogo() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24" aria-hidden>
      <path d="M17.05 12.04c-.03-2.5 2.04-3.7 2.13-3.76-1.16-1.7-2.97-1.93-3.61-1.96-1.54-.16-3 .9-3.78.9-.77 0-1.97-.88-3.24-.86-1.67.03-3.21.97-4.07 2.46-1.73 3.01-.44 7.46 1.24 9.9.82 1.19 1.8 2.53 3.08 2.48 1.24-.05 1.71-.8 3.21-.8 1.49 0 1.92.8 3.23.77 1.33-.02 2.18-1.21 3-2.41.94-1.38 1.33-2.72 1.35-2.79-.03-.01-2.59-.99-2.62-3.93zM14.6 4.7c.68-.83 1.14-1.98 1.02-3.13-.98.04-2.17.65-2.88 1.48-.63.73-1.19 1.9-1.04 3.02 1.09.09 2.21-.55 2.9-1.37z"/>
    </svg>
  );
}

function PlayLogo() {
  return (
    <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden>
      <path d="M3.6 2.3c-.2.2-.3.5-.3.9v17.6c0 .4.1.7.3.9l.1.1L13.5 12v-.1L3.7 2.2l-.1.1z" fill="currentColor" opacity="0.9"/>
      <path d="M17 15.3l-3.5-3.4v-.1L17 8.4l4 2.3c1.1.7 1.1 1.7 0 2.3l-4 2.3z" fill="currentColor"/>
      <path d="M17 8.4L13.5 12 3.6 2.3c.4-.4 1-.4 1.7 0L17 8.4z" fill="currentColor" opacity="0.75"/>
      <path d="M17 15.3L5.3 21.7c-.6.4-1.2.3-1.7 0L13.5 12 17 15.3z" fill="currentColor" opacity="0.6"/>
    </svg>
  );
}

function PyPiLogo() {
  return (
    <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24" aria-hidden>
      <path d="M11.6 2c-1.3 0-2.5.1-3.5.3-2.9.5-3.4 1.6-3.4 3.5v2.5h6.8v.9H2.1c-2 0-3.7 1.2-4.2 3.4v.1c-.6 2.5-.6 4 0 6.6.5 2 1.6 3.4 3.5 3.4h2.3v-3c0-2.2 1.9-4.1 4.2-4.1h6.8c1.9 0 3.4-1.6 3.4-3.5V5.8c0-1.9-1.6-3.3-3.4-3.6-1.1-.2-2.3-.2-3.5-.2zM8 4.1c.7 0 1.3.6 1.3 1.3S8.7 6.7 8 6.7s-1.3-.6-1.3-1.3S7.3 4.1 8 4.1z" transform="scale(0.9) translate(1.3 0.5)"/>
    </svg>
  );
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
