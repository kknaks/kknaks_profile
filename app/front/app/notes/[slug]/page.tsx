import { notFound } from "next/navigation";

import { api } from "@/lib/api";
import { NotesExplorer } from "@/components/notes/notes-explorer";
import { NotesHeader } from "@/components/notes/notes-header";

export const dynamic = "force-dynamic";

/**
 * 직접 URL 진입 — `/notes` 와 같은 탐색기 레이아웃에 해당 노트가 선택된 상태.
 *
 * 본문은 `note.detail_path` 가 가리키는 md 를 백엔드가 읽어 `body` 로 내려준
 * 것이다(erd.md §상세 본문은 DB 에 없다). 이후의 노트 이동은 NotesExplorer 가
 * 클라이언트에서 fetch 하고 URL 만 갈아 끼운다.
 */
export default async function NoteDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;

  let list;
  let detail;
  try {
    [list, detail] = await Promise.all([api.notes(500), api.noteDetail(slug)]);
  } catch {
    notFound();
  }

  const notes = list["notes[]"];

  return (
    <main>
      <NotesHeader
        subtitle={list.notes?.subtitle}
        totalCount={list.notes?.totalCount ?? notes.length}
      />
      <NotesExplorer items={notes} initialDetail={detail["notes.detail"]} />
    </main>
  );
}
