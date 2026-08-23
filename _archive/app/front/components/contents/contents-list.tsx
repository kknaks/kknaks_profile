import Link from "next/link";

import type { Lang } from "@/lib/i18n";
import type { ContentItem } from "@/lib/types";

import { YouTubeFrame } from "./youtube-frame";

/**
 * Contents list — 시안 proto-contents.jsx ContentsList 패턴.
 * 최신 1개는 큰 카드 (영상 + 메타), 나머지는 row list.
 */
export function ContentsList({
  items,
  lang,
}: {
  items: ContentItem[];
  lang: Lang;
}) {
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  if (items.length === 0) {
    return (
      <p style={{ padding: "48px 80px", color: "var(--fg-2)" }}>
        {t("아직 업로드된 콘텐츠가 없습니다.", "No contents uploaded yet.")}
      </p>
    );
  }

  const [latest, ...rest] = items;

  return (
    <>
      {/* Latest — large card */}
      <section className="pad-x" style={{ padding: "48px 80px 24px" }}>
        <div className="caps" style={{ marginBottom: 16 }}>
          {t("최신", "latest")}
        </div>
        <Link
          href={`/contents/${latest.id}${lang === "en" ? "?lang=en" : ""}`}
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
                {latest.id}
              </span>
              <span
                className="tag"
                style={{
                  color: "var(--accent)",
                  background: "var(--accent-soft)",
                  borderColor: "var(--accent-line)",
                }}
              >
                <span className="tag-dot" style={{ background: "var(--accent)" }} />
                {latest.day}
              </span>
              <span
                className="mono"
                style={{ fontSize: 11, color: "var(--fg-3)", marginLeft: "auto" }}
              >
                {latest.date}
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
                {t("교안 보기", "open sheet")} →
              </span>
            </div>
          </div>
        </Link>
      </section>

      {/* Rest — list */}
      {rest.length > 0 && (
        <section className="pad-x" style={{ padding: "24px 80px 64px" }}>
          <div className="caps" style={{ marginBottom: 16 }}>
            {t("이전 회차", "previous")}
          </div>
          <ul style={{ margin: 0, padding: 0, listStyle: "none" }}>
            {rest.map((c) => (
              <li
                key={c.id}
                style={{ borderTop: "1px solid var(--line-1)" }}
              >
                <Link
                  href={`/contents/${c.id}${lang === "en" ? "?lang=en" : ""}`}
                  className="contents-row"
                  style={{
                    display: "grid",
                    gridTemplateColumns: "76px 88px 1fr 200px 80px",
                    gap: 20,
                    padding: "18px 12px",
                    alignItems: "center",
                    textDecoration: "none",
                    color: "inherit",
                  }}
                >
                  <span className="mono" style={{ fontSize: 11, color: "var(--fg-3)" }}>
                    {c.id}
                  </span>
                  <span className="mono" style={{ fontSize: 11, color: "var(--fg-2)" }}>
                    {c.day}
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
                    {c.date}
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
