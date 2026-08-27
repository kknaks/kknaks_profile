import { api } from "@/lib/api";
import { NotesExplorer } from "@/components/notes/notes-explorer";
import { NotesHeader } from "@/components/notes/notes-header";

export const dynamic = "force-dynamic";

/**
 * 공개 글 — 탐색기형. 목록은 전체가 필요하다 — 트리가 폴더별 전량을 그리므로
 * 기본 limit(50)보다 큰 값을 보낸다. 노트 선택 전이므로 initialDetail 은 null.
 */
export default async function NotesPage() {
  let data;
  try {
    data = await api.notes(500);
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
      <NotesHeader
        subtitle={data.notes?.subtitle}
        totalCount={data.notes?.totalCount ?? notes.length}
      />
      <NotesExplorer items={notes} initialDetail={null} />
    </main>
  );
}
