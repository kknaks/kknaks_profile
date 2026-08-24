import { api } from "@/lib/api";
import { NotesList } from "@/components/notes/notes-list";

export const dynamic = "force-dynamic";

export default async function NotesPage() {
  let data;
  try {
    data = await api.notes();
  } catch (err) {
    return (
      <main className="pad-x" style={{ padding: "56px 80px" }}>
        <h1>Notes</h1>
        <p style={{ color: "var(--danger)" }}>
          백엔드 응답 실패: {(err as Error).message}
        </p>
      </main>
    );
  }

  const notes = data["notes[]"];

  return (
    <main>
      <header
        className="pad-x m-pad-h"
        style={{
          padding: "56px 80px 32px",
          borderBottom: "1px solid var(--line-1)",
        }}
      >
        <div
          className="mono"
          style={{
            fontSize: 11,
            color: "var(--fg-3)",
            textTransform: "uppercase",
            letterSpacing: "0.14em",
            marginBottom: 12,
          }}
        >
          04 / Notes · {data.notes?.subtitle ?? "읽고 정리한 것"}
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16, flexWrap: "wrap" }}>
          <h1
            className="m-h1"
            style={{
              fontSize: 56,
              lineHeight: 1.05,
              letterSpacing: "-0.025em",
              margin: 0,
              fontWeight: 600,
            }}
          >
            Notes
          </h1>
          <span className="mono" style={{ fontSize: 12, color: "var(--fg-3)" }}>
            {data.notes?.totalCount ?? notes.length} 글
          </span>
        </div>
      </header>

      <NotesList items={notes} />
    </main>
  );
}
