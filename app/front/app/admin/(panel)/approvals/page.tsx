// 수집함 · 승인 대기 — 게이트 1·2(케이스 1) + problem 게이트(케이스 6)의 pending 전부.
// 잔디잡·queue 표(erd §미결 7)를 세울 때 채운다. 지금은 자리만.
export default function AdminApprovalsPage() {
  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>승인 대기</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          게이트 1·2 + problem 게이트 — pending 전부 여기
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
          잔디잡을 만들면서 게이트 화면을 채웁니다.
        </p>
      </div>
    </div>
  );
}
