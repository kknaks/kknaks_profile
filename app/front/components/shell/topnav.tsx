"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const NAV_ITEMS = [
  { id: "about", label: "About", href: "/about" },
  { id: "career", label: "Career", href: "/career" },
  { id: "projects", label: "Projects", href: "/projects" },
  { id: "notes", label: "Notes", href: "/notes" },
  { id: "contents", label: "Contents", href: "/contents" },
  { id: "algorithms", label: "Algorithms", href: "/algorithms" },
];

export function TopNav() {
  const pathname = usePathname();

  const [menuOpen, setMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 720);
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  // **훅을 전부 부른 뒤에 반환한다.** 종전에는 이 줄이 `useEffect` 앞에 있어서
  // `/admin` 에서 훅 일부만 실행되고 끝났고, React 가 나머지를 기대해
  // `Rendered fewer hooks than expected` 로 **런타임이 죽었다**. 조건부 반환 자체는
  // 괜찮지만 그 위치가 훅 사이면 안 된다(Rules of Hooks).
  if (pathname?.startsWith("/admin")) return null; // 관리자 셸은 자체 레이아웃

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
        href="/"
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
              href={item.href}
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
              {item.label}
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
        <Link
          href="/admin"
          aria-label="admin"
          title="admin"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 30,
            height: 30,
            border: "1px solid var(--line-2)",
            borderRadius: 4,
            color: "var(--fg-2)",
          }}
        >
          <svg
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
          </svg>
        </Link>

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
                href={item.href}
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
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
