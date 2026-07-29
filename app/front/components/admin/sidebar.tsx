"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import type { AdminUser } from "@/lib/api";

type NavItem = {
  label: string;
  href: string;
  icon: ReactNode;
  ready: boolean; // false = 아직 미구현(준비 중) — 클릭 비활성
};

// 관리 대상 = 블로그 콘텐츠 도메인 미러. 대시보드만 우선 구현, 나머지는 준비 중.
const NAV: NavItem[] = [
  { label: "대시보드", href: "/admin", ready: true, icon: <IconGrid /> },
  { label: "승인 큐", href: "/admin/queue", ready: true, icon: <IconInbox /> },
  { label: "콘텐츠", href: "/admin/contents", ready: false, icon: <IconDoc /> },
  { label: "노트", href: "/admin/notes", ready: false, icon: <IconNote /> },
  { label: "프로젝트", href: "/admin/projects", ready: false, icon: <IconStack /> },
  { label: "알고리즘", href: "/admin/algorithms", ready: false, icon: <IconCode /> },
  { label: "커리어", href: "/admin/career", ready: false, icon: <IconBriefcase /> },
  { label: "설정", href: "/admin/settings", ready: false, icon: <IconGear /> },
];

export function AdminSidebar({
  user,
  onLogout,
}: {
  user: AdminUser | null;
  onLogout: () => void;
}) {
  const pathname = usePathname();

  return (
    <aside
      style={{
        width: 232,
        flexShrink: 0,
        background: "var(--bg-1)",
        borderRight: "1px solid var(--line-1)",
        display: "flex",
        flexDirection: "column",
        // 셸이 뷰포트 높이를 잡고 있다 — sticky 없이 그 높이를 그대로 채운다.
        height: "100%",
      }}
    >
      {/* Brand */}
      <Link
        href="/admin"
        className="mono"
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "18px 20px",
          color: "var(--fg-0)",
          fontSize: 13,
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <span style={{ width: 8, height: 8, background: "var(--accent)", borderRadius: 2 }} />
        kknaks<span style={{ color: "var(--fg-3)" }}>.dev</span>
        <span
          style={{
            marginLeft: 4,
            fontSize: 10,
            letterSpacing: "0.12em",
            color: "var(--fg-3)",
            border: "1px solid var(--line-2)",
            borderRadius: 3,
            padding: "1px 5px",
          }}
        >
          ADMIN
        </span>
      </Link>

      {/* Nav */}
      <nav style={{ padding: "12px 10px", display: "flex", flexDirection: "column", gap: 2 }}>
        {NAV.map((item) => {
          const active =
            item.href === "/admin" ? pathname === "/admin" : pathname?.startsWith(item.href);

          const inner = (
            <span
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "9px 12px",
                borderRadius: 6,
                fontSize: 13,
                color: item.ready
                  ? active
                    ? "var(--fg-0)"
                    : "var(--fg-1)"
                  : "var(--fg-3)",
                background: active ? "var(--bg-3)" : "transparent",
                borderLeft: active
                  ? "2px solid var(--accent)"
                  : "2px solid transparent",
                cursor: item.ready ? "pointer" : "default",
              }}
            >
              <span style={{ display: "flex", width: 16, height: 16, color: "inherit" }}>
                {item.icon}
              </span>
              <span style={{ flex: 1 }}>{item.label}</span>
              {!item.ready && (
                <span
                  className="mono"
                  style={{ fontSize: 9, color: "var(--fg-4)", letterSpacing: "0.08em" }}
                >
                  soon
                </span>
              )}
            </span>
          );

          return item.ready ? (
            <Link key={item.href} href={item.href} style={{ textDecoration: "none" }}>
              {inner}
            </Link>
          ) : (
            <div key={item.href} aria-disabled title="준비 중">
              {inner}
            </div>
          );
        })}
      </nav>

      {/* User + logout */}
      <div
        style={{
          marginTop: "auto",
          padding: "14px 16px",
          borderTop: "1px solid var(--line-1)",
          display: "flex",
          alignItems: "center",
          gap: 10,
        }}
      >
        <span
          style={{
            width: 28,
            height: 28,
            borderRadius: "50%",
            background: "var(--accent-soft)",
            color: "var(--accent)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 12,
            fontWeight: 600,
            textTransform: "uppercase",
          }}
        >
          {user?.username?.[0] ?? "?"}
        </span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 12,
              color: "var(--fg-1)",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {user?.username ?? "—"}
          </div>
          <div className="mono" style={{ fontSize: 10, color: "var(--fg-4)" }}>
            {user?.role ?? ""}
          </div>
        </div>
        <button
          onClick={onLogout}
          title="로그아웃"
          aria-label="로그아웃"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: 30,
            height: 30,
            border: "1px solid var(--line-2)",
            borderRadius: 5,
            background: "transparent",
            color: "var(--fg-2)",
            cursor: "pointer",
          }}
        >
          <IconLogout />
        </button>
      </div>
    </aside>
  );
}

/* ── icons (16px line) ─────────────────────────────────────────────── */
const svg = {
  width: 16,
  height: 16,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

function IconGrid() {
  return (
    <svg {...svg}>
      <rect x="3" y="3" width="7" height="7" />
      <rect x="14" y="3" width="7" height="7" />
      <rect x="14" y="14" width="7" height="7" />
      <rect x="3" y="14" width="7" height="7" />
    </svg>
  );
}
function IconInbox() {
  return (
    <svg {...svg}>
      <path d="M22 12h-6l-2 3h-4l-2-3H2" />
      <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
    </svg>
  );
}
function IconDoc() {
  return (
    <svg {...svg}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
    </svg>
  );
}
function IconNote() {
  return (
    <svg {...svg}>
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4z" />
    </svg>
  );
}
function IconStack() {
  return (
    <svg {...svg}>
      <path d="M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
    </svg>
  );
}
function IconCode() {
  return (
    <svg {...svg}>
      <path d="m16 18 6-6-6-6M8 6l-6 6 6 6" />
    </svg>
  );
}
function IconBriefcase() {
  return (
    <svg {...svg}>
      <rect x="2" y="7" width="20" height="14" rx="2" />
      <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
    </svg>
  );
}
function IconGear() {
  return (
    <svg {...svg}>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}
function IconLogout() {
  return (
    <svg {...svg}>
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
    </svg>
  );
}
