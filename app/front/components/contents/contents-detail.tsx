import Link from "next/link";
import ReactMarkdown from "react-markdown";

import type { ContentDetail } from "@/lib/types";

import { YouTubeFrame } from "./youtube-frame";

/**
 * Contents detail — 시안 proto-contents.jsx ContentsDetail 패턴.
 * 03 영역 (Applied example) 자리에 8섹션 강의 교안 markdown 렌더 (spec-06, adr-05).
 */
export function ContentsDetail({ item }: { item: ContentDetail }) {

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
          href="/contents"
          className="mono"
          style={{
            color: "var(--fg-3)",
            fontSize: 12,
            textDecoration: "none",
            display: "inline-block",
            marginBottom: 20,
          }}
        >
          ← {"전체 회차"}
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
            gap: 12,
          }}
        >
          <span>{item.slug}</span>
          <span>{item.publishedOn ?? ""}</span>
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
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 20 }}>
          {(item.tags ?? []).map((tag) => (
            <span key={tag} className="tag">
              {tag.startsWith("#") ? tag : `#${tag}`}
            </span>
          ))}
        </div>
      </header>

      {/* 01 video + 02 speaker.
          옛 02 자리에는 `concept[]`(요지 6문장) 카드가 있었다. **컬럼이 아니다** —
          본문에 속하므로 `body` 안에 있다(erd.md §content). 화면이 다시 조립하지 않는다. */}
      <div
        className="pad-x m-stack"
        style={{
          padding: "48px 80px 24px",
          display: "grid",
          gridTemplateColumns: "1.4fr 1fr",
          gap: 56,
          alignItems: "start",
        }}
      >
        <div>
          <SectionHeader idx="01" label="video" title={"영상"} />
          <YouTubeFrame id={item.youtubeId} title={item.title} />
          <div
            className="mono"
            style={{
              fontSize: 11,
              color: "var(--fg-3)",
              marginTop: 10,
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>▶ {item.duration ?? "—"}</span>
            <span>youtu.be/{item.youtubeId}</span>
          </div>
        </div>

        <aside>
          <SectionHeader idx="02" label="speaker" title={"출처"} />
          {item.speaker && (
            <div
              style={{
                padding: "16px 20px",
                border: "1px solid var(--line-1)",
                borderRadius: 6,
                background: "var(--bg-1)",
              }}
            >
              <div className="caps" style={{ marginBottom: 8 }}>
                {"발표"}
              </div>
              <div className="mono" style={{ fontSize: 13, color: "var(--fg-0)" }}>
                {item.speaker}
              </div>
            </div>
          )}
        </aside>
      </div>

      {/* 03 강의 교안 — 시안 03 Applied example 영역에 markdown body 렌더 */}
      <section
        className="pad-x"
        style={{ padding: "32px 80px 32px" }}
      >
        <SectionHeader
          idx="03"
          label="material"
          title={"학습 자료"}
        />
        <article className="contents-body">
          <ReactMarkdown>{item.body}</ReactMarkdown>
        </article>
      </section>

      {/* Prev / Next nav */}
      <ContentsPrevNext
        newer={item.newer}
        older={item.older}
      />
    </>
  );
}

function SectionHeader({
  idx,
  label,
  title,
}: {
  idx: string;
  label: string;
  title: string;
}) {
  return (
    <div
      style={{
        marginBottom: 18,
        display: "flex",
        alignItems: "baseline",
        gap: 12,
      }}
    >
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
        {idx}
      </span>
      <h2
        style={{
          margin: 0,
          fontSize: 22,
          letterSpacing: "-0.015em",
          fontWeight: 600,
        }}
      >
        {title}
      </h2>
      <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
        · {label}
      </span>
    </div>
  );
}

function ContentsPrevNext({
  newer,
  older,
}: {
  newer: ContentDetail["newer"];
  older: ContentDetail["older"];
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
          href={`/contents/${newer.slug}`}
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
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}>
            ← {"다음 회차"}
          </div>
          <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{newer.title}</div>
        </Link>
      ) : (
        <div />
      )}
      {older ? (
        <Link
          href={`/contents/${older.slug}`}
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
          <div className="mono" style={{ fontSize: 11, color: "var(--fg-3)", marginBottom: 6 }}>
            {"이전 회차"} →
          </div>
          <div style={{ fontSize: 14, color: "var(--fg-0)" }}>{older.title}</div>
        </Link>
      ) : (
        <div />
      )}
    </nav>
  );
}
