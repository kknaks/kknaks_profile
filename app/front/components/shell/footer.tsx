"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { ProfileResponse, SiteResponse } from "@/lib/types";

export function PageFooter() {
  const pathname = usePathname();

  const [me, setMe] = useState<ProfileResponse | null>(null);
  const [site, setSite] = useState<SiteResponse | null>(null);

  useEffect(() => {
    let cancelled = false;
    Promise.all([api.profile(), api.site()])
      .then(([meData, siteData]) => {
        if (cancelled) return;
        setMe(meData);
        setSite(siteData);
      })
      .catch(() => {
        // 네트워크 실패 시 hardcode fallback 안 함 — 빈 footer 보여줌 (DB SoT 원칙).
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (pathname?.startsWith("/admin")) return null; // 관리자 셸은 자체 레이아웃
  // /chat 은 한 화면짜리 대화 표면이다 — 하단이 고정 컴포저 자리라 푸터를 두지 않는다.
  if (pathname?.startsWith("/chat")) return null;

  const user = me?.profile;
  const copy = site?.site;

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
          gridTemplateColumns: "1.4fr 1fr 1fr",
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
            {user?.handle}
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
            {copy?.footer?.tagline}
          </p>
        </div>

        <div>
          <div className="caps" style={{ marginBottom: 10 }}>
            연락
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
            현재
          </div>
          {/* version·uptime 은 DB 에 없다 — 빌드/런타임 값이라(erd.md §site_config). */}
          <div
            className="mono"
            style={{ fontSize: 12, color: "var(--fg-2)", lineHeight: 1.7 }}
          >
            {user?.location && <div>{user.location}</div>}
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
          © {new Date().getFullYear()} {user?.handle} · all systems nominal
        </span>
        <span style={{ fontSize: 11, color: "var(--fg-3)" }}>
          built with next.js + python
        </span>
      </div>
    </footer>
  );
}
