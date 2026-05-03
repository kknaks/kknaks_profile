"use client";

import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { DEFAULT_LANG, isLang, type Lang } from "@/lib/i18n";
import type { MeResponse, SiteResponse } from "@/lib/types";

export function PageFooter() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const rawLang = searchParams.get("lang") ?? DEFAULT_LANG;
  const lang: Lang = isLang(rawLang) ? rawLang : DEFAULT_LANG;

  const [me, setMe] = useState<MeResponse | null>(null);
  const [site, setSite] = useState<SiteResponse | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([api.me(lang), api.site(lang)])
      .then(([meData, siteData]) => {
        if (cancelled) return;
        setMe(meData);
        setSite(siteData);
      })
      .catch(() => {
        // 네트워크 실패 시 hardcode fallback 안 함 — 빈 footer 보여줌 (md SoT 원칙).
      });
    return () => {
      cancelled = true;
    };
  }, [lang]);

  if (pathname?.startsWith("/print")) return null;

  const user = me?.user;
  const siteMeta = site?.site;
  const files = site?.files;

  const linkHref = (value: string | undefined) =>
    value ? (value.startsWith("http") ? value : `https://${value}`) : "#";

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
            {user?.handle ?? "kknaks"}
            <span style={{ color: "var(--fg-3)" }}>.dev</span>
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
            {siteMeta?.footerTagline ?? ""}
          </p>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {lang === "en" ? "Contact" : "연락"}
          </div>
          {user?.email && (
            <a
              href={`mailto:${user.email}`}
              style={{
                display: "block",
                fontSize: 13,
                color: "var(--fg-1)",
                padding: "4px 0",
                fontFamily: "var(--font-mono)",
              }}
            >
              {user.email}
            </a>
          )}
          {user?.github && (
            <a
              href={linkHref(user.github)}
              target="_blank"
              rel="noreferrer"
              style={{
                display: "block",
                fontSize: 13,
                color: "var(--fg-1)",
                padding: "4px 0",
                fontFamily: "var(--font-mono)",
              }}
            >
              {user.github}
            </a>
          )}
          {user?.linkedin && (
            <a
              href={linkHref(user.linkedin)}
              target="_blank"
              rel="noreferrer"
              style={{
                display: "block",
                fontSize: 13,
                color: "var(--fg-1)",
                padding: "4px 0",
                fontFamily: "var(--font-mono)",
              }}
            >
              {user.linkedin}
            </a>
          )}
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {lang === "en" ? "Files" : "자료"}
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
            {files?.resumeLabel ?? ""} ↓
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
            {files?.portfolioLabel ?? ""}
          </a>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            {lang === "en" ? "Now" : "현재"}
          </div>
          <div
            className="mono"
            style={{ fontSize: 12, color: "var(--fg-2)", lineHeight: 1.7 }}
          >
            {siteMeta?.location && <div>{siteMeta.location}</div>}
            {siteMeta?.version && <div>v{siteMeta.version}</div>}
            {siteMeta?.uptime && (
              <div style={{ color: "var(--accent)" }}>● uptime {siteMeta.uptime}</div>
            )}
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
          © {siteMeta?.year ?? ""} {user?.handle ?? "kknaks"} · all systems nominal
        </span>
        <span style={{ fontSize: 11, color: "var(--fg-3)" }}>
          built with next.js + python
        </span>
      </div>
    </footer>
  );
}
