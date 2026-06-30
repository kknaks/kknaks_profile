"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { DEFAULT_LANG, isLang, SUPPORTED_LANGS, type Lang } from "@/lib/i18n";

const NAV_ITEMS = [
  { id: "about", label: { ko: "About", en: "About" }, href: "/about" },
  { id: "career", label: { ko: "Career", en: "Career" }, href: "/career" },
  { id: "projects", label: { ko: "Projects", en: "Projects" }, href: "/projects" },
  { id: "notes", label: { ko: "Notes", en: "Notes" }, href: "/notes" },
  { id: "contents", label: { ko: "Contents", en: "Contents" }, href: "/contents" },
  { id: "algorithms", label: { ko: "Algorithms", en: "Algorithms" }, href: "/algorithms" },
  { id: "graph", label: { ko: "Graph", en: "Graph" }, href: "/graph" },
];

export function TopNav() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const rawLang = searchParams.get("lang") ?? DEFAULT_LANG;
  const lang: Lang = isLang(rawLang) ? rawLang : DEFAULT_LANG;

  const [menuOpen, setMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  if (pathname?.startsWith("/print")) return null;

  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 720);
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  const withLang = (href: string) => (lang === DEFAULT_LANG ? href : `${href}?lang=${lang}`);
  const langSwitchHref = (target: Lang) => {
    const sp = new URLSearchParams(searchParams);
    if (target === DEFAULT_LANG) sp.delete("lang");
    else sp.set("lang", target);
    const qs = sp.toString();
    return qs ? `${pathname}?${qs}` : pathname;
  };

  const activeId = pathname === "/" ? "home" : pathname.split("/")[1];

  return (
    <div
      className="topnav-wrap pad-x"
      style={{
        position: "sticky",
        top: 0,
        zIndex: 20,
        padding: "14px 32px",
        display: "flex",
        alignItems: "center",
        gap: 24,
        borderBottom: "1px solid var(--line-1)",
        background: "rgba(10,11,13,0.75)",
        backdropFilter: "blur(10px)",
      }}
    >
      <Link
        href={withLang("/")}
        className="mono"
        style={{
          color: "var(--fg-0)",
          fontSize: 13,
          display: "flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span style={{ width: 8, height: 8, background: "var(--accent)", borderRadius: 2 }} />
        kknaks<span style={{ color: "var(--fg-3)" }}>.dev</span>
      </Link>

      <nav className="m-hide" style={{ display: "flex", gap: 4, marginLeft: 16 }}>
        {NAV_ITEMS.map((item, idx) => {
          const active = activeId === item.id;
          return (
            <Link
              key={item.id}
              href={withLang(item.href)}
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: 12,
                padding: "6px 10px",
                color: active ? "var(--fg-0)" : "var(--fg-2)",
                borderBottom: active
                  ? "1px solid var(--accent)"
                  : "1px solid transparent",
                transition: "color 120ms",
              }}
            >
              <span style={{ color: "var(--fg-3)" }}>0{idx + 1} </span>
              {item.label[lang]}
            </Link>
          );
        })}
      </nav>

      <div style={{ marginLeft: "auto", display: "flex", gap: 10, alignItems: "center" }}>
        <span
          className="mono m-hide"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            display: "flex",
            alignItems: "center",
            gap: 6,
          }}
        >
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              background: "var(--accent)",
              boxShadow: "0 0 0 3px var(--accent-soft)",
            }}
          />
          online
        </span>
        <div
          style={{
            display: "flex",
            border: "1px solid var(--line-2)",
            borderRadius: 4,
            overflow: "hidden",
          }}
        >
          {SUPPORTED_LANGS.map((l) => (
            <Link
              key={l}
              href={langSwitchHref(l)}
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: 11,
                padding: "4px 8px",
                background: lang === l ? "var(--bg-3)" : "transparent",
                color: lang === l ? "var(--fg-0)" : "var(--fg-3)",
              }}
            >
              {l.toUpperCase()}
            </Link>
          ))}
        </div>

        {isMobile && (
          <button
            aria-label="menu"
            onClick={() => setMenuOpen((o) => !o)}
            style={{
              display: "flex",
              width: 36,
              height: 32,
              background: menuOpen ? "var(--bg-3)" : "transparent",
              border: "1px solid var(--line-2)",
              borderRadius: 4,
              cursor: "pointer",
              padding: 0,
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: 4,
            }}
          >
            <span
              style={{
                display: "block",
                width: 16,
                height: 1,
                background: "var(--fg-0)",
                transform: menuOpen ? "translateY(2.5px) rotate(45deg)" : "none",
                transition: "transform 160ms",
              }}
            />
            <span
              style={{
                display: "block",
                width: 16,
                height: 1,
                background: "var(--fg-0)",
                opacity: menuOpen ? 0 : 1,
                transition: "opacity 120ms",
              }}
            />
            <span
              style={{
                display: "block",
                width: 16,
                height: 1,
                background: "var(--fg-0)",
                transform: menuOpen ? "translateY(-2.5px) rotate(-45deg)" : "none",
                transition: "transform 160ms",
              }}
            />
          </button>
        )}
      </div>

      {menuOpen && isMobile && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            background: "var(--bg-1)",
            borderBottom: "1px solid var(--line-1)",
            padding: "8px 0",
            boxShadow: "var(--shadow-pop)",
          }}
        >
          {NAV_ITEMS.map((item, idx) => {
            const active = activeId === item.id;
            return (
              <Link
                key={item.id}
                href={withLang(item.href)}
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: 14,
                  padding: "14px 20px",
                  background: active ? "var(--bg-2)" : "transparent",
                  color: active ? "var(--fg-0)" : "var(--fg-1)",
                  borderLeft: active
                    ? "2px solid var(--accent)"
                    : "2px solid transparent",
                  textAlign: "left",
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                }}
              >
                <span style={{ color: "var(--fg-3)" }}>0{idx + 1}</span>
                <span>{item.label[lang]}</span>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
