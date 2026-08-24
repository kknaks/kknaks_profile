// 관리자 대시보드 — 인증 게이트/로그아웃은 (panel)/layout.tsx 셸이 담당.
export default function AdminDashboardPage() {
  return (
    <div style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>대시보드</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          kknaks.dev admin
        </p>
      </header>

      <div
        style={{
          border: "1px dashed var(--line-2)",
          borderRadius: 8,
          padding: 48,
          textAlign: "center",
          color: "var(--fg-3)",
        }}
      >
        <p style={{ fontSize: 15, color: "var(--fg-1)", margin: 0 }}>준비 중</p>
        <p className="mono" style={{ fontSize: 12, marginTop: 8 }}>
          왼쪽 사이드바 항목별 관리 화면을 순차적으로 채웁니다.
        </p>
      </div>
    </div>
  );
}
