// 수집함 · 자료 캡처 — 케이스 1: 종류 선택 + 메모 모달 → queue → 비동기 처리 폴링.
// 잔디잡·queue 표(erd §미결 7)를 세울 때 채운다. 지금은 자리만.
export default function AdminCapturePage() {
  return (
    <div className="admin-page" style={{ padding: "28px 32px", maxWidth: 960, margin: "0 auto" }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, color: "var(--fg-0)", margin: 0 }}>자료 캡처</h1>
        <p className="mono" style={{ fontSize: 12, color: "var(--fg-3)", marginTop: 6 }}>
          케이스 1 — 종류 선택 · queue · 비동기 처리
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
          queue 표(erd §미결 7)가 정해지면 채웁니다.
        </p>
      </div>
    </div>
  );
}
