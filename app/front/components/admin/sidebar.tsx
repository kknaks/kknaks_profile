"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { AdminUser } from "@/lib/api";

type NavItem = {
  label: string;
  href: string;
  icon: ReactNode;
  ready: boolean; // false = 아직 미구현(준비 중) — 클릭 비활성
};

type NavSection = {
  title: string;
  items: NavItem[];
};

// 리뉴얼 — 그룹 단위로 하나씩 다시 채운다. 그룹 = 어드민이 하는 일 묶음.
const NAV: NavSection[] = [
  {
    // 케이스 1(자료 캡처)·케이스 6(problem 게이트)의 자리 — 잔디잡 만들 때 채운다.
    // 승인도 인박스 행 펼침에서 한다 — 넣는 곳·보는 곳·승인하는 곳이 한 페이지.
    title: "수집함",
    items: [
      { label: "인박스", href: "/admin/capture", ready: true, icon: <IconInbox /> },
    ],
  },
  {
    // 채용담당자가 남긴 대화를 읽는 자리(SPEC-017 U-8). 읽기 전용 — 여기서
    // 대화에 개입하지 않는다. 「수집함」과 나눠 둔 건 주체가 달라서다 —
    // 저쪽은 내가 넣은 것, 이쪽은 방문자가 물은 것.
    title: "방문자",
    items: [
      { label: "채팅", href: "/admin/chats", ready: true, icon: <IconChat /> },
    ],
  },
  {
    title: "프로필",
    items: [
      { label: "기본 정보", href: "/admin/profile", ready: true, icon: <IconUser /> },
      { label: "사이트 문구", href: "/admin/site-config", ready: true, icon: <IconDoc /> },
      { label: "커밋 히스토리", href: "/admin/commits", ready: true, icon: <IconCommit /> },
    ],
  },
  {
    title: "커리어",
    items: [
      { label: "회사", href: "/admin/companies", ready: true, icon: <IconBuilding /> },
      { label: "역할", href: "/admin/careers", ready: true, icon: <IconBriefcase /> },
      { label: "해결한 문제", href: "/admin/problems", ready: true, icon: <IconTarget /> },
      { label: "교육", href: "/admin/education", ready: true, icon: <IconBook /> },
    ],
  },
  {
    title: "프로젝트",
    items: [
      { label: "회사 제품", href: "/admin/products", ready: true, icon: <IconStack /> },
      { label: "개인 프로젝트", href: "/admin/projects", ready: true, icon: <IconCode /> },
    ],
  },
  {
    title: "리소스",
    items: [
      { label: "노트", href: "/admin/notes", ready: true, icon: <IconNote /> },
      { label: "콘텐츠", href: "/admin/contents", ready: true, icon: <IconPlay /> },
      { label: "알고리즘", href: "/admin/algorithms", ready: true, icon: <IconCode /> },
    ],
  },
  {
    title: "설정",
    items: [
      { label: "깃 토큰", href: "/admin/git-tokens", ready: true, icon: <IconGear /> },
    ],
  },
];

export function AdminSidebar({
  user,
  onLogout,
}: {
  user: AdminUser | null;
  onLogout: () => void;
}) {
  const pathname = usePathname();

  // 모바일은 shell/topnav 와 같은 패턴 — 햄버거 + 드롭다운 (≤720).
  const [isMobile, setIsMobile] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 720);
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  const isActive = (href: string) =>
    href === "/admin" ? pathname === "/admin" : Boolean(pathname?.startsWith(href));

  if (isMobile) {
    return (
      <div
        style={{
          position: "sticky",
          top: 0,
          zIndex: 20,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "12px 16px",
          background: "var(--bg-1)",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <Link
          href="/admin"
          className="mono"
          style={{ display: "flex", alignItems: "center", gap: 8, color: "var(--fg-0)", fontSize: 12 }}
        >
          <span style={{ width: 8, height: 8, background: "var(--accent)", borderRadius: 2 }} />
          kknaks<span style={{ color: "var(--fg-3)" }}>.dev</span>
          <span
            style={{
              marginLeft: 4,
              fontSize: 9,
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

        <button
          aria-label="menu"
          onClick={() => setMenuOpen((o) => !o)}
          style={{
            marginLeft: "auto",
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

        {menuOpen && (
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
              // 항목이 화면보다 길다 — 헤더(sticky) 아래 남은 높이 안에서 자체 스크롤.
              maxHeight: "calc(100dvh - 60px)",
              overflowY: "auto",
              WebkitOverflowScrolling: "touch",
            }}
          >
            {NAV.map((section) => (
              <div key={section.title}>
                <div
                  className="mono"
                  style={{
                    padding: "10px 20px 4px",
                    fontSize: 9,
                    letterSpacing: "0.12em",
                    color: "var(--fg-4)",
                  }}
                >
                  {section.title}
                </div>
                {section.items.map((item) => {
                  const active = isActive(item.href);
                  const row = (
                    <span
                      style={{
                        display: "flex",
                        alignItems: "center",
                        gap: 12,
                        padding: "13px 20px",
                        fontSize: 13,
                        background: active ? "var(--bg-2)" : "transparent",
                        color: item.ready
                          ? active
                            ? "var(--fg-0)"
                            : "var(--fg-1)"
                          : "var(--fg-3)",
                        borderLeft: active
                          ? "2px solid var(--accent)"
                          : "2px solid transparent",
                      }}
                    >
                      <span style={{ display: "flex", width: 16, height: 16 }}>{item.icon}</span>
                      <span style={{ flex: 1 }}>{item.label}</span>
                      {!item.ready && (
                        <span
                          className="mono"
                          style={{ fontSize: 8, color: "var(--fg-4)", letterSpacing: "0.08em" }}
                        >
                          soon
                        </span>
                      )}
                    </span>
                  );
                  return item.ready ? (
                    <Link key={item.href} href={item.href} style={{ textDecoration: "none", display: "block" }}>
                      {row}
                    </Link>
                  ) : (
                    <div key={item.href} aria-disabled title="준비 중">
                      {row}
                    </div>
                  );
                })}
              </div>
            ))}

            <div style={{ borderTop: "1px solid var(--line-1)", marginTop: 8 }}>
              <Link
                href="/"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "13px 20px",
                  fontSize: 13,
                  color: "var(--fg-1)",
                  textDecoration: "none",
                }}
              >
                <span style={{ display: "flex", width: 16, height: 16 }}>
                  <IconExternal />
                </span>
                블로그로 가기
              </Link>
              <button
                onClick={onLogout}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "13px 20px",
                  fontSize: 13,
                  color: "var(--fg-1)",
                  background: "transparent",
                  border: "none",
                  width: "100%",
                  cursor: "pointer",
                  textAlign: "left",
                }}
              >
                <span style={{ display: "flex", width: 16, height: 16 }}>
                  <IconLogout />
                </span>
                로그아웃
                <span className="mono" style={{ marginLeft: "auto", fontSize: 10, color: "var(--fg-4)" }}>
                  {user?.username}
                </span>
              </button>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <aside
      className="admin-sidebar"
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
          fontSize: 12,
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <span style={{ width: 8, height: 8, background: "var(--accent)", borderRadius: 2 }} />
        kknaks<span style={{ color: "var(--fg-3)" }}>.dev</span>
        <span
          style={{
            marginLeft: 4,
            fontSize: 9,
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
      <nav
        className="admin-nav"
        style={{ padding: "12px 10px", display: "flex", flexDirection: "column", gap: 14 }}
      >
        {NAV.map((section) => (
          <div
            key={section.title}
            className="admin-nav-section"
            style={{ display: "flex", flexDirection: "column", gap: 2 }}
          >
            <div
              className="mono admin-nav-section-title"
              style={{
                padding: "0 12px 6px",
                fontSize: 9,
                letterSpacing: "0.12em",
                color: "var(--fg-4)",
              }}
            >
              {section.title}
            </div>
            {section.items.map((item) => {
              const active =
                item.href === "/admin" ? pathname === "/admin" : pathname?.startsWith(item.href);

              const inner = (
            <span
              className="admin-nav-item"
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "9px 12px",
                borderRadius: 6,
                fontSize: 12,
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
                  style={{ fontSize: 8, color: "var(--fg-4)", letterSpacing: "0.08em" }}
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
          </div>
        ))}
      </nav>

      {/*
        블로그로 나가는 문. 관리자 셸에는 이것 말고 밖으로 가는 링크가 없어서,
        들어오면 주소를 직접 고치거나 뒤로가기를 눌러야 나갈 수 있었다.
        로그아웃 옆이 아니라 **위**에 두는 이유는 둘이 다른 일이기 때문이다 —
        나가는 것과 세션을 끊는 것을 나란히 두면 눌러야 할 쪽을 헷갈린다.
      */}
      <Link
        href="/"
        className="m-hide"
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          // `auto` 가 위쪽을 밀어 하단에 붙인다. 좌우 10px 은 nav 항목과 같은 선.
          margin: "auto 10px 0",
          padding: "9px 12px",
          borderRadius: 6,
          fontSize: 12,
          color: "var(--fg-1)",
          textDecoration: "none",
        }}
      >
        <span style={{ display: "flex", width: 16, height: 16 }}>
          <IconExternal />
        </span>
        <span style={{ flex: 1 }}>블로그로 가기</span>
      </Link>

      {/* User + logout */}
      <div
        className="admin-user-row"
        style={{
          padding: "14px 16px",
          marginTop: 12,
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
            fontSize: 11,
            fontWeight: 600,
            textTransform: "uppercase",
          }}
        >
          {user?.username?.[0] ?? "?"}
        </span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div
            style={{
              fontSize: 11,
              color: "var(--fg-1)",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {user?.username ?? "—"}
          </div>
          <div className="mono" style={{ fontSize: 9, color: "var(--fg-4)" }}>
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

function IconPlay() {
  return (
    <svg {...svg}>
      <circle cx="12" cy="12" r="10" />
      <path d="m10 8 6 4-6 4V8z" />
    </svg>
  );
}
function IconBuilding() {
  return (
    <svg {...svg}>
      <rect x="4" y="2" width="16" height="20" rx="2" />
      <path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M8 10h.01M16 10h.01M12 10h.01M8 14h.01M16 14h.01M12 14h.01" />
    </svg>
  );
}
function IconTarget() {
  return (
    <svg {...svg}>
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  );
}
function IconBook() {
  return (
    <svg {...svg}>
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  );
}
function IconUser() {
  return (
    <svg {...svg}>
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
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
function IconChat() {
  return (
    <svg {...svg}>
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
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
function IconCommit() {
  return (
    <svg {...svg}>
      <circle cx="12" cy="12" r="4" />
      <path d="M1.05 12H8M16 12h6.95" />
    </svg>
  );
}
function IconExternal() {
  return (
    <svg {...svg}>
      <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
      <path d="M15 3h6v6M10 14 21 3" />
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
