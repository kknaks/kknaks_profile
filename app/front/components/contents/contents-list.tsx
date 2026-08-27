import Link from "next/link";

import type { ContentItem } from "@/lib/types";

import { YouTubeFrame } from "./youtube-frame";

/**
 * Contents list — 시안 proto-contents.jsx ContentsList 패턴.
 * 최신 1개는 큰 카드 (영상 + 메타), 나머지는 row list.
 */
export function ContentsList({ items }: { items: ContentItem[] }) {

  if (items.length === 0) {
    return (
      <p style={{ padding: "48px 80px", color: "var(--fg-2)" }}>
        {"아직 업로드된 콘텐츠가 없습니다."}
      </p>
    );
  }

  const [latest, ...rest] = items;

  return (
    <>
      {/* Latest — large card */}
      <section className="pad-x" style={{ padding: "48px 80px 24px" }}>
        <div className="caps" style={{ marginBottom: 16 }}>
          {"최신"}
        </div>
        <Link
          href={`/contents/${latest.slug}`}
          className="card m-stack"
          style={{
            display: "grid",
            gridTemplateColumns: "1.15fr 1fr",
            overflow: "hidden",
            textDecoration: "none",
            color: "inherit",
          }}
        >
          <YouTubeFrame id={latest.youtubeId} title={latest.title} />
          <div
            style={{
              padding: "28px 32px",
              borderLeft: "1px solid var(--line-1)",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                marginBottom: 14,
              }}
            >
              <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                {latest.slug}
              </span>
              <span
                className="mono"
                style={{ fontSize: 11, color: "var(--fg-3)", marginLeft: "auto" }}
              >
                {latest.publishedOn ?? ""}
              </span>
            </div>
            <h2
              style={{
                margin: "0 0 12px",
                fontSize: 26,
                lineHeight: 1.25,
                letterSpacing: "-0.015em",
                fontWeight: 600,
              }}
            >
              {latest.title}
            </h2>
            <p
              style={{
                margin: "0 0 18px",
                color: "var(--fg-1)",
                fontSize: 14,
                lineHeight: 1.65,
              }}
            >
              {latest.summary}
            </p>
            <div
              style={{
                display: "flex",
                gap: 6,
                flexWrap: "wrap",
                marginBottom: 18,
              }}
            >
              {(latest.tags ?? []).map((tag) => (
                <span key={tag} className="tag">
                  {tag.startsWith("#") ? tag : `#${tag}`}
                </span>
              ))}
            </div>
            <div
              style={{
                marginTop: "auto",
                display: "flex",
                alignItems: "center",
                gap: 12,
              }}
            >
              <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                ▶ {latest.duration ?? "—"}
              </span>
              <span
                className="mono"
                style={{ fontSize: 11, color: "var(--accent)", marginLeft: "auto" }}
              >
                {"교안 보기"} →
              </span>
            </div>
          </div>
        </Link>
      </section>

      {/* Rest — list */}
      {rest.length > 0 && (
        <section className="pad-x" style={{ padding: "24px 80px 64px" }}>
          <div className="caps" style={{ marginBottom: 16 }}>
            {"이전 회차"}
          </div>
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {rest.map((c) => (
              <li
                key={c.slug}
                style={{ borderTop: "1px solid var(--line-1)" }}
              >
                <Link
                  href={`/contents/${c.slug}`}
                  className="contents-row"
                  style={{
                    display: "grid",
                    gridTemplateColumns: "120px 1fr 200px 80px",
                    gap: 20,
                    padding: "18px 12px",
                    alignItems: "center",
                    textDecoration: "none",
                    color: "inherit",
                  }}
                >
                  <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                    {c.slug}
                  </span>
                  <div>
                    <div style={{ fontSize: 15, color: "var(--fg-0)", marginBottom: 4 }}>
                      {c.title}
                    </div>
                    <div style={{ fontSize: 13, color: "var(--fg-2)", lineHeight: 1.5 }}>
                      {c.summary}
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {(c.tags ?? []).slice(0, 3).map((tag) => (
                      <span key={tag} className="tag" style={{ fontSize: 10 }}>
                        {tag.startsWith("#") ? tag : `#${tag}`}
                      </span>
                    ))}
                  </div>
                  <span
                    className="mono"
                    style={{ fontSize: 11, color: "var(--fg-3)", textAlign: "right" }}
                  >
                    {c.publishedOn ?? ""}
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}
    </>
  );
}
