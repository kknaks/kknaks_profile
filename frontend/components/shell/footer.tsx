"use client";

import { useSearchParams } from "next/navigation";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";

export function PageFooter() {
  const searchParams = useSearchParams();
  const rawLang = searchParams.get("lang") ?? DEFAULT_LANG;
  const lang: Lang = isLang(rawLang) ? rawLang : DEFAULT_LANG;
  const t = (ko: string, en: string) => (lang === "en" ? en : ko);

  return (
    <footer
      className="pad-x"
      style={{
        borderTop: "1px solid var(--line-1)",
        padding: "40px 32px 24px",
        marginTop: 80,
      }}
    >
      <div
        className="m-stack"
        style={{
          display: "grid",
          gridTemplateColumns: "1.4fr 1fr 1fr 1fr",
          gap: 32,
        }}
      >
        <div>
          <div
            className="mono"
            style={{
              fontSize: 13,
              marginBottom: 8,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ width: 8, height: 8, background: "var(--accent)", borderRadius: 2 }} />
            kknaks<span style={{ color: "var(--fg-3)" }}>.dev</span>
          </div>
          <p
            style={{
              margin: 0,
              fontSize: 13,
              color: "var(--fg-2)",
              lineHeight: 1.6,
              maxWidth: 320,
            }}
          >
            {t(
              "홈서버에서 직접 호스팅하는 작은 포트폴리오. Next.js + Python.",
              "A small portfolio self-hosted on my home server. Next.js + Python.",
            )}
          </p>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {t("연락", "Contact")}
          </div>
          <a
            href="mailto:hello@kknaks.dev"
            style={{
              display: "block",
              fontSize: 13,
              color: "var(--fg-1)",
              padding: "4px 0",
              fontFamily: "var(--font-mono)",
            }}
          >
            hello@kknaks.dev
          </a>
          <a
            href="https://github.com/kknaks"
            style={{
              display: "block",
              fontSize: 13,
              color: "var(--fg-1)",
              padding: "4px 0",
              fontFamily: "var(--font-mono)",
            }}
          >
            github.com/kknaks
          </a>
          <a
            href="#"
            style={{
              display: "block",
              fontSize: 13,
              color: "var(--fg-1)",
              padding: "4px 0",
              fontFamily: "var(--font-mono)",
            }}
          >
            linkedin/in/kknaks
          </a>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {t("자료", "Files")}
          </div>
          <a
            href="#"
            style={{
              display: "block",
              fontSize: 13,
              color: "var(--fg-1)",
              padding: "4px 0",
            }}
          >
            {t("이력서 (PDF) ↓", "Resume (PDF) ↓")}
          </a>
          <a
            href="#"
            style={{
              display: "block",
              fontSize: 13,
              color: "var(--fg-1)",
              padding: "4px 0",
            }}
          >
            {t("포트폴리오 (PDF)", "Portfolio (PDF)")}
          </a>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {t("현재", "Now")}
          </div>
          <div
            className="mono"
            style={{ fontSize: 12, color: "var(--fg-2)", lineHeight: 1.7 }}
          >
            <div>seoul · KST</div>
            <div>v0.1.0 · stable</div>
            <div style={{ color: "var(--accent)" }}>● uptime 99.4%</div>
          </div>
        </div>
      </div>

      <div
        className="mono"
        style={{
          display: "flex",
          justifyContent: "space-between",
          borderTop: "1px solid var(--line-1)",
          marginTop: 32,
          paddingTop: 16,
        }}
      >
        <span style={{ fontSize: 11, color: "var(--fg-3)" }}>
          © 2026 kknaks · all systems nominal
        </span>
        <span style={{ fontSize: 11, color: "var(--fg-3)" }}>
          built with next.js + python
        </span>
      </div>
    </footer>
  );
}
